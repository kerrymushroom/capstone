from yolopandas import pd
from IPython.display import display
import matplotlib.pyplot as plt

product_df = pd.DataFrame(
    [
        {"name": "The Da Vinci Code", "type": "book", "price": 15, "quantity": 300, "rating": 4},
        {"name": "Jurassic Park", "type": "book", "price": 12, "quantity": 400, "rating": 4.5},
        {"name": "Jurassic Park", "type": "film", "price": 8, "quantity": 6, "rating": 5},
        {"name": "Matilda", "type": "book", "price": 5, "quantity": 80, "rating": 4},
        {"name": "Clockwork Orange", "type": None, "price": None, "quantity": 20, "rating": 4},
        {"name": "Walden", "type": None, "price": None, "quantity": 100, "rating": 4.5},
    ],
)

result = product_df.llm.query("Group by type and take the mean of all numeric columns.", yolo=True).llm.query("Make a bar plot of the result and use a log scale.", yolo=True)
# print("result========")
# print(result)
# result = product_df.llm.query("Group by type and take the mean of all numeric columns.Make a bar plot of the result and use a log scale.", yolo=True)

