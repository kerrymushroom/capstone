import matplotlib.pyplot as plt
from yolopandas import pd
# A. Case Study 1: Department Store Dataset
product_df = pd.read_csv("/Users/subring/capstone/project/EnhancedChat2VIS/data/department_store.csv")
result = product_df.llm.query("What is the highest price of product, grouped by product type? Show a bar chart, and display by the names in desc.", yolo=True)
# result = product_df.llm.query("What is the highest price of product, grouped by product type? Return in DataFrame format", yolo=True).llm.query("Show a bar chart, and display by the names in desc.", yolo=True)

# result = product_df.llm.query("What is the highest price of product, grouped by product type? Return in DataFrame format", yolo=True)
# if isinstance(result, pd.Series):
#     result = result.to_frame()

# print(type(result))
# result1 = result.llm.query("Show a bar chart, and display by the names in desc.", yolo=True)

# result = product_df.llm.query("what is the average price of each product type", yolo=True)
# result.plot(kind='bar')
# plt.xlabel('Product Type')
# plt.ylabel('Max Price')
# plt.title('Maximum Price by Product Type')
plt.show()
