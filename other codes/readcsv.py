
from os.path import abspath, basename, join, dirname, splitext, exists

from os import makedirs, listdir

import pandas as pd
import csv

file = r"D:\calisma\projeler\tripadvisor\data\enhepsi.csv"
xl_file = r"D:\calisma\projeler\tripadvisor\data\enhepsi.xlsx"

file = r"D:\calisma\projeler\tripadvisor\data\enhepsi_benim_excel_ile_yeniden_kaydettigim.csv"


with open(file, "r") as d:
    reader = csv.reader(d)
    a = reader.()


pd.read_csv(file, delimiter=",")

e = pd.read_excel(xl_file, usecols="A:J")
