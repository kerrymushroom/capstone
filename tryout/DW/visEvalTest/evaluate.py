# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import base64
import json
import logging
import os
from typing import Union

import cairosvg
import pandas as pd
from attr import dataclass

from .check import (
    chart_check,
    data_check,
    deconstruct,
    layout_check,
    order_check,
    readability_check,
    scale_and_ticks_check,
)
from .dataset import Dataset


@dataclass
class CheckResult:
    answer: Union[bool, int]
    aspect: str
    rationale: str

    def get_json(self):
        return {
            "answer": self.answer,
            "aspect": self.aspect,
            "rationale": self.rationale,
        }

'''
an example of CheckResult
CheckResult(
            answer=True,
            aspect="code execution",
            rationale="Code executed successfully.",
        )
'''

@dataclass
class EvaluationDetail:
    id: str
    results: list[list[CheckResult]]

# test if the code could execute
VALID_ASPECTS = ["code execution", "surface-form check"]
# check the data requirement
LEGAL_ASPECTS = ["deconstruction", "chart type check", "data check", "order check"]
# use llm to evaluate itself in visualization readability test
# layout check and scale and sticks check requires vision model
READABILITY_ASPECT = ["layout check", "scale and ticks check", "readability check"]

FAIL_ASPECTS = VALID_ASPECTS + LEGAL_ASPECTS + ["layout check", "scale and ticks check"]


class EvaluationResult:
    dataset: Dataset
    details: list[EvaluationDetail]

    def __init__(self, dataset: Dataset, details: list[EvaluationDetail]):
        self.dataset = dataset
        self.details = details

    def detail_records(self) -> pd.DataFrame:
        records = []
        for detail in self.details:
            id = detail.id
            instance_results = detail.results
            count = len(instance_results)
            record = {
                "id": id,
                "chart": self.dataset.dict[id]["chart"],
                "hardness": self.dataset.dict[id]["hardness"],
            }

            # fail rate
            for aspect in FAIL_ASPECTS:
                evaluate_result = [
                    (
                        all(
                            [
                                item.answer
                                for item in query_results
                                if item.aspect == aspect
                            ]
                        )
                    )
                    for query_results in instance_results
                ]
                fail_result = [item for item in evaluate_result if not item]
                record[f"{aspect}_fail_rate"] = len(fail_result) / count

            high_level_dimensions = [
                ["invalid_rate", VALID_ASPECTS],
                ["illegal rate", LEGAL_ASPECTS],
            ]
            pass_count = count
            for dimension in high_level_dimensions:
                evaluate_result = [
                    (
                        all(
                            [
                                item.answer
                                for item in query_results
                                if (item.aspect in dimension[1])
                            ]
                        )
                    )
                    for query_results in instance_results
                ]
                false_count = len([item for item in evaluate_result if not item])
                record[dimension[0]] = false_count / count
                pass_count -= false_count
                records.append(record)

            # pass rate
            record["pass_rate"] = pass_count / count
            records.append(record)

            # readability score
            evaluate_result = [
                (
                    sum(
                        [
                            item.answer
                            for item in query_results
                            if item.aspect == "readability check"
                        ]
                    )
                )
                for query_results in instance_results
            ]
            if pass_count > 0:
                record["readability_score"] = sum(evaluate_result) / pass_count

            record["quality_score"] = sum(evaluate_result) / count

        return pd.DataFrame(records)

    def score(self):
        records = self.detail_records()
        metrics = [
            "invalid_rate",
            "illegal rate",
            "pass_rate"
        ]
        score = {}
        for metric in metrics:
            score[metric] = records[metric].mean()

        for key in records.keys():
            if (
                key not in metrics
                and key != "id"
                and key != "chart"
                and key != "hardness"
            ):
                score[key] = records[key].mean()

        return score


def convert_svg_to_base64(svg_string):
    png_string = cairosvg.svg2png(bytestring=svg_string)
    base64_encoded = base64.b64encode(png_string).decode("utf-8")
    return f"data:image/png;base64,{base64_encoded}"


