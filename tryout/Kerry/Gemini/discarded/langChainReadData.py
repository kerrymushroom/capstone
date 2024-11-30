# from langchain_community.document_loaders.csv_loader import CSVLoader
#
# import requests
# import tempfile
#
# # URL of the CSV file
#
# csv_url = "https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv"
#
# response = requests.get(csv_url)
# if response.status_code == 200:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
#         temp_file.write(response.content)
#         temp_file_path = temp_file.name
#
#
# loader = CSVLoader(file_path=temp_file_path)
# data = loader.load()
#
# for record in data[:2]:
#     print(record)
