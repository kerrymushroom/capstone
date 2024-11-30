import warnings
import pandas as pd
from viseval.agent import Agent,ChartExecutionResult
from .utils import show_svg
from .chat2test import get_output
from .evaluate import Evaluator
import sys

#from .agent import Agent

# set your openai key
key = "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"
available_models = {"ChatGPT-4": "gpt-4o"}
selected_models = "ChatGPT-4"
model_type = selected_models

class Chat2vis(Agent):
    def __init__(self):
        pass

    def generate(self, nl_query: str, tables: list[str], config: dict):
        library = config["library"]
        if library == "seaborn":
            import_statements = "import seaborn as sns\n"
        else:
            import_statements = ""
        try:
            print("generate: "+tables[0])
            df_name = tables[0].replace('.csv','')
            code = get_output(df_name,nl_query,key,rules=None,example=None)
            context = {
                    "tables": tables,
                }
            return code, context
        except Exception:
            warnings.warn(str(sys.exc_info()))
        return None, None

    def execute(self, code: str, context: dict, log_name: str = None):
        tables = context["tables"]
        print("execute: "+tables[0])
        df_nvBenchEval = pd.read_csv(tables[0])
        global_env = {
            "df_nvBenchEval": df_nvBenchEval,
            "svg_string": None,
            "show_svg": show_svg,
            "svg_name": log_name,
        }
        code += "\nsvg_string = show_svg(plt, svg_name)"
        code += "\nplt.close()"
        try:
            print("execute code: \n"+code)
            exec(code, global_env)
            svg_string = global_env["svg_string"]
            return ChartExecutionResult(status=True, svg_string=svg_string)
        except Exception as exception_error:
            import traceback

            exception_info = traceback.format_exception_only(
                type(exception_error), exception_error
            )
            print(exception_info)
            return ChartExecutionResult(status=False, error_msg=exception_info)