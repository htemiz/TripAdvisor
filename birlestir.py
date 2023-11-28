from pandas import DataFrame
from os.path import join, exists
from os import makedirs, listdir, getcwd
import pandas as pd
import numpy as np




file_hotel_1 = r"D:\calisma\projeler\tripadvisor\data\Istanbul Otelleri\otel_bilgileri.feather"
file_hotel_2 = r"D:\calisma\projeler\tripadvisor\data\Istanbul Otelleri\otel_bilgileri_01.feather"

file_yorum_1 = r"D:\calisma\projeler\tripadvisor\data\Istanbul Otelleri\yorum_bilgileri.feather"
file_yorum_2 = r"D:\calisma\projeler\tripadvisor\data\Istanbul Otelleri\yorum_bilgileri_01.feather"

df_hotel_1 = pd.read_feather(file_hotel_1)
df_hotel_2 = pd.read_feather(file_hotel_2)

df_yorum_1 = pd.read_feather(file_yorum_1)
df_yorum_2 = pd.read_feather(file_yorum_2)

df_hotel = pd.concat([df_hotel_1, df_hotel_2])
df_hotel = df_hotel.drop_duplicates(subset=['HotelID'], ignore_index=True)


df_yorum = pd.concat([df_yorum_1, df_yorum_2])
df_yorum = df_yorum.sort_values('ReviewID').drop_duplicates(subset='ReviewID',
                                                 ignore_index=True, keep='last')


df_hotel.reset_index(inplace=True, drop=True)
df_hotel.to_feather( join(getcwd(), r"Istanbul Otel Bilgileri.feather"))

df_yorum.reset_index(inplace=True, drop=True)
df_yorum.to_feather(join(getcwd(), "Istanbul Otel Yorumlari.feather"))

df_hotel.to_excel(join(getcwd(), r"Istanbul Otel Bilgileri.xlsx"), engine='xlsxwriter')
df_yorum.to_excel(join(getcwd(), r"Istanbul Otel Yorumlari.xlsx"), engine='xlsxwriter')


