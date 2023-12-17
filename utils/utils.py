from config import configuration
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
import pyautogui as pgui
from os import getcwd
from os.path import join, exists, dirname
from os import makedirs
from numpy.random import random
import pandas as pd
from selenium.webdriver.common.by import By
import gc
from selenium.webdriver.common.keys import Keys

sleep_min = configuration['sleep_min']
sleep_max = configuration['sleep_max']
slp_factor = 1
wait_time = configuration['wait_time']
slp_small_factor = .5


def click_accept_button(driver):

    try:
        #btn_accept = driver.find_element_by_id( 'onetrust-accept-btn-handler')
        btn_accept = driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")

        if btn_accept is not None:
            btn_accept.click()
    except Exception as e:
        pass


def click_and_press_esc(driver):
    try:
        btn_accept = driver.find_element(By.ID, '_evidon-accept-button')
        if btn_accept is not None:
            btn_accept.click()
    except:
        pass
    try:
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    except:
        pass

def find_next_button(driver):
    try:
        btnNext = driver.find_element(By.XPATH, '//div[@data-trackingstring="pagination_h"]//a[text()="Next"]')
    except:
        return None
    return btnNext


def makine_cevirisini_kapat(driver):
    try:
        Hayir_Butonu = driver.find_element(By.ID, 'autoTranslateNo')
        if Hayir_Butonu is not None:
            try:
                Hayir_Butonu.find_element(By.XPATH, '..').click()
                sleep_a_while(1, 2)
            except:
                pass
    except:
        pass

def get_browser(chromedriver_path, download_dir, prompt=False, upgrade=True, ntry=1):
    try:
        chrome_options = webdriver.ChromeOptions()
        service = Service(executable_path=chromedriver_path)

        preferences = {"download.prompt_for_download": prompt,
                       "download.default_directory": download_dir,
                       "download.directory_upgrade": upgrade,
                       "profile.default_content_settings.popups":1,
                       "profile.default_content_setting_values.notifications": 2,
                       "profile.default_content_setting_values.automatic_downloads": 1,
                       }

        chrome_options.add_experimental_option("prefs", preferences)
        driver = webdriver.Chrome(service=service,
                                  options=chrome_options)
        return driver
    except Exception as e:
        print('Browser oluşturulurken şu hata ile karşılaşıldı:', e)
        if ntry <=3:
            print(f'Browser tekrar oluşturulmaya çalışılıyor... Deneme ({ntry})')
            return get_browser(chromedriver_path, download_dir, prompt=False, upgrade=True, ntry=ntry+1)
        else:
            return None


def get_element(driver, name, by='class'):
    found = False
    element = None
    try:
        if by =='class':
            element = driver.find_element(By.CLASS_NAME, name)
        elif by =='id':
                element = driver.find_element(By.ID, name)
        found = True
        return element

    except:
        if found:
            return element

        return None


def hosgeldiniz_penceresini_kapat(driver):
    try:
        div = driver.find_element(By.CLASS_NAME, 'GLTFe')
        if div is not None:
            click_and_press_esc(driver)
    except:
        pass

def move_mouse_to_element(driver, element):
    try:
        win_rect = driver.get_window_rect()
        # x = win_rect['x'] + win_rect['width'] / 2
        # y = win_rect['y'] + win_rect['height'] / 2
        x = win_rect['x'] + element.location['x'] + 100
        y = win_rect['y'] + element.location['y']
        pgui.moveTo(x, y)
    except Exception as e:
        print("Mouse'u elemana taşırken bir hata ile karşılaşıldı. Hata şu:\n", e)
        pass


def move_mouse_to_mid_window(driver):
    try:
        win_rect = driver.get_window_rect()
        x = win_rect['x'] + win_rect['width'] / 2
        y = win_rect['y'] + win_rect['height'] / 2
        pgui.moveTo(x, y)
    except Exception as e:
        print("move_mouse_to_mid_window fonksiyonunda bir hata ile karşılaşıldı. Hata şu:\n", e)
        pass
    # diğer yol
    # import ctypes
    # ctypes.windll.user32.SetCursorPos(x, y) # move mouse to
    ## bunlar diğer örnekler
    # https://learn.microsoft.com/tr-tr/windows/win32/api/winuser/nf-winuser-mouse_event?redirectedfrom=MSDN
    # ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    # ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up
    # browser pencerenin başladığı piksel (y değeri)
    # driver.execute_script('return window.outerHeight - window.innerHeight;')


def open_page(driver, url):
    driver.get(url)
    driver.implicitly_wait(3.5)
    sleep_a_while(sleep_min=sleep_min , sleep_max=sleep_max )  # better to sleep a while

    click_accept_button(driver)
    driver.implicitly_wait(1)
    sleep_a_while(sleep_min=sleep_min , sleep_max=sleep_max )  # better to sleep a while
    click_and_press_esc(driver)
    sleep_a_while(sleep_min=sleep_min , sleep_max=sleep_max )  # better to sleep a while
    click_and_press_esc(driver)

def captcha_asked(driver):
    div_captcha = None
    try:
        div_captcha = driver.find_element(By.ID, 'captcha-container')
    except Exception as e:
        pass

    if div_captcha is None:
        return False
    else:
        return True


def read_more_butonuna_bas(driver):
    # read more butonuna basalım ki tüm yorumların textlerinin tamamı görünür olsu.
    # bu butonların birine tıklamak yeterli
    click_and_press_esc(driver)
    click_and_press_esc(driver)

    try:
        read_more = driver.find_element(By.CLASS_NAME,'Ignyf')
        if read_more is not None:
            read_more.click()
    except:
        try:
            driver.implicitly_wait(wait_time, )
            sleep_a_while(sleep_min=sleep_min , sleep_max=sleep_max)  # better to sleep a while

            # sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

            read_more = driver.find_element(By.CLASS_NAME,'Ignyf')
            if read_more is not None:
                read_more.click()
        except:
            # print("Hiç Bir Yorum Bilgisi Bulunamadı: otelID:", hotel_id)
            # yorum_olmayanlari_yaz(hotel_id, download_dir
            # print("Read More butonu bulunamadı")
            pass


def sleep_a_while(sleep_min = sleep_min, sleep_max = sleep_max, factor= 1.0,):
    # sleep(sleep_min * factor)
    sleep( ((sleep_max-sleep_min) * random() + sleep_min ) * factor)

def yorum_olmayanlari_yaz(hotel_id, root_folder=getcwd()):

    with open(join(root_folder, '../Yorum bulunamayan oteller.txt'), 'a', encoding='utf8') as f:
        f.writelines(str(hotel_id) + "\n")

def write_or_append_data(data, file,):
    if not exists(dirname(file)):
        makedirs(dirname(file))

    if exists(file):
        if ".feather" in file:
            df_saved_data = pd.read_feather(file)
        elif ".parquet" in file:
            df_saved_data = pd.read_parquet(file)
    else:
        df_saved_data = data

    try:
        print("DataFrame kayıt ediliyor... ", end='')
        data.reset_index(inplace=True, drop=True)
        new_data = pd.concat([df_saved_data, data], ignore_index=True, sort=False)

        if ".feather" in file:
            new_data.to_feather(file)
        elif ".parquet" in file:
            new_data.to_parquet(file)

        print("Başarılı!")
    except Exception as e:
        print("DataFrame dosyasını yazarken şu hata ile karşılaşıldı:", e)


def write_last_index(index, file):
    if not exists(dirname(file)):
        makedirs(dirname(file))

    with open(file, "w") as f:
        f.writelines(str(index))