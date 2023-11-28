import requests
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import csv
from sys import argv
import time
from time import sleep
from pandas import DataFrame
from numpy.random import random
import argparse
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support.select import Select
import re
from os.path import join, exists
from os import makedirs
import pandas as pd
import traceback

from utils import *

sleep_min = .15
sleep_max = .25
slp_factor = 15
slp_small_factor = 7.5

def sleep_a_while(factor= 1.0, sleep_min = sleep_min, sleep_max = sleep_max):
    sleep(sleep_min * factor)
    # sleep( ((sleep_max-sleep_min) * random() + sleep_min ) * factor)


def parse_element( div_Pksol_Next_Sibling):
    reg_url =""
    profile_name =""
    splt_dynamic = "https://dynamic-media-cdn.tripadvisor.com/media/"
    splt_static  = "https://media-cdn.tripadvisor.com/media/"

    # m =  driver.find_element_by_xpath('//div[@aria-label="View photo"]')

    # Under <div aria-label="View photo"> there is only one child :
    #   <div class="dIRoN">  has 3 children div
    #      1st div has image url
    #      2nd ??
    #      3rd
    #
    # div_Pksol_Next_Sibling has 2 main div
    #
    #   1st div
    #       1st div  -> LEFT BUTTON
    #       2nd div  -> RIGHT BUTTON
    #       3rd div class="eRRor _Q s"  ->  PICTURES
    #           1st div  class="bITwU undefined"    -> previous picture
    #           2nd div  class="bITwU bWjLp _Q s"   -> current picture
    #               div -> div ->
    #                   1st div     -> picture here
    #                   2nd div     some headers (e.g., 1 of 1295)
    #                   3rd div     USER and Review INFOs
    #                       1st div class="FKlEP f k"  -> some divs -> <a href="/profile/..."
    #
    #                       2nd div     -> Review
    #
    #           3rd div  class="bXuCL"              -> next picture
    #
    #

    """
    soup = BeautifulSoup(element.get_attribute('innerHTML'),'html.parser')

    img_div  =soup.div.div
    style = img_div.attrs["style"]
    img_url = re.findall(reg_url_string, style)[0]

    """

    # html = BeautifulSoup(div_Pksol_Next_Sibling.get_attribute('innerHTML'), 'html.parser')
    # html.find("img", source=re.compile("dynamic-media-cdn"))
    # html.find("img")

    sleep_a_while() # better to sleep a while

    html = BeautifulSoup(div_Pksol_Next_Sibling.get_attribute('innerHTML'), 'html.parser')
    try:
        url = html.find("source", srcset=re.compile("dynamic-media-cdn"))
        if url is not None:
            url = url.attrs["srcset"]

        else:
            url = html.find("img", src=re.compile("media-cdn.tripadvisor.com"))

            if url is not None:
                url = url.attrs["src"]
    except:
        print("URL not retrieved")
        print("URL: ", url)
        sleep(1)
        return None, None

    try:

        reg_url = re.findall(reg_url_string, url)[0]
    except Exception:
        traceback.print_exc()
        print("Regex cannot parse!", url)
        print("URL: ", url)
        print("Regexed url: ", reg_url)
        sleep(2)


    a_profile = html.find("a", href=re.compile("Profile"))
    if a_profile is not None:
        profile_name = a_profile.attrs["href"].split("/Profile/")[-1]

    html.findAll("button")

    return reg_url, profile_name


def write_albums_not_exist(hotel_id, album):

    try:
        f = open(file_albums_not_exist, "a")
        f.writelines(str(hotel_id) + "\t" + str(album) + "\n")
        f.close()
    except Exception:
        traceback.print_exc()
        print("Cannot write to file '" + file_albums_not_exist + "'" )


def write_wrong_ids(hotel_url, file_wrong_ids):
    try:
        f = open(file_wrong_ids, "a")
        f.writelines(hotel_url + "\n")
        f.close()
    except Exception:
        traceback.print_exc()
        print("Cannot write to file 'file_wrong_ids.txt' hotel url:", hotel_url)

def write_problematic_hotel_urls(hotel_url, file_wrong_ids):
    try:
        f = open(file_problematic_hotel_urls, "a")
        f.writelines(hotel_url + "\n")
        f.close()
    except Exception:
        traceback.print_exc()
        print("Cannot write to file 'problematic_hotel_urls.txt' hotel url:", hotel_url)

def write_first_picture_in_album_not_retrieved(hotel_url, album):
    try:
        f = open(file_first_picture_in_album_not_retrieved, "a")
        f.writelines(hotel_url + "\tALBUM: " + album + "\n")
        f.close()
    except Exception:
        traceback.print_exc()
        print("Cannot write to file '" + file_first_picture_in_album_not_retrieved + "' hotel url: ",
              hotel_url + " ALBUM: " + dict_albums[v])

def collect_elements(driver, div, div_Pksol_Next_Sibling,  scroll=1000):

    images = list()
    nxt_button = div_Pksol_Next_Sibling.find_element_by_css_selector("button[aria-label='Next']")
    # driver.manage().timeouts().implicitlyWait(5, TimeUnit.SECONDS)
    div_eRRor = div_Pksol_Next_Sibling.find_element_by_class_name("eRRor")

    # script = 'arguments[0].scrollBy(0,' + str(scroll) + ')'
    # elements =  driver.find_elements_by_xpath('//div[@aria-label="View photo"]')
    elements= list()
    """
    for e in elements:
        sleep(random(sleep_min, sleep_max))

        try:
            im_url, usr_name = parse_element(div_Pksol_Next_Sibling)

            if im_url is not None:
                images.append((im_url, usr_name))
                print(im_url, usr_name)

        except :
            print("Dosya indirilemedi")

        nxt_button.click()
    """

    reached_end = False
    first = True

    while not reached_end:
        # driver.execute_script(script, div)

        sleep_a_while()

        tmp = driver.find_elements_by_xpath('//div[@aria-label="View photo"]')
        if len(tmp) == 0:
            div_cur_picture = div_eRRor.find_elements_by_xpath("./div")[1]  # second child div
            im_url, usr_name = parse_element(div_cur_picture)
            images.append((im_url, usr_name))
            reached_end = True
            break

        for a in tmp:
            if elements.__contains__(a):
                reached_end = True
            else:
                elements.append(a)
                reached_end = False
                try:
                    # take the first picture from the 2nd sub div,
                    # take the others from the 3rd sub div
                    elem_idx = 1 if first  else 2 # second child
                    div_cur_picture = div_eRRor.find_elements_by_xpath("./div")[elem_idx]  # second child div

                    im_url, usr_name = parse_element(div_cur_picture)

                    print(im_url, usr_name)

                    if im_url is not None:
                        images.append((im_url, usr_name))

                    if  nxt_button.get_attribute("disabled"): # button is disabled since only one picture exists
                        reached_end = True
                        print("End of album")
                        break
                    else:
                        nxt_button.click() # go to next picture

                    sleep_a_while()

                except Exception as e:
                    traceback.print_exc()

    return images

def find_indexes(albums, dict_albums, indexes_to_download, hotel_id):

        dict_return = dict()
        dict_albums_fetched = dict()

        for j in range(len(albums)):
            alb = BeautifulSoup(albums[j].get_attribute("innerHTML"), "html.parser")
            albm_text = alb.div.div.contents[1].div.div.text
            albm_text = albm_text.replace("&amp;", "&")
            dict_albums_fetched[albm_text] = j

        for k in indexes_to_download:
            if dict_albums_fetched.__contains__(dict_albums[k]):
                dict_return[k] =  dict_albums_fetched[dict_albums[k]]
            else:
                print(f"Album '{dict_albums[k]}' not exist in the albums.", )
                write_albums_not_exist(hotel_id, dict_albums[k])

        return dict_return

#
#       TAKE HOTEL IDs
#
xl_file_Hotel_IDs = r"D:\calisma\projeler\tripadvisor\data\Otel IDleri.xlsx"
file_wrong_ids = r"D:\calisma\projeler\tripadvisor\data\wrong_ids.txt"
file_first_picture_in_album_not_retrieved = r"D:\calisma\projeler\tripadvisor\data\First picture in album not retrieved.txt"
file_problematic_hotel_urls = r"D:\calisma\projeler\tripadvisor\data\problematic_hotel_urls.txt"
file_albums_not_exist = r"D:\calisma\projeler\tripadvisor\data\Albums_not_exist.txt"


df_hotel_ids = pd.read_excel(xl_file_Hotel_IDs, usecols="B")
Hotel_IDs = df_hotel_ids.loc[:, 0].to_list()

reg_url_string =r"""\b((?:https?://)?(?:(?:www\.)?(?:[\da-z\.-]+)\.(?:[a-z]{2,6})|(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)|(?:(?:[0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,5}(?::[0-9a-fA-F]{1,4}){1,2}|(?:[0-9a-fA-F]{1,4}:){1,4}(?::[0-9a-fA-F]{1,4}){1,3}|(?:[0-9a-fA-F]{1,4}:){1,3}(?::[0-9a-fA-F]{1,4}){1,4}|(?:[0-9a-fA-F]{1,4}:){1,2}(?::[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:(?:(?::[0-9a-fA-F]{1,4}){1,6})|:(?:(?::[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(?::[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(?:ffff(?::0{1,4}){0,1}:){0,1}(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])|(?:[0-9a-fA-F]{1,4}:){1,4}:(?:(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(?:25[0-5]|(?:2[0-4]|1{0,1}[0-9]){0,1}[0-9])))(?::[0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])?(?:/[\w\.-]*)*/?)\b"""
button_kabul = '<button id="_evidon-accept-button" class="evidon-banner-acceptbutton" tabindex="0" aria-label="Kabul" style="cursor: pointer;">Kabul</button>'


url_kirbiyik = "https://www.tripadvisor.com/Hotel_Review-g1192197-d1195695"
album_Room = "https://www.tripadvisor.com/Hotel_Review-g1192197-d1195695-Reviews-Kirbiyik_Resort_Hotel_Alanya-Kargicak_Alanya_Turkish_Mediterranean_Coast.html#/media/1195695/191918241:p/?albumid=101&type=0&category=101"
album_Pool_Beach = "https://www.tripadvisor.com/Hotel_Review-g1192197-d1195695-Reviews-Kirbiyik_Resort_Hotel_Alanya-Kargicak_Alanya_Turkish_Mediterranean_Coast.html#/media/1195695/?albumid=104&type=0&category=104"

chromedriver_path = r"D:\programlar\chromedriver 93.exe"
download_dir =  r"d:\calisma\projeler\tripadvisor\download_albums"
driver = get_browser(chromedriver_path, download_dir)
# driver.maximize_window()


"""
# Albums panes on the left side are separated by divs with class name: "bWqnk z w"
# There are 9 panes (groups)
____________________________
0.All photos
1.' Traveler'
2.Hotel & Amenities
3.Pool & Beach
4.Room/Suite
5.Panoramas
6.Bathroom
7.'Dining    '
8.Family/Play Areas
____________________________
<div class="bWqnk z w" style="margin-bottom: 0px;"><div class="dIzpy w h _S"><div class="fdWJU o w h z R2 bQqyi"><div class="fYoLS t l _U o"><div class="bxLAc GA" style="height: 100%; width: 100%; position: relative;"><img class="bMGfJ _Q t _U s l bnegk" src="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/0d/57/b1/b4/spa--v13835882.jpg?w=300&amp;h=200&amp;s=1" alt="" style="height: 100%; width: 100%; object-fit: cover;"></div></div><div class="caHPn s l _U u j b z"><div class="eLFmY M0 _T w o _X z"><div class="jlBfu W o">Hotel &amp; Amenities</div><div class="eHNTQ"> (1034) </div></div></div></div></div></div>

driver.get(album_Pool_Beach)
"""
dict_albums = {0:'All photos', 1:'Traveler', 2:'Hotel & Amenities', 3:'Pool & Beach', 4:'Room/Suite',
               5:'Panoramas', 6:'Bathroom', 7:'Dining    ', 8:'Family/Play Areas'}


cols=["Hotel ID", "Album", "Url", "User Name"]


main_url= "https://www.tripadvisor.com/Hotel_Review-g1192197-d"

albums_to_download = list(range (1,9)) # all albums except 'All photos'
# albums_to_download = list(range (6,8)) # all albums except 'All photos'

start = 227 # en son burada kaldı

for j in range(0, len(Hotel_IDs[start:])):

    hotel_id = Hotel_IDs[j+ start]

    hotel_url = main_url + str(hotel_id)

    print("\nHOTEL: ", hotel_url)

    df = DataFrame(columns=cols, )

    hata_olustu = True

    try:
        driver.get(hotel_url)
        hata_olustu = False

    except:
        if hata_olustu:
            wrong_id = str(Hotel_IDs[j + start ])
            write_problematic_hotel_urls(wrong_id, file_wrong_ids)
            print(f"Hotel with id {wrong_id} does not exist!\n")
            continue

    else:
        if hata_olustu:
            # hata bağlantının karşı taraf tarafından kesilmesinden
            # kaynaklanıyor olabilir. Az bekleme süresinin karesi
            # ile bekleme süresinin çarpımı kadar bekle ve sonra devam et
            sleep_a_while(slp_small_factor**2)
            continue

    sleep_a_while()

    try:
        btn_accept = driver.find_element_by_id('_evidon-accept-button')
        if btn_accept is not None:
            btn_accept.click()

    except:
        pass

    sleep_a_while()
    # Close the booking pop-up window
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    sleep_a_while()

    hata_olustu = True

    try:
        # Open "PHOTOS" view by clicking Main Image Pane
        # driver.find_element_by_xpath('//div[@data-section-signature="photo_viewer"]').click()
        driver.find_element_by_id('taplc_resp_hr_atf_photos_component_mas_media_window_0').click()
        hata_olustu = False
    except Exception as e:
        if hata_olustu:
            # traceback.print_exc()
            wrong_id = str(Hotel_IDs[j + start ])
            write_wrong_ids(wrong_id, file_wrong_ids)
            print(f"Hotel with id {wrong_id} does not exist!\n")
            continue

    else:
        if hata_olustu:
            continue

    # sleep to wait until page is loaded with albums
    sleep_a_while(slp_factor)

    albums = driver.find_elements_by_class_name('bWqnk')

    idxs_to_download = find_indexes(albums, dict_albums, albums_to_download, str(hotel_id))

    for i, v in idxs_to_download.items(): # do not include "All photos"

        print("ALBUM : " , dict_albums[i])

        # if i >= len(albums):
        #     print("The index cannot be out of range of albums")
        #     print("passing this album")
        #     continue

        albums[v].click()  # activate album on the right pane

        folder_path = join(download_dir, dict_albums[i])
        if not exists(folder_path):
            makedirs(folder_path)

        div_Pksol = driver.find_element_by_class_name('Pksol')
        div_Pksol_Next_Sibling = driver.find_element_by_xpath("//div[@class='Pksol _R z']/following-sibling::div")

        try:
            sleep_a_while(10)
            # activate first picture in the right pane
            first_pic = driver.find_element_by_xpath('//div[@aria-label="View photo"]')
            first_pic.click()

        except Exception:
            print("First picture cannot be found in the ALBUM : ", dict_albums[v])
            print("Hotel URL: ", hotel_url)
            write_first_picture_in_album_not_retrieved(hotel_url,  dict_albums[v])
            sleep_a_while()
            continue

        sleep_a_while(slp_factor)

        elements = collect_elements(driver, div_Pksol, div_Pksol_Next_Sibling, scroll=1500)

        a = [(hotel_id, dict_albums[i], im_url, user_name) for im_url, user_name in elements]
        data = pd.DataFrame(a, columns=cols)

        df = df.append(data)

        # df.to_excel(join(download_dir,  str(hotel_id) + "Data_" + dict_albums[i] + ".xlsx"))

        sleep_a_while(slp_factor)

    df.to_excel(join(download_dir, "Album_Data_" + str(hotel_id) + ".xlsx"))
    sleep_a_while(slp_small_factor)

print("ALL JOBS FINISHED")
sleep_a_while(slp_factor)
driver.quit()
    # sleep(random(sleep_min * slp_factor, sleep_max * slp_factor))


"""
Images in the Albums shown on the right pane are served within
<div aria-label="View photo" .... >

scroll all photos in the albume pane (on the right side) 
Pksol _R z
"""


#
#
#       THE FOLLOWING IS TO EXPLORE THE PICTURES ONE BY ONE
#
#



"""



def collect_elements_old_version(driver, div, div_Pksol_Next_Sibling,  scroll=1500):
    script = 'arguments[0].scrollBy(0,' + str(scroll) + ')'
    elements =  driver.find_elements_by_xpath('//div[@aria-label="View photo"]')

    for e in elements:
        e.click()

        t, u = parse_element(div_Pksol_Next_Sibling)
        print(t, u)


    reached_end = False

    while not reached_end:
        driver.execute_script(script, div)
        sleep(random(sleep_min * slp_small_factor, sleep_max * slp_small_factor))

        tmp = driver.find_elements_by_xpath('//div[@aria-label="View photo"]')
        for a in tmp:
            if elements.__contains__(a):
                reached_end = True
            else:
                elements.append(a)
                reached_end = False

    return elements


"""
