
import pandas as pd

from utils.utils import *


region_id = "28930"
chromedriver_path = "crawler/chromedriver.exe"
download_dir = "../data/florida"
file_hotels = join(download_dir, "florida_hotels.feather")
oa = 'oa30'
region_url = "https://www.tripadvisor.com.tr/Hotels-g28930-"


def get_hotel_ids_with_next_button(region_id, star=None, driver=None,  sleep_min=3, sleep_max=3 ):
    global oa
    driver.set_window_size(1200, 900)
    driver.get(region_url + oa)
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

        save_data(df, None, file_hotels, None, root_folder=getcwd())

        btnNext = driver.find_element(By.XPATH,"//a[@aria-label='Next page']" )
        if btnNext is not None and 'disabled' not in btnNext.get_attribute('class'):
            # print("Sonraki sayfaya geçiliyor...")
            oa = 'oa' + btnNext.get_attribute('href').split('-oa')[-1].split('-')[0]
            write_last_index(oa, download_dir  )
            btnNext.click()
        else:
            break


if __name__ == "__main__":
    driver = get_browser(chromedriver_path, download_dir)
    get_hotel_ids_with_next_button(region_id, star=5, driver=driver,  sleep_min=6, sleep_max=7 )