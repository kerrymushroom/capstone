import pandas as pd
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('./visEval_dataset/databases/sports_competition/competition.csv')

# 确保列的类型为类别类型
df['Competition_type'] = df['Competition_type'].astype('category')
df['Country'] = df['Country'].astype('category')

# 分组并计数，按 Competition_type 进行分组，再按 Country 展开
competition_counts = df.groupby(['Competition_type', 'Country']).size().unstack().fillna(0)

# 计算每个 Competition_type 的总数量，并降序排序
competition_counts['Total'] = competition_counts.sum(axis=1)
competition_counts = competition_counts.sort_values(by='Total', ascending=False).drop(columns='Total')

# 绘制图表
fig, ax = plt.subplots(figsize=(12, 6))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 生成普通柱状图（非堆叠），不同国家用颜色区分
competition_counts.plot(kind='bar', stacked=False, ax=ax)

# 设置轴标签和标题
ax.set_xlabel('Competition Type')
ax.set_ylabel('Number of Competitions')
ax.set_title('Total Number of Competitions by Type and Country (Descending Order)')
fig.suptitle('')

# 调整 X 轴标签旋转角度
plt.xticks(rotation=45)
plt.tight_layout()

# 显示图表
plt.show()