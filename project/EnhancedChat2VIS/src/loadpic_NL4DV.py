import pandas as pd
from nl4dv import NL4DV


# NL4DV GPT mode
def use_nl4dv_3(url, api_key, query):
    print(url)
    processing_mode = "gpt"
    nl4dv_instance = NL4DV(data_url=url, processing_mode=processing_mode, gpt_api_key=api_key)

    # Execute the query
    output = nl4dv_instance.analyze_query(query)
    print(output)

    return output["visList"][0]["vlSpec"]


# NL4DV semantic-parsing mode
def use_nl4dv_2(url, query):
    processing_mode = "semantic-parsing"
    nl4dv_instance = NL4DV(data_url=url, processing_mode=processing_mode)

    # Execute the query
    output = nl4dv_instance.analyze_query(query)
    print(output)

    return output["visList"][0]["vlSpec"]
