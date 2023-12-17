
from config import configuration
from config.update import update_config
from sys import argv
from hotels.reviews import *
from hotels.parse import get_hotel_information
from hotels.reviews import parse_reviews
from utils.utils import get_browser, write_last_index, write_or_append_data
import pandas as pd
from time import sleep
from os.path import abspath
import gc

width, height = configuration['width'], configuration['height']
file_type = configuration['file_type']

chromedriver_path = "crawler/chromedriver.exe"

"""
    sehir_ve_ID = {"London":186338, "NewYork":60763, "Paris":187147, "Tokyo":298184, "Beijing":294212,
                   "Istanbul": 293974, "Belek": 312725, 'Girit': 189413,
                   "Mayorka": 187462, 'Antalya': 297962}

    sehir_ve_ID['London']

    sehirler =('London', 'NewYork', 'Paris', 'Tokyo', 'Beijing')
    sehirler =('Antalya',)
    
    r"D:\calisma\projeler\tripadvisor\data\Antalya\Antalya_oteller.csv"
"""

def main(data, region_name, download_dir ):

    url_root = "https://www.tripadvisor.com.tr/Hotel_Review-g"

    if download_dir is None:
        download_dir = abspath(join("../data/", region_name))
    else:
        download_dir = abspath(join(download_dir, region_name))

    file_hotel = join(download_dir, region_name + "_hotel_information." + file_type)
    file_yorum = join(download_dir, region_name + "_hotel_reviews." + file_type)

    first = True
    df_review = df_hotel = None
    n_periyot = 1

    ntotal= len(data)
    # last_index = hotelIDs.index(kalinan) # kalinan index
    last_index = configuration['last_index']

    for count in range(last_index, len(data)):#[hotelIDs[x] for x in [1,38, 39]]:
        # id= 507978# 507977
        print('Hotel Index: #%d/%d' % (count, ntotal), end=' ')

        region_id, hotel_id = data.loc[count,['RegionID', 'HotelID']]
        url = url_root + str(region_id) + "-d" + str(hotel_id)
        driver = get_browser(chromedriver_path, download_dir)
        driver.set_window_size(width, height)
        open_page(driver, url)

        n_try_captcha = 1
        while captcha_asked(driver) and n_try_captcha <3:
            sleep_a_while(sleep_min * n_try_captcha *10, sleep_max * n_try_captcha *10)
            open_page(driver, url)

        hotel_data = get_hotel_information(region_id, hotel_id, driver,)
        # bazen insan olduğumuz doğrulanmak isteniyor. Aradığımız sayfa yerine
        # başka bir sayfa açıldığından, yeni browser ile yeniden deniyoruz
        if hotel_data is None:
            sleep(5.5)
            driver = get_browser(chromedriver_path, download_dir)
            driver.set_window_size(width, height)
            open_page(driver, url)
            hotel_data = get_hotel_information(region_id, hotel_id, driver,)

        #hotel_data None ise, bu id de bir otel yok demektir. sonraki otele eç
        if hotel_data is None:
            print("Bu ID'ye (", str(id), ") sahip bir otel yok! Geçiliyor...\n")
            sleep(.2)
            update_config(file_path='config/configuration.json', path=["last_index"],
                          new_value=count + 1)  # count + 1, to start with next hotel in next time
            # write_last_index(count +1, file_last_index) # count + 1, to start with next hotel in next time
            continue

        reviews = parse_reviews(driver, hotel_id,)
        if reviews is None: # diller divini alırken bir hata ile karşılaşıldı. Tekrar deneyelim
            open_page(driver, url)
            hosgeldiniz_penceresini_kapat(driver)
            click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
            click_accept_button(driver)
            reviews = parse_reviews(driver, hotel_id,)

        sleep(.5)

        if first:
            df_hotel = pd.DataFrame.from_records(hotel_data, columns=hotel_data.keys(), index=[0])
            if reviews is not None:
                df_review = reviews
            first = False
        else:
            df_hotel = df_hotel.append( hotel_data, ignore_index=True)
            if reviews is not None:
                if df_review is not None:
                    df_review = pd.concat([df_review, reviews], ignore_index=True, sort=False)
                else:
                    df_review = reviews

        if count % n_periyot == 0:  # her n_periyot adet otelde bir kayıt yap
            sleep(.5)
            write_or_append_data(df_hotel, file_hotel)
            write_or_append_data(df_review, file_yorum)
            first = True
            df_hotel = None
            df_review = None

            try:
                driver.close()
            except Exception as e:
                print('Browser kapatılırken şu hata ile karşılaşıldı:', e)

            gc.collect()

        update_config(file_path='config/configuration.json', path=["last_index"], new_value=count+1) # count + 1, to start with next hotel in next time
        sleep(.5)

    write_or_append_data(df_hotel, file_hotel)
    write_or_append_data(df_review, file_yorum)


if __name__ == '__main__':
    data_file =  argv[1]
    region_name = argv[2]
    if len(argv) ==4:
        download_dir = argv[3]
    else:
        download_dir = "../data/"
    fonksiyon = getattr(pd, "read_" + file_type)
    data = fonksiyon(data_file)
    data = data.drop_duplicates()
    main(data, region_name, download_dir )


