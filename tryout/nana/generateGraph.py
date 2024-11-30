import pandas as pd
import matplotlib.pyplot as plt

#read file
df = pd.read_csv(r'../../github/capstone/project/EnhancedChat2VIS\src\uploaded_files/movies.csv')
print(df.head())

plt.figure(figsize=(10, 6))
#read tile file
plt.scatter(df['Worldwide Gross'], df['IMDB Rating'], color='blue', alpha=0.7)

plt.title('Worldwide Gross vs IMDB Rating', fontsize=16)

plt.xlabel('Worldwide Gross', fontsize=14)
plt.ylabel('IMDB Rating', fontsize=14)
#generate
plt.grid()
plt.show()
