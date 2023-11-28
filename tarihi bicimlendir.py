from pandas import DataFrame
from os.path import join, exists
from os import makedirs, listdir
import pandas as pd
import numpy as np
from datetime import date, datetime, timedelta

root_dir = r"D:\calisma\projeler\tripadvisor\data"

file_yorum = r"Istanbul Otel Yorumlari_HAM.feather"
file_yorum_duzgun_tarih = r"Istanbul Otel Yorumlari_tarih_bicimlenmis.feather"
file_yorum_duzgun_tarih_excel = r"Istanbul Otel Yorumlari_tarih_bicimlenmis.xlsx"

file_pandemi_oncesi = r"Istanbul Otel Yorumlari_Pandemi_Oncesi.feather"
file_pandemi_sonrasi = r"Istanbul Otel Yorumlari_Pandemi_Sonrasi.feather"

file_pandemi_oncesi_excel = r"Istanbul Otel Yorumlari_Pandemi_Oncesi.xlsx"
file_pandemi_sonrasi_excel = r"Istanbul Otel Yorumlari_Pandemi_Sonrasi.xlsx"

yorumlar = pd.read_feather(file_yorum)

""" SÜTUNLAR
"Index(['HotelID', 'UserID', 'ReviewID', 'UserRegion', 'ReviewDate',
      'UserRating', 'Title', 'Text', 'StayDate', 'Contribution', 'TripType',
      'UDS_Location', 'UDS_Cleanliness', 'UDS_Service', 'HelpfulVotes',
      'UDS_Sleep Quality', 'UDS_Rooms', 'UDS_Value', 'ResponseDate',
      'ResponseHeader', 'ResponseText',
      'UDS_Business service (e.g., internet access)',
      'UDS_Check in / front desk', 'Image_1', 'Image_2', 'Image_3'],
     dtype='object')
"""

def parse_date(text, reference_date=date(2021,10,31)):
    tarih = None
    if text is None:
        return None

    elif 'weeks ago' in text :
        week = int(text.split('weeks ago')[0].strip())
        tarih = reference_date - timedelta(weeks=week)

    elif 'week ago' in text :
        week = int(text.split('week ago')[0].strip())
        tarih = reference_date - timedelta(weeks=week)

    elif 'days ago' in text:
        day = int(text.split('days ago')[0].strip())
        tarih = reference_date - timedelta(days=day)

    elif 'day ago' in text:
        day = int(text.split('day ago')[0].strip())
        tarih = reference_date - timedelta(days=day)

    elif 'yesterday' == text.lower():
        day = 1
        tarih = reference_date - timedelta(days=day)

    elif 'today' == text.lower():
        tarih = reference_date

    # tarih ay ve gün olarak verilmiş olabiliyor; 'Oct 3' gibi.
    elif len(text.split(' ', )) == 2 and  int(text.split(' ', )[-1]) < 32:
        month, day = text.split(' ', )
        tarih = datetime.strptime(day + ' ' + month + ' 2021', '%d %b %Y')

    # 'week 1 ago' gibi
    elif len(text.split(' ', )) == 3 and ' ago' in text:
        day_or_week, num, ago = text.split(' ', )

        if day_or_week == 'week':
            tarih = reference_date - timedelta(weeks=day_or_week)

        elif day_or_week == 'day':
            tarih = reference_date - timedelta(days=day_or_week)
        else:
            print('metin çözümlenemedi: ', text)
            return None

    # tarih ay ve gün olarak verilmiş olabiliyor; 'Oct 3' gibi.
    elif len(text.split(' ', )) == 3 :
        month, day, year = text.split(' ', )
        day = day.replace(',', '')
        tarih = datetime.strptime(day + ' ' + month + ' ' + year, '%d %b %Y')

    else:
        tarih = datetime.strptime(text, '%b %Y')

    # print(tarih)
    return tarih

# Kalma tarihini DateTime yap
yorumlar.StayDate  = pd.to_datetime(yorumlar.StayDate,  )
yorumlar.ReviewDate = yorumlar.ReviewDate.apply(parse_date)
yorumlar.ResponseDate = yorumlar.ResponseDate.apply(parse_date)

# yorum tarihinde ne tür tarih şekilleri var?
# yorumlar.ReviewDate.str.split(' ', expand=True).iloc[:,-1].unique()
# print(yorumlar[yorumlar['ResponseDate'].isnull() ].count)

yorumlar.to_feather(file_yorum_duzgun_tarih)
yorumlar.to_excel(file_yorum_duzgun_tarih_excel)

pando = yorumlar[yorumlar.StayDate.between('2018-01-01', '2019-10-31', inclusive='both')]
pands = yorumlar[yorumlar.StayDate.between('2020-01-01', '2021-10-31', inclusive='both')]

pando.to_excel(file_pandemi_oncesi_excel)
pando.reset_index(inplace=True, drop=True)
pando.to_feather(file_pandemi_oncesi)

pands.to_excel(file_pandemi_sonrasi_excel)
pands.reset_index(inplace=True, drop=True)
pands.to_feather(file_pandemi_sonrasi)



yorumlar.ResponseDate  = pd.to_datetime(yorumlar.ResponseDate,  )

