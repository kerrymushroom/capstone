import google.generativeai as genai
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 配置 Gemini API 密钥

genai.configure(api_key="AIzaSyCLXMk4PNMrGXu3ltiB930Y2bq4h0gE6OY")


# 定义 run_request 函数来调用 Gemini 模型
def run_request(question_to_ask, model_type, key, alt_key):
    try:
        # 输出 API 密钥以检查是否正确
        print(f"Using Gemini API Key: {key}")

        # 配置并调用 Gemini 模型
        genai.api_key = key
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content("It's a test, say hello")
        print(response.text)

        # 提取内容
        llm_response = response['content']

        # 输出生成的代码
        print(f"Generated code: {llm_response}")

        return llm_response
    except Exception as e:
        # 捕捉并输出 API 请求中的错误信息
        print(f"Error during API request: {e}")


# 定义获取数据集的描述信息函数
def get_primer(df_dataset, df_name):
    primer_desc = "Use a dataframe called df from data_file.csv with columns '" \
                  + "','".join(str(x) for x in df_dataset.columns) + "'. "
    for i in df_dataset.columns:
        if len(df_dataset[i].drop_duplicates()) < 20 and df_dataset.dtypes[i] == "O":
            primer_desc += f"\nThe column '{i}' has categorical values '" \
                           + "','".join(str(x) for x in df_dataset[i].drop_duplicates()) + "'. "
        elif df_dataset.dtypes[i] in ["int64", "float64"]:
            primer_desc += f"\nThe column '{i}' is of type {df_dataset.dtypes[i]} and contains numeric values. "
    primer_desc += "\nLabel the x and y axes appropriately."
    primer_desc += "\nAdd a title. Set the fig suptitle as empty."
    primer_desc += "{}"  # 空间留给其他的额外指示
    primer_desc += "\nUsing Python version 3.9.12, create a script using the dataframe df to graph the following: "

    primer_code = "import pandas as pd\nimport matplotlib.pyplot as plt\n"
    primer_code += "fig,ax = plt.subplots(1,1,figsize=(10,4))\n"
    primer_code += "ax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False)\n"
    primer_code += f"df={df_name}.copy()\n"
    return primer_desc, primer_code


# 定义格式化问题的函数
def format_question(primer_desc, primer_code, question, model_type):
    instructions = ""
    if model_type == "Code Llama":
        instructions = "\nDo not use the 'c' argument in the plot function, use 'color' instead."
    primer_desc = primer_desc.format(instructions)
    return f'"""\n{primer_desc}{question}\n"""\n{primer_code}'


# 定义 Streamlit 界面
st.title("自然语言生成可视化 - 使用 Gemini 和 Streamlit")

# 输入 Gemini API 密钥
gemini_key = st.text_input("输入你的 Gemini API 密钥", type="password", key="gemini_key_input")

# 用户输入自然语言查询
user_query = st.text_area("请输入你想生成的可视化描述", "例如：显示过去5年每月收入的折线图", key="user_query")

# 模型选择
selected_models = ["Gemini-1.5"]  # 目前为单一模型
available_models = {"Gemini-1.5": "gemini-1.5-flash"}  # 模型映射
model_count = len(selected_models)

# 加载示例数据集
if "datasets" not in st.session_state:
    datasets = {}
    datasets["Movies"] = pd.read_csv("https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/movies.csv")
    datasets["Housing"] = pd.read_csv("https://raw.githubusercontent.com/frog-land/Chat2VIS_Streamlit/main/housing.csv")
    st.session_state["datasets"] = datasets
else:
    datasets = st.session_state["datasets"]

# 数据集选择
chosen_dataset = st.selectbox("选择一个数据集", list(datasets.keys()), key="chosen_dataset")  # 让用户选择数据集

# 生成可视化按钮
if st.button("生成可视化", key="generate_button"):
    if not gemini_key:
        st.error("请提供有效的 Gemini API 密钥")
    else:
        try:
            api_keys_entered = True

            # 确保 API 密钥已经输入
            if "Gemini-1.5" in selected_models:
                if not gemini_key:
                    st.error("Please enter a valid Gemini API key.")
                    api_keys_entered = False

            if api_keys_entered:
                # 动态生成列数，显示多个模型结果
                plots = st.columns(model_count)

                # 获取数据集的 primer1 和 primer2
                primer1, primer2 = get_primer(datasets[chosen_dataset], 'datasets["' + chosen_dataset + '"]')

                # 针对每个选定的模型生成可视化
                for plot_num, model_type in enumerate(selected_models):
                    with plots[plot_num]:
                        st.subheader(model_type)
                        try:
                            # 格式化问题
                            question_to_ask = format_question(primer1, primer2, user_query, model_type)
                            # 调用模型生成答案
                            answer = run_request(question_to_ask, available_models[model_type], key=gemini_key,
                                                 alt_key=None)
                            # 将生成的 Python 代码加到 primer2 之后
                            answer = primer2 + answer
                            print("Model: " + model_type)
                            print(answer)
                            # 创建空的图表区域并执行生成的 Python 代码
                            plot_area = st.empty()
                            exec(answer)
                        except Exception as e:
                            st.error(f"执行模型 {model_type} 时出错: {e}")
        except Exception as e:
            st.error(f"调用 Gemini 模型失败: {e}")

# 示例代码生成后的可视化
st.write("下面是一个生成的示例图表：")

# 使用随机数据生成折线图
data = pd.DataFrame(np.random.randn(50, 3), columns=['A', 'B', 'C'])
st.line_chart(data)
