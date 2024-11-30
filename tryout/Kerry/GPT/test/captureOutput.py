import io
import sys

# 创建一个 StringIO 对象来捕获输出
output_buffer = io.StringIO()

# 重定向标准输出到 StringIO 对象
sys.stdout = output_buffer

# 示例代码段，其中包含 print()
print("This is the answer!")
answer = 42
print(f"The answer is: {answer}")

# 重置标准输出
sys.stdout = sys.__stdout__

# 获取捕获的输出内容
captured_output = output_buffer.getvalue()

# 输出捕获的内容
print("Captured Output:")
print(captured_output)

# 如果需要将捕获的输出存储到变量中
stored_output = captured_output