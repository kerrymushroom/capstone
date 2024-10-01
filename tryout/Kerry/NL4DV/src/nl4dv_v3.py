import pandas as pd
from nl4dv import NL4DV

# def toPic():

# Your dataset must be hosted on GitHub for the LLM-based mode to function.
data_url = "../resource/cars.csv"
df = pd.read_csv(data_url)

# Choose your processing mode LLM or parsing. Choose "gpt" for the LLM-based mode or "semantic-parsing" for the
# rules-based mode.
processing_mode = "gpt"

# Enter your OpenAI key
gpt_api_key = "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"

# Initialize an instance of NL4DV
nl4dv_instance = NL4DV(processing_mode=processing_mode, gpt_api_key=gpt_api_key)
nl4dv_instance.set_data(data_url=None, data_value=df)

# Define a query
query = "show average MPG of different Origin"

# Execute the query
output = nl4dv_instance.analyze_query(query)

# Print the output
print(str(output))
    # return output["visList"][0]["vlSpec"]
