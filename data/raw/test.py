import pandas as pd

df = pd.read_csv("data/raw/Final Dataset.xlsx - Sheet1.csv")
print(df.shape)
print(df["Patient Name"].nunique())
