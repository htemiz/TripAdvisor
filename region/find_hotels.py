import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.utils import *
from os.path import abspath, join
from sys import argv
from hotels.helpers import get_region_id_and_name_from_url

"""
region_id = "28930"
region_name = 'Florida'
"""
def get_hotels_of_region(driver, region_id, region_name, download_dir, page='oa30', star=None, sleep_min=3, sleep_max=3 ):

    if download_dir is None:
        download_dir = abspath(join("../data/" + region_name))
    else:
        download_dir = abspath(join(download_dir + region_name))

    region_url = "https://www.tripadvisor.com.tr/Hotels-g" + region_id + "-"
    file_hotels = join(download_dir, "Hotels_in_" + region_name + "_Region.feather")
    file_last_index = join(download_dir, region_name + '_last_index.txt')

    # return
    driver.set_window_size(1200, 900)
    driver.get(region_url + page)
    print('Page: ', page[2:])

    while True:
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        click_accept_button(driver)
        click_and_press_esc(driver)

        try:
            btn_accept = driver.find_element_by_id('_evidon-accept-button')
            if btn_accept is not None:
                btn_accept.click()
        except:
            pass

        try:
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        except:
            pass

        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.TAG_NAME, 'body'))

        try:
            tum_icerik = driver.find_element(By.XPATH, "//span[text()='Tüm içerik']")
            if tum_icerik is not None:
                if tum_icerik is not None:
                    tum_icerik.find_element(By.XPATH,"../..").click() # ebeveynine tıkla
                    driver.execute_script("arguments[0].scrollIntoView();", tum_icerik)
        except:
            pass

        sleep_a_while(sleep_min=sleep_min/2, sleep_max=sleep_max/2)  # better to sleep a while
        # sayfada gösterilen otellere ait bilgiler bu div altında
        # div_oteller = driver.find_elements(By.CLASS_NAME, "NXAUb")
        div_oteller = driver.find_elements(By.XPATH, "//div[@data-automation='hotel-card-title']")
        alar =[div_oteller[x].find_element(By.XPATH, "a[contains(@href,'Hotel_Review-g')]") for x in range(len(div_oteller))]
        hotel_urls_and_name = [(x.get_attribute('href'), x.text.split('. ')[-1])  for x in alar]
        h = [{'RegionID':x, 'HotelID':y, 'HotelName':z} for (x, y, z) in
             (get_region_id_and_name_from_url(u) for u in hotel_urls_and_name)]
        df = pd.DataFrame()
        for x in h:
            df = pd.concat([df,pd.DataFrame.from_records(x, columns=x.keys(), index=[0] )] )

        write_or_append_data(df, file_hotels)

        try:
            btnNext = driver.find_element(By.XPATH,"//a[@aria-label='Next page']" )
            if btnNext is not None and 'disabled' not in btnNext.get_attribute('class'):
                # print("Sonraki sayfaya geçiliyor...")
                page = 'oa' + btnNext.get_attribute('href').split('-oa')[-1].split('-')[0]
                write_last_index(page, file_last_index)
                btnNext.click()
            else:
                print('Next Butonu Bulunamadı. Şu ana dek alınan bilgiler return ediliyor...')
                return pd.read_feather(file_hotels)

        except Exception as e:
            from selenium.common.exceptions import NoSuchElementException
            if NoSuchElementException == type(e):
                print('Tüm oteller gezildi.')
                return pd.read_feather(file_hotels)
            else:
                print('Beklenmeyen bir hata ile karşılaşıldı. Hata şuydu:\n', e)
                return None



if __name__ == "__main__":
    region_id, region_name  = argv[1], argv[2]
    if len(argv) ==4:
        download_dir = argv[3]
    else:
        download_dir = "../../data/"

    chromedriver_path = "../crawler/chromedriver.exe"
    driver = get_browser(chromedriver_path, download_dir)

    get_hotels_of_region(driver, region_id, region_name, download_dir, star=5,
                                   page='oa2850', sleep_min=4, sleep_max=5 )