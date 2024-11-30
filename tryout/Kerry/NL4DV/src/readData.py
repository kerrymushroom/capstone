import pandas as pd

file = "/Users/lixiangjun/Desktop/capstone/tryout/Kerry/NL4DV/resource/Output_Counts_for_NL4DV_Output.csv"

df = pd.read_csv(file)
#print("\'", end='')
print(','.join(df.iloc[:, 2].astype(str).tolist()), end='')
#print("\'")