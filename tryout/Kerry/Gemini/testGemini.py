import google.generativeai as genai
import pandas as pd
import tempfile
import os

genai.configure(api_key="AIzaSyCLXMk4PNMrGXu3ltiB930Y2bq4h0gE6OY")
# 读取 URL 的 CSV 文件到 DataFrame
originalCsv = pd.read_csv("https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/cars.csv")

# 将 DataFrame 转换为 CSV 并写入临时文件
with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
    originalCsv.to_csv(temp_file, index=False)
    temp_file.seek(0)  # 将文件指针移到开头
    temp_filename = temp_file.name  # 获取临时文件的文件名

# 打印临时文件的路径（可以在调试时查看）
print(f"临时文件的路径：{temp_filename}")


model = genai.GenerativeModel("gemini-1.5-flash")
uploadFile = genai.upload_file(temp_file.name)
response = model.generate_content(["Give me the vega chart code of average MPG by origin.", uploadFile])
print(response.text)