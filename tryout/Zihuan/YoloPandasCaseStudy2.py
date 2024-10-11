import matplotlib.pyplot as plt
from yolopandas import pd

# B. Case Study 2: Colleges Dataset
product_df = pd.read_csv("/Users/subring/capstone/tryout/Zihuan/data/colleges.csv")
# result = product_df.llm.query("Show debt and earnings for Public and Private colleges.", yolo=True)
# result = product_df.llm.query("The median debt for Public and Private colleges. Return in DataFrame format.", yolo=True).llm.query("Show a chart.", yolo=True)
result = product_df.llm.query("Show debt and earnings for Public and Private colleges. Return in DataFrame format", yolo=True).llm.query("Show a chart.", yolo=True)
# print(type(result))
plt.show()
