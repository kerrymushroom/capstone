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

# result = product_df.llm.query("Now show me all products that are books.", yolo=True)
# result = product_df.llm.query("Split the dataframe into two, 1/3 in one, 2/3 in the other.")
result = product_df.llm.query("Draw a bar chart to show the price of each book", yolo=True)

# result = product_df.llm.query("What item is the least expensive?")
# result = product_df.llm.query("What columns are missing values?")
print("result========")
print(result)

