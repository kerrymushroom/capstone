import matplotlib.pyplot as plt
from yolopandas import pd

# E. Case Study 5: Misspecified Prompts
product_df = pd.read_csv("/Users/subring/capstone/tryout/Zihuan/data/movies.csv")
# result = product_df.llm.query("draw the numbr of movie by gener. Return in DataFrame format.", yolo=True).llm.query("Show a chart", yolo=True)
result = product_df.llm.query("draw the numbr of movie by gener. Return in DataFrame format.", yolo=True).llm.query("Show a bar chart", yolo=True)

plt.show()
