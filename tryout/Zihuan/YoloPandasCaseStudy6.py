import matplotlib.pyplot as plt
from yolopandas import pd

# F. Case Study 6: Underspecified and Ambiguous Prompts
product_df = pd.read_csv("/Users/subring/capstone/tryout/Zihuan/data/movies.csv")

# result = product_df.llm.query("tomatoes. Return in DataFrame format.", yolo=True).llm.query("chart", yolo=True)
result = product_df.llm.query("tomatoes. Return in DataFrame format.", yolo=True).llm.query("Show a chart", yolo=True)
plt.show()
