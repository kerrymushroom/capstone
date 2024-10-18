import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Hardcoded data representing chart types, hardness levels, and true ratios
data = {
    'chart_type': ['Bar', 'Bar', 'Bar', 'Bar', 'Grouping Line', 'Grouping Line', 'Grouping Line', 'Grouping Scatter',
                   'Grouping Scatter', 'Grouping Scatter', 'Line', 'Line', 'Line', 'Line', 'Pie', 'Pie', 'Pie', 'Pie',
                   'Scatter', 'Scatter', 'Scatter', 'Scatter', 'Stacked Bar', 'Stacked Bar', 'Stacked Bar',
                   'Stacked Bar'],
    'hardness': ['Easy', 'Extra Hard', 'Hard', 'Medium', 'Extra Hard', 'Hard', 'Medium', 'Easy', 'Hard', 'Medium',
                 'Easy', 'Extra Hard', 'Hard', 'Medium', 'Easy', 'Extra Hard', 'Hard', 'Medium', 'Easy', 'Extra Hard',
                 'Hard', 'Medium', 'Easy', 'Extra Hard', 'Hard', 'Medium'],
    'True': [0.6238425925925926, 0.6401225114854517, 0.5647935779816514, 0.6610544971200709, 0.3777777777777777,
             0.6153846153846154, 1.0, 0.6417910447761194, 0, 0.8793103448275862, 0.6538461538461539,
             0.7796610169491526, 0.6623376623376623, 0.6626506024096386, 0.1924528301886792, 0.1176470588235294,
             0.0925925925925925, 0.1147540983606557, 0.8509316770186336, 0.9090909090909092, 0.7857142857142857, 0.7375,
             1.0, 0.3684210526315789, 0.8496732026143791, 0.981132075471698
             ]
}

# Create a DataFrame from the hardcoded data
df = pd.DataFrame(data)

# Convert 'True' values to percentages
df['True'] = df['True'] * 100

# Sort the data by chart_type and hardness levels in the desired order
hardness_order = ['Easy', 'Medium', 'Hard', 'Extra Hard']
df['hardness'] = pd.Categorical(df['hardness'], categories=hardness_order, ordered=True)
df = df.sort_values(by=['chart_type', 'hardness'])

# Pivot the data for easy plotting
true_ratios = df.pivot(index='chart_type', columns='hardness', values='True')

# Set up the plot
fig, ax = plt.subplots(figsize=(16, 6))

# Get unique chart types and hardness levels
chart_types = df['chart_type'].unique()
hardness_levels = hardness_order

# Define custom colors for each hardness level
colors = ['#92D050', '#EED236', '#EE9F36', '#E6576A']

# Number of bars per cluster (one for each hardness level)
bar_width = 0.15  # Width of each bar
x = np.arange(len(chart_types))  # The label locations

# Plot bars for each hardness level with custom colors
for i, (hardness, color) in enumerate(zip(hardness_levels, colors)):
    bars = ax.bar(x + i * bar_width, true_ratios[hardness], bar_width, label=hardness, color=color)
    # Add labels above the bars for each bar with two decimal places
    for bar in bars:
        yval = bar.get_height()
        # Adjust the position of the text to prevent overlapping (shift each label vertically based on index)
        offset = (i - 1.5) * 3  # Adjusting label position by a small vertical shift
        ax.text(bar.get_x() + bar.get_width()/2, yval + offset, f'{yval:.2f}%', ha='center', va='bottom', fontsize=10)

# Add labels and title
ax.set_xlabel('Chart Type', fontsize=14)
ax.set_ylabel('True Ratio (%)', fontsize=14)
ax.set_title('Clustered Bar Plot of True Ratios by Chart Type and Hardness', fontsize=16)
ax.set_xticks(x + bar_width * (len(hardness_levels) - 1) / 2)
ax.set_xticklabels(chart_types, fontsize=12)
ax.legend(title='Hardness', fontsize=12)

# Show the plot
plt.tight_layout()
plt.show()