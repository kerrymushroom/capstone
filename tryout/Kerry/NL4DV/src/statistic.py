import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = {
    'chart_type': ['Bar', 'Bar', 'Bar', 'Bar', 'Grouping Line', 'Grouping Line', 'Grouping Line', 'Grouping Scatter',
                   'Grouping Scatter', 'Grouping Scatter', 'Line', 'Line', 'Line', 'Line', 'Pie', 'Pie', 'Pie', 'Pie',
                   'Scatter', 'Scatter', 'Scatter', 'Scatter', 'Stacked Bar', 'Stacked Bar', 'Stacked Bar',
                   'Stacked Bar'],
    'hardness': ['Easy', 'Extra Hard', 'Hard', 'Medium', 'Extra Hard', 'Hard', 'Medium', 'Easy', 'Hard', 'Medium',
                 'Easy', 'Extra Hard', 'Hard', 'Medium', 'Easy', 'Extra Hard', 'Hard', 'Medium', 'Easy', 'Extra Hard',
                 'Hard', 'Medium', 'Easy', 'Extra Hard', 'Hard', 'Medium'],
    'False': [325,235,759,765,28,10,0,24,2,7,27,13,26,56,214,15,49,162,24,1,3,21,0,96,23,1],
    'True': [539,418,985,1492,17,16,1,43,0,51,51,46,51,110,51,2,5,21,137,10,11,59,1,56,130,52]
}

df = pd.DataFrame(data)

df['Total'] = df['True'] + df['False']

pivot_df = df.pivot(index='chart_type', columns='hardness', values='Total')

pivot_df_filled = pivot_df.fillna(0)

plt.figure(figsize=(14, 8))
plt.imshow(pivot_df_filled, cmap='Blues', aspect='auto')

plt.xticks(np.arange(len(pivot_df_filled.columns)), pivot_df_filled.columns)
plt.yticks(np.arange(len(pivot_df_filled.index)), pivot_df_filled.index)
plt.colorbar(label='Number of Questions')

for i in range(pivot_df_filled.shape[0]):
    for j in range(pivot_df_filled.shape[1]):
        value = pivot_df_filled.iloc[i, j]
        color = 'white' if (
                    (i == 0 and j >= pivot_df_filled.shape[1] - 2)) else 'black'
        plt.text(j, i, f'{int(value)}', ha='center', va='center', color=color, fontsize=16)

plt.title('Number of Questions by Chart Type and Hardness')
plt.xlabel('Hardness')
plt.ylabel('Chart Type')

plt.tight_layout()
plt.show()
