import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./visEval_dataset/databases/behavior_monitoring/student_addresses.csv')
df['date_address_to'] = pd.to_datetime(df['date_address_to'])
df['month'] = df['date_address_to'].dt.to_period('M')
grouped = df.groupby(['month', 'other_details'])['monthly_rental'].mean().unstack()

fig, ax = plt.subplots(1, 1, figsize=(10, 4))
grouped.plot(kind='bar', ax=ax)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlabel('Month')
ax.set_ylabel('Average Monthly Rental')
ax.set_title('Average Monthly Rental Comparison by Property Type')
plt.suptitle('')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()