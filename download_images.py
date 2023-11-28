import requests
from os.path import join, exists, basename, dirname
from os import makedirs, getcwd
import pandas as pd
from time import sleep


# df = pd.read_excel(xl_file, usecols="A:D")
# bathroom_images = df[df["Album"] == "Bathroom"]
# bathroom_images = bathroom_images['Url']
# df.to_feather(r"D:\calisma\projeler\tripadvisor\download_albums\all_hotels.feather")
# xl_file = r"D:\calisma\projeler\tripadvisor\download_albums\all_hotels.xlsx"
# url = "https://media-cdn.tripadvisor.com/media/oyster-panos/sources/beach--v197045.tiles/wide_700.jpg"
# url = 'https://dynamic-media-cdn.tripadvisor.com/media/photo-o/14/90/4f/6f/siyah-lekelere-dikkatli.jpg'



session = requests.session()

def prepare_url(url, width=500):
    if "photo-" in url:
        url = url + "?w=" + str(width)
    return url

def prepare_file_name(url, hotel_id="342355", album=None, user_name=None):
    if "photo-" in url:
        ll = url.split("photo-")[1][2:]
        ll = ll.replace("/", "#")

    elif "/oyster-panos/sources/" in url:
        ll = url.split("/oyster-panos/sources/")[1]
        ll = ll.replace("/", "#")
    else:
        raise Exception("URL parse edilemedi! URL:" + url)
        return None

    name = hotel_id + "_" + album if album is not None else hotel_id
    name = name + "_" + user_name if user_name is not None else name
    name += "_" + ll
    return name

def download( url, file_name, root_dir=None):
    global session
    try:
        img_data = session.get(url, timeout=25).content
    except requests.exceptions.Timeout as err:
        print(err)
        print("Resim indirilemedi! URL: ", url)
        print("Tekrar denenecek...")
        sleep(3.5)
        session = requests.session()

        try:
            img_data = session.get(url, timeout=15).content
        except requests.exceptions.Timeout as err:
            print("Tekrar denendi ama cevap alınamadaı! URL: ", url)
            sleep(1)
            session = requests.session()
            return


    file_name = join(root_dir, file_name) if root_dir is not None else file_name
    print("Kaydedilecek dosya adı: ", file_name + "\n")
    with open(file_name, 'wb') as handler:
        handler.write(img_data)


width=500

root_dir = r"D:\calisma\projeler\tripadvisor\data"
feather_file = r"D:\calisma\projeler\tripadvisor\data\Hotels_NoDup.feather"

Albums = ['Dining    ',
          'Family/Play Areas',
          'Hotel & Amenities',
          'Panoramas',
          'Pool & Beach',
          'Room/Suite',
          #'Bathroom',
          #'Traveler',
          ]

df = pd.read_feather(feather_file)
d = df[df["Album"] != "Bathroom"] # Bathroom dışındaki tüm albümler
d = d.dropna(subset=["Url"]) # URL'si boş olmayan kayıtlar
d = d[d['Album'].isin(Albums)]
d.sort_values("Album", inplace=True)

start = 0

for alb in Albums:

    dd = d[d['Album'] == alb]
    if dd.shape[0] >= 20_000:
        dd =dd.sample(n=20000, replace=False)

    print(start , ". kayıttan " , dd.shape[0], " a kadar indirecek")
    for i in range(start, dd.shape[0]):

        row = dd.iloc[i]
        hotel_id = str(row["Hotel ID"])
        album = row["Album"].strip()
        album = album.replace("/", "#")
        user_name = row['User Name']
        url = row['Url']

        file_name = prepare_file_name(url, hotel_id=hotel_id, album=album, user_name=user_name)

        if not exists(join(root_dir, album)):
            makedirs(join(root_dir, album))

        file_name = join(root_dir, album, file_name)
        url_downlad = prepare_url(url, width=width)

        print("index: " , i, ", " , url_downlad)
        download(url_downlad, file_name, )

        sleep(.7)