class Evaluator:
    def __init__(self, webdriver_path=None, vision_model=None):
        self.webdriver_path = webdriver_path
        self.vision_model = vision_model

    def evaluate(self, agent, dataset, config):
        use_logs = False
        evaluation_details = []
        # set logs 
        if "logs" in config:
            log_folder = config["logs"]
            isExists = os.path.exists(log_folder)
            try:
                if not isExists:
                    os.makedirs(log_folder)
                logging.basicConfig(
                    level=logging.INFO,
                    filename=log_folder / "evaluation.log",
                    filemode="a",
                    format="%(levelname)s: %(message)s",
                )
                use_logs = True
            except Exception as e:
                print(e)

        # 使用了dataset.benchmark
        for instance in dataset.benchmark:
            # codes are initially empty list
            codes = []
            instance_results = []
            # get nl_queries from visEval_single.json dict value, nl_queries could be a list of queries
            nl_queries = instance["nl_queries"]
            # get relevant tables csv path list
            tables = instance["tables"]

            # if log_folder / "evaluation.log" folder is created
            if use_logs:
                instanceFolder = log_folder / instance["id"]
                path = instanceFolder / "result.json"
                if os.path.exists(path):
                    with open(path, "r") as f:
                        data = json.load(f)
                        if "codes" in data and "evaluations" in data:
                            instance_results = []
                            for query_result in data["evaluations"]:
                                results = [
                                    CheckResult(
                                        answer=result["answer"],
                                        aspect=result["aspect"],
                                        rationale=result["rationale"],
                                    )
                                    for result in query_result
                                ]
                                instance_results.append(results)
                            evaluation_details.append(
                                EvaluationDetail(instance["id"], instance_results)
                            )
                            continue
                else:
                    logging.info(f"Instance ({instance['id']}) evaluation began.")
                    isExists = os.path.exists(instanceFolder)
                    if not isExists:
                        os.makedirs(instanceFolder)

            # 同一个id, query有很多问法，是个list
            for index in range(len(nl_queries)):
                nl_query = nl_queries[index]
                if index < len(codes):
                    code = codes[index]
                    # context initially is an empty dict
                    context = {}
                    # context keys: "tables", "library",之后"svg_string"
                    context["tables"] = tables
                else:
                    # generate two things: 1.前置代码pre_code + "\n" + 返回代码code(llm response), 2.context single element dict:{"tables": tables,} 此时context里没有svg_string, 只有tables
                    code, context = agent.generate(nl_query, tables, config)
                    # add code element to codes list
                    codes.append(code)
                if code is None:
                    results = [
                        CheckResult(
                            answer=False,
                            aspect="generation",
                            rationale="Code generation failed.",
                        )
                    ]
                # 此处继续处理
                else:
                    # add library in config to context, like "matplotlib", "seaborn"
                    # now context dict has two keys: "tables","library"
                    context["library"] = config["library"]
                    if use_logs:
                        results = self.validity_check(
                            code, context, agent, instanceFolder / f"{index}.svg"
                        )
                    else:
                        results = self.validity_check(code, context, agent)

                    pass_validity = all([result.answer for result in results])
                    # 如果validity_check通过
                    if pass_validity:
                        ground_truth = {
                            # "chart": "Bar"
                            "chart": instance["chart"],
                            # "vis_obj": {"chart": "bar", "x_name": "Rank", "y_name": "COUNT(Rank)", "x_data": [["AssocProf", "AsstProf", "Instructor", "Professor"]], "y_data": [[8, 15, 8, 27]], "classify": [], "describe": "GROUP BY Rank", "sort": null}
                            "vis_obj": instance["vis_obj"],
                            # "query_meta": [{"channel_specified": []}, {"channel_specified": []}]}
                            # 有的query_meta值更多
                            #query_meta": [{"channel_specified": [], "sort_by": "field"}, {"channel_specified": [], "sort_by": "field"}, {"channel_specified": [], "sort_by": "field"}]
                            "meta_info": instance["query_meta"][index],
                        }
                        # 进行legality_check, 加上个ground_truth 字典
                        results += self.legality_check(context, ground_truth)

                    pass_legality = all([result.answer for result in results])
                    if pass_legality:
                        # 如果通过legality测试，再继续使用gptVision进行readability测试
                        results += self.readability_evaluate(context, nl_query)

                instance_results.append(results)

            evaluation_details.append(
                EvaluationDetail(instance["id"], instance_results)
            )
            if use_logs:
                logging.info(f"Instance ({instance['id']}) evaluation finished.")
                # convert CheckResult to json
                instance_results = [
                    [result.get_json() for result in results]
                    for results in instance_results
                ]
                with open(log_folder / (instance["id"] + "/result.json"), "w") as f:
                    f.write(
                        json.dumps({"codes": codes, "evaluations": instance_results})
                    )
                    f.close()
        return EvaluationResult(dataset, evaluation_details)

    def execute(self, code, context, agent, log_name=None) -> CheckResult:
        # self.execute调用agent.execute
        # 返回result
        result = agent.execute(code, context, log_name)
        if result.status is False:
            return CheckResult(
                answer=False, aspect="code execution", rationale=result.error_msg
            )
        # context再多一个"svg_string"
        context["svg_string"] = result.svg_string
        return CheckResult(
            answer=True,
            aspect="code execution",
            rationale="Code executed successfully.",
        )

    # surface_form_check只查code字符串里有没有plt.show()
    
    def surface_form_check(self, code) -> CheckResult:
        if "plt.show()" not in code:
            return CheckResult(
                answer=False,
                aspect="surface-form check",
                rationale="Did not plot visualization.",
            )
        else:
            return CheckResult(
                answer=True,
                aspect="surface-form check",
                rationale="Plotted visualization.",
            )

    def validity_check(self, code, context, agent, log_name=None) -> list[CheckResult]:
        results = []
        # 调用self.execute，是否能生成
        result = self.execute(code, context, agent, log_name)
        results.append(result)
        if result.answer:
            result = self.surface_form_check(code)
            results.append(result)

        return results

    def deconstruction(self, context) -> CheckResult:
        svg_string = context["svg_string"]
        library = context["library"]
        if library == "seaborn":
            library = "matplotlib"
        try:
            # 使用deconstruct.py 提取信息
            chart_info, msg = deconstruct(svg_string, library)
            if chart_info is None:
                return CheckResult(
                    answer=False,
                    aspect="deconstruction",
                    rationale=msg,
                )
            context.update(chart_info)
            return CheckResult(
                answer=True,
                aspect="deconstruction",
                rationale="Deconstructed the chart successfully.",
            )
        except:
            return CheckResult(
                answer=False,
                aspect="deconstruction",
                rationale="Cannot parse the visualization.",
            )

    def chart_type_check(self, context, ground_truth) -> CheckResult:
        answer, rationale = chart_check(
            context,
            ground_truth["chart"],
            (
                ground_truth["meta_info"]["stacked_bar"]
                if "stacked_bar" in ground_truth["meta_info"]
                else None
            ),
        )
        return CheckResult(
            answer=answer,
            aspect="chart type check",
            rationale=rationale,
        )

    def data_check(self, context, ground_truth) -> CheckResult:
        answer, rationale = data_check(
            context,
            ground_truth["vis_obj"],
            ground_truth["meta_info"]["channel_specified"],
        )
        return CheckResult(
            answer=answer,
            aspect="data check",
            rationale=rationale,
        )

    def order_check(self, context, ground_truth) -> CheckResult:
        # answer是bool, rationale是string "Doesn't sort."
        # 调用order_check.py
        answer, rationale = order_check(
            context,
            # 其实就是instance["vis_obj"]
            ground_truth["vis_obj"],
            (
                # 其实是instance["query_meta"][index]
                ground_truth["meta_info"]["sort_by"]
                if "sort_by" in ground_truth["meta_info"]
                else None
            ),
        )
        return CheckResult(
            answer=answer,
            aspect="order check",
            rationale=rationale,
        )

    def legality_check(self, context, ground_truth) -> list[CheckResult]:
        results = []
        result = self.deconstruction(context)
        results.append(result)
        if result.answer:
            chart_type_check_result = self.chart_type_check(context, ground_truth)
            data_check_result = self.data_check(context, ground_truth)
            results.append(chart_type_check_result)
            results.append(data_check_result)
            if data_check_result.answer and ground_truth["vis_obj"]["sort"] is not None:
                # 调用self.order_check
                self.order_check(context, ground_truth)
                results.append(self.order_check(context, ground_truth))

        return results

    def layout_check(self, context) -> CheckResult:
        assert "svg_string" in context
        assert self.webdriver_path is not None

        answer, rationale = layout_check(context, self.webdriver_path)
        return CheckResult(
            answer=answer,
            aspect="layout check",
            rationale=rationale,
        )

    def scale_and_ticks_check(self, context, query) -> CheckResult:
        assert "base64" in context and "encoding" in context and "chart" in context
        assert self.vision_model is not None

        answer, rationale = scale_and_ticks_check(context, query, self.vision_model)
        return CheckResult(
            answer=answer,
            aspect="scale and ticks check",
            rationale=rationale,
        )

    # include layout_check and scale_and_ticks_check
    def readability_evaluate(self, context, query: str) -> list[CheckResult]:
        results = []
        if self.webdriver_path:
            layout_result = self.layout_check(context)
            if layout_result.answer is not None:
                results.append(layout_result)

        if self.vision_model:
            context["base64"] = convert_svg_to_base64(context["svg_string"])
            scale_and_ticks_result = self.scale_and_ticks_check(context, query)
            if scale_and_ticks_result.answer is not None:
                results.append(scale_and_ticks_result)

            aspect_format = {
                "layout check": "Overflow/Overlap",
                "scale and ticks check": "Scale/Ticks",
            }
            reviews = [
                {
                    "aspect": aspect_format[result.aspect],
                    "content": result.rationale,
                }
                for result in results
            ]
            context["reviews"] = reviews

            answer, rationale = readability_check(context, query, self.vision_model)
            if answer is not None:
                readability_result = CheckResult(
                    answer=answer,
                    aspect="readability check",
                    rationale=rationale,
                )
                results.append(readability_result)

        return results
