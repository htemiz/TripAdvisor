import re
import codecs
from lxml import html
import requests
import csv
from typing import List, Any
from bs4 import BeautifulSoup
import urllib.request as request
from contextlib import closing
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.select import Select
import pandas as pd
from utils import *
import gc
from os.path import exists


def main():
    file = r"D:\calisma\projeler\tripadvisor\data\Beijing_oteller.csv"

    df = pd.read_csv(file, header=None)
    df = df.drop_duplicates(ignore_index=True)

    df.to_csv(file, index=False, header=None)

    file = r"D:\calisma\projeler\tripadvisor\data\Istanbul Otelleri\1\otel_bilgileri.feather"
    file = r"D:\calisma\projeler\tripadvisor\data\Istanbul Otelleri\1\yorum_bilgileri.feather"

    df = pd.read_feather(file)
    df = df.drop_duplicates(subset='HotelID')
    df.to_excel('yorum bilgileri.xlsx',  engine='xlsxwriter')

    df = df.drop_duplicates(subset='ReviewID', ignore_index=True,)

    df.to_feather(file)

    file = r"D:\istanbul yarim kalinan\otel_bilgileri.feather"

    df.to_excel('otel bilgileri.xlsx')


main()

if __name__ == '__main__':
    main()