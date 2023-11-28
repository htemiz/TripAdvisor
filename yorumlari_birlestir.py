import pandas
from pandas import DataFrame
from os.path import join, exists
from os import makedirs, listdir, getcwd
import pandas as pd
import numpy as np

data = pandas.DataFrame()

root = r"D:\calisma\projeler\tripadvisor\data\_indirilenler"

files = listdir(root)

files = [f for f in files if (("otel" in f) and (".feather" in f))]

for f  in files:
    print(f)
    tmp = pd.read_feather(join(root, f))

    data = pd.concat([data, tmp])



data.to_feather(join(root, "Otel_Bilgileri_Kasim_2023.feather"))

# Yorum ID'si iki ve daha fazla aynı olan kayıtlar
# dup = data.groupby('ReviewID').filter(lambda x: len(x) >=2)


file_hotel_1 = r"D:\calisma\projeler\tripadvisor\data\Istanbul Otelleri\otel_bilgileri.feather"
