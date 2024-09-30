import os
from yolopandas import pd
import matplotlib.pyplot as plt
from yolopandas.utils.query_helpers import run_query_with_cost

# api_key=os.environ.get("OPENAI_API_KEY")

product_df = pd.read_csv("/Users/subring/capstone/project/EnhancedChat2VIS/data/customers_and_products_contacts.csv")
# myPrompt = product_reviews.llm.query("What item is the least expensive?", yolo=False)
# myPrompt = product_df.llm.query("Group by type and take the mean of all numeric columns.", yolo=False)
myPrompt = run_query_with_cost(product_df, "What item is the least expensive?", yolo=False)

print("myPrompt===========")
print(myPrompt)