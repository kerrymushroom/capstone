import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('./visEval_dataset/databases/behavior_monitoring/Student_Addresses.csv')
df['date_address_from'] = pd.to_datetime(df['date_address_from'])
df['year'] = df['date_address_from'].dt.year

df_grouped = df.groupby(['year', 'other_details']).size().unstack(fill_value=0)

fig, ax = plt.subplots(figsize=(10, 4))
df_grouped.plot(kind='bar', stacked=True, ax=ax)

ax.set_xlabel('Year')
ax.set_ylabel('Count of Address Changes')
ax.set_title('Distribution of Address Changes Over Time by Type')

plt.suptitle('')
ax.xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=0)

plt.show()