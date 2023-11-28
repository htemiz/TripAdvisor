from pandas import DataFrame
from os.path import join, exists
from os import makedirs, listdir
import pandas as pd


root_dir = r"D:\calisma\projeler\tripadvisor\download_albums"


files = listdir(root_dir) # all files in root folder
files = [join(root_dir, file) for file in files if file.endswith(".xlsx")] # Excel files only

first = True
for file in files:
    print(file)
    if first:
        df_all = pd.read_excel(file, usecols="B:E",)
        first= False
    else:
        df = pd.read_excel(file, usecols="B:E")
        df_all = df_all.append(df, ignore_index=True)

# df_all.to_excel(join(root_dir, "all_hotels.xlsx"), index=False)

df_all.to_feather(join(root_dir, "all_hotels.feather"))


