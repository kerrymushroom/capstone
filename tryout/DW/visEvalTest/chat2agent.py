import warnings
import pandas as pd
from viseval.agent import Agent, ChartExecutionResult
from .utils import show_svg
from chat2test import get_output

# set your openai key
key = ""
available_models = {"ChatGPT-4": "gpt-4o"}
selected_models = "ChatGPT-4"
model_type = selected_models

class Chat2vis(Agent):
	def generate(self, nl_query: str, tables: list[str], config: dict):
		library = config["library"]

        if library == "seaborn":
            import_statements = "import seaborn as sns\n"
        else:
            import_statements = ""
        code = get_output(tables[0],nl_query,key,rules=None,example=None)
        context = {
                "tables": tables,
            }
            return code, context
        except Exception:
            warnings.warn(str(sys.exc_info()))
        return None, None

    def execute(self, code: str, context: dict, log_name: str = None):
        tables = context["tables"]
        df_nvBenchEval = pd.read_csv(tables[0])
        global_env = {
            "df_nvBenchEval": df_nvBenchEval,
            "svg_string": None,
            "show_svg": show_svg,
            "svg_name": log_name,
        }
        code += "\nsvg_string = show_svg(plt, svg_name)"
        try:
            exec(code, global_env)
            svg_string = global_env["svg_string"]
            return ChartExecutionResult(status=True, svg_string=svg_string)
        except Exception as exception_error:
            import traceback

            exception_info = traceback.format_exception_only(
                type(exception_error), exception_error
            )
            return ChartExecutionResult(status=False, error_msg=exception_info)