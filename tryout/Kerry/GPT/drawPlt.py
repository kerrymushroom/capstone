import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv("./visEval_dataset/databases/behavior_monitoring/Student_Addresses.csv")
df['date_address_to'] = pd.to_datetime(df['date_address_to'])
df['weekday'] = df['date_address_to'].dt.day_name()

grouped = df.groupby(['other_details', 'weekday'])['monthly_rental'].sum().unstack()
grouped = grouped.reindex(columns=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

ax = grouped.plot(kind='bar', stacked=False, figsize=(12, 6))
ax.set_xlabel('Other Details')
ax.set_ylabel('Sum of Monthly Rental')
ax.set_title('Sum of Monthly Rental by Weekday and Other Details')
plt.suptitle('')

plt.xticks(rotation=0)
plt.legend(title='Weekday')
plt.tight_layout()

plt.show()