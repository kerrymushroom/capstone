import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

# Save the chart as a local image file
def save_fig_to_image(fig, file_path):
    fig.savefig(file_path, format='png', bbox_inches='tight', pad_inches=0.1)  # Save directly to file
    print(f"Chart saved as {file_path}")


# "1556":
# "evaluation": "X label overlapped"
df = pd.read_csv("/Users/subring/capstone/findRule/visEval_dataset/databases/hr_1/employees.csv")
df['HIRE_DATE'] = pd.to_datetime(df['HIRE_DATE'])
filtered_df = df[df['FIRST_NAME'].str.contains("D|S")]
sorted_df = filtered_df.sort_values('HIRE_DATE')
plt.plot(sorted_df['HIRE_DATE'], sorted_df['SALARY'])
plt.xlabel('Hire Date')
plt.ylabel('Salary')
plt.title('Salary Change Over Time for Employees with D or S in First Name')
plt.suptitle('')
# Gets the current figure object
fig = plt.gcf()

# "1835@x_name@ASC":
# "evaluation": "The x-axis data display is incomplete.",
# df = pd.read_csv('/Users/subring/capstone/findRule/visEval_dataset/databases/hr_1/employees.csv')
# df['HIRE_DATE'] = pd.to_datetime(df['HIRE_DATE'])
# filtered_df = df[~df['FIRST_NAME'].str.contains('M')]
# sorted_df = filtered_df.sort_values(by='HIRE_DATE')
# fig = plt.figure(figsize=(12,6)) # NameError: name 'fig' is not defined
# plt.plot(sorted_df['HIRE_DATE'], sorted_df['SALARY'], marker='o')
# plt.xlabel('Hire Date')
# plt.ylabel('Salary')
# plt.title('Salaries Over Hire Dates (Excluding First Names with \"M\")')
# plt.suptitle('')
# plt.grid(True)
# plt.tight_layout()


# Create a small size Figure: image_test.png
# The chart goes beyond the upper boundary, the chart goes beyond the lower boundary
# fig, ax = plt.subplots(figsize=(3, 2))  # Reduce the canvas size to make it easier to cross boundaries
# ax.plot([1, 2, 3], [4, 5, 6])
# ax.set_title("This is an extremely long title that will likely extend beyond the canvas boundaries", fontsize=20)
# ax.set_xlabel("This is a very long x-axis label that will go beyond the edge of the canvas", fontsize=15)
# ax.set_ylabel("This is a very long y-axis label that will go beyond the edge of the canvas", fontsize=15)

# "196":
# "evaluation": "X-axis label overflowed. Missing part of X-axis data (2018) because of \"ax.xaxis.set_major_locator(mdates.YearLocator())\"",
# df = pd.read_csv('/Users/subring/capstone/findRule/visEval_dataset/databases/behavior_monitoring/Student_Addresses.csv')
# df['date_address_from'] = pd.to_datetime(df['date_address_from'])
# df['year'] = df['date_address_from'].dt.year
# df_grouped = df.groupby(['year', 'other_details']).size().unstack(fill_value=0)
# fig, ax = plt.subplots(figsize=(10, 4))
# df_grouped.plot(kind='bar', stacked=True, ax=ax)
# ax.set_xlabel('Year')
# ax.set_ylabel('Count of Address Changes')
# ax.set_title('Distribution of Address Changes Over Time by Type')
# plt.suptitle('')
# ax.xaxis.set_major_locator(mdates.YearLocator())
# plt.xticks(rotation=45, ha='right')


# "225":
# "evaluation": "Wrong order of the weekdays; Rotated x-axis; X title overflow"
# df = pd.read_csv("/Users/subring/capstone/findRule/visEval_dataset/databases/behavior_monitoring/Student_Addresses.csv")
# df['date_address_from'] = pd.to_datetime(df['date_address_from'])
# df['weekday'] = df['date_address_from'].dt.day_name()
# avg_rental = df.groupby(['other_details', 'weekday'])['monthly_rental'].mean().unstack()
# fig, ax = plt.subplots(figsize=(10, 4))
# avg_rental.plot(kind='bar', ax=ax)
# ax.set_xlabel('Other Details')
# ax.set_ylabel('Average Monthly Rental')
# ax.set_title('Average Monthly Rental by Weekday and Other Details')
# fig.suptitle('')
# plt.xticks(rotation=45)
# plt.tight_layout()


# "3236@x_name@ASC":
# "evaluation": "Rotated x-axis; X title overflow"
# fig, ax = plt.subplots(1, 1, figsize=(10, 4))
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# df = pd.read_csv('/Users/subring/capstone/findRule/visEval_dataset/databases/wine_1/WINE.csv')
# filtered_df = df[df['Price'] > 100]
# winery_counts = filtered_df['Winery'].value_counts().sort_index()
# winery_counts.plot(kind='bar', ax=ax)
# ax.set_xlabel('Winery')
# ax.set_ylabel('Number of Wines')
# ax.set_title('Number of Wineries with Wines Priced Over $100')
# fig.suptitle('')
# plt.xticks(rotation=0)

# "1510@y_name@ASC":
# "evaluation": "Rotated x-axis; X title overflow"
# df = pd.read_csv('/Users/subring/capstone/findRule/visEval_dataset/databases/gas_company/company.csv')
# industry_counts = df[df['Main_Industry'] != 'Oil and gas']['Main_Industry'].value_counts().sort_values()
# fig, ax = plt.subplots(1, 1, figsize=(10, 4))
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# industry_counts.plot(kind='bar', ax=ax)
# ax.set_title('')
# ax.set_xlabel('Main Industry')
# ax.set_ylabel('Number of Companies')
# plt.title('Number of Companies without a Gas Station in Each Main Industry')



# Set the image file path
file_path = '/Users/subring/capstone/tryout/Zihuan/image_1556.png'

# Save the chart as a local file
save_fig_to_image(fig, file_path) # type: ignore

plt.show()