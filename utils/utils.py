from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
import pyautogui as pgui
from os import getcwd
from os.path import join, exists
import pandas as pd
from selenium.webdriver.common.by import By
import gc
from selenium.webdriver.common.keys import Keys


sleep_min = .15
sleep_max = .25
slp_factor = 15
slp_small_factor = 7.5


def click_accept_button(driver):

    try:
        #btn_accept = driver.find_element_by_id( 'onetrust-accept-btn-handler')

        btn_accept = driver.find_element(By.XPATH, "//button[@id='onetrust-accept-btn-handler']")

        if btn_accept is not None:
            btn_accept.click()
    except:
        pass


def click_and_press_esc(driver):

    try:
        btn_accept = driver.find_element(By.ID, '_evidon-accept-button')
        if btn_accept is not None:
            btn_accept.click()

    except:
        pass

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def find_next_button(driver):

    try:
        btnNext = driver.find_element(By.XPATH, '//div[@data-trackingstring="pagination_h"]//a[text()="Next"]')
    except:
        return None
    return btnNext


def get_browser(chromedriver_path, download_dir, prompt=False, upgrade=True):
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


def parse_img_url(url):

    parts = url.split("https//", True)[0].split(' ')[0].split('?')[0]

    path = parts.split('.')
    ext = path[-1] # extension (like jpg)
    part_slashes = path[2].split('/')

    #name of file designated after all / 's )
    name = part_slashes[-1]
    hex_name = "".join(part_slashes[-5:-1])
    return name, hex_name, ext

def otel_sayfasini_ac(driver, url):
    driver.get(url)
    driver.implicitly_wait(3)
    sleep_a_while(sleep_min=sleep_min , sleep_max=sleep_max )  # better to sleep a while

    click_accept_button(driver)
    driver.implicitly_wait(1)
    sleep_a_while(sleep_min=sleep_min , sleep_max=sleep_max )  # better to sleep a while

    click_and_press_esc(driver)


def sleep_a_while(factor= 1.0, sleep_min = sleep_min, sleep_max = sleep_max):
    sleep(sleep_min * factor)
    # sleep( ((sleep_max-sleep_min) * random() + sleep_min ) * factor)


def yorum_olmayanlari_yaz(hotel_id, root_folder=getcwd()):

    with open(join(root_folder, '../Yorum bulunamayan oteller.txt'), 'a', encoding='utf8') as f:
        f.writelines(str(hotel_id) + "\n")


def save_data(df_hotel, df_review, file_hotel, file_yorum, root_folder= getcwd()):
    if df_hotel is not None:
        if exists(join(root_folder,file_hotel)):
            df_saved_hotel = pd.read_feather(join(root_folder, file_hotel))
            df_saved_hotel = pd.concat([df_saved_hotel, df_hotel], ignore_index=True, sort=False)
        else:
            df_saved_hotel = df_hotel

        try:
            df_saved_hotel.reset_index(inplace=True, drop=True)
            print("Otel bilgileri kayıt ediliyor... ", end='')
            df_saved_hotel.to_feather(join(root_folder, file_hotel))
            print("Başarılı!")

            df_saved_hotel = None
        except Exception as e:
            print("Otel bilgileri Feather dosyasını yazarken hata ile karşılaşıldı")
            print(e)

    if df_review is not None:
        if exists(join(root_folder, file_yorum)):
            df_saved_yorum = pd.read_feather(join(root_folder, file_yorum))
            df_saved_yorum = pd.concat([df_saved_yorum, df_review], ignore_index=True, sort=False)
        else:
            df_saved_yorum = df_review

        try:
            df_saved_yorum.reset_index(inplace=True, drop=True)
            print("Yorum bilgileri kayıt ediliyor... ", end='')
            df_saved_yorum.to_feather(join(root_folder, file_yorum))
            print("Başarılı!")

            df_saved_yorum = None
        except Exception as e:
            print("Yorum bilgileri Feather dosyasını yazarken hata ile karşılaşıldı")
            print(e)

    gc.collect()
    sleep(1)

def write_last_index(index, root_folder=getcwd()):
    with open(join(root_folder, 'last_index.txt'), "w") as f:
        f.writelines(str(index))