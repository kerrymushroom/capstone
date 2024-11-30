import matplotlib.pyplot as plt
from yolopandas import pd

# D. Case Study 4: Customers and Products Contacts Dataset
product_df = pd.read_csv("/Users/subring/capstone/tryout/Zihuan/data/customers_and_products_contacts.csv")
result = product_df.llm.query("Show the number of products with price higher than 1000 or lower than 500 for each product name in a bar chart, and could you rank y-axis in descending order?", yolo=True)
# result = product_df.llm.query("show me the number of products with price higher than 1000 or lower than 500 for each product name. Return in DataFrame format", yolo=True).llm.query("Show a bar chart, and rank y-axis in descending order?", yolo=True)
# result = product_df.llm.query("show me the number of products with price higher than 1000 or lower than 500 for each product name. Return in DataFrame format", yolo=True).llm.query("Show a bar chart by ranking y-axis in descending order?", yolo=True)
plt.show()
