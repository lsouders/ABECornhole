import pandas as pd

results = pd.read_csv("RoundRobin.csv")

df = results[['Team Name', 'Points For', 'Points Against']]
print(df.head())