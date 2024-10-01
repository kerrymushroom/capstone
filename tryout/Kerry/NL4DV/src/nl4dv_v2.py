from nl4dv import NL4DV
import os
import pandas as pd

data_url = "../resource/cars.csv"
df = pd.read_csv(data_url)

# Initialize an instance of NL4DV
nl4dv_instance = NL4DV(data_url=os.path.join("..", "resource", "cars.csv"))

# using Stanford Core NLP
dependency_parser_config = {"name": "corenlp", "model": os.path.join("..", "dependency","stanford-english-corenlp-2018-10-05-models.jar"),"parser": os.path.join("..", "dependency","stanford-parser.jar")}

# using Stanford CoreNLPServer
# dependency_parser_config = {"name": "corenlp-server", "url": "http://localhost:9000"}

# using Spacy
# dependency_parser_config = {"name": "spacy", "model": "en_core_web_sm", "parser": None}

# Set the Dependency Parser
nl4dv_instance.set_dependency_parser(config=dependency_parser_config)
nl4dv_instance.set_data(data_url=None, data_value=df)

# Define a query
query = "show average MPG of different Origin"

# Execute the query
output = nl4dv_instance.analyze_query(query)
print(output)
