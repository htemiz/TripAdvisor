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
from os.path import join, abspath, dirname, basename, exists
from os import makedirs

from utils import *


user_agent_02 = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

headers_01 = {'User-Agent': user_agent_02,
        #'User-Agent': '*',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'Cache-Control': 'no-cache',
'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
'Host': 'www.tripadvisor.com',
'Pragma': 'no-cache',
'Referer': 'https://www.tripadvisor.com/',
#'Referer': url_from_autocomplete,

}


headers_02 = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'}

headers_03 = {
    'cookie': 'TAUnique=%1%enc%3AHvAwOscAcmfzIwJbsS10GnXn4FrCUpCm%2Bnw21XKuzXoV7vSwMEnyTA%3D%3D; fbm_162729813767876=base_domain=.tripadvisor.com; TACds=B.3.11419.1.2019-03-31; TASSK=enc%3AABCGM1r6xBekOjRaaQZ3QVS7dP4cwZ8sombvPTq8xK6xN55i7TN8puwZdwvXvG1i%2FJ2UQXYG1CwsU%2BXLwLs5qIxnmW5qbLt4I48DfK5FhHpwUw3ZgrbskK%2FjDc4ENfcCXw%3D%3D; ServerPool=C; TART=%1%enc%3A8yMCW7EtdBqPX0oluvfOS5mBk6DRMHXwNEAPJlcpaDumiCWsxs%2BxfBbTYsxpa%2F9l%2FJzCllshf9g%3D; VRMCID=%1%V1*id.10568*llp.%2FRestaurant_Review-g187147-d3405673-Reviews-La_Terrasse_Vedettes_de_Paris-Paris_Ile_de_France%5C.html*e.1557691551614; PMC=V2*MS.36*MD.20190505*LD.20190506; PAC=ALNtqHPT2KJjQwExTPJt3gCvzvDYH_x63ZOT4b3LetvkHuHXcEUY4eLx0TqKGzOIpoXF3K_j57rNigUkWJzSv7TtTna4L3DKcfiaeK9zT9ixGEevH6QwZVd-PdMyr9y5aRzjEVAfid42zC4WXeTcQTJkPVwGMCW2mB2k3xxfB78GgJFIR_I9vf6Bzhq89x_UTTUcQgFpCr8GEFV9GpJWG8UNGeriJSbmPtCXA10oXl5ox7U9TQvSILLSH8PdrP8nwUQMRnfUA_fKbXTaRgH4tzBwZQpbd1vlOOg7fKyfIN9V95PzNOXBEQCJIo3z09Nux0tyZZVX0PX_zI_moLpr9Od3eSi1E8Hm5QcLyG9QNfA1C5WckG9GOV5VKEL0bxDY5TG1smCaQDXpRLkvp8w2bD7vyI2e27WFbtuYvJDJ126v2_KyZmVbG3laZlvWrX2kWGL13IyhVS2Ivjr_9uJAwMpBKuNByH0FBU3ziJcRdqkXiz6lnYMSRSQ1Y8Dmkjkrc0DNTABvuHjbZ7Fh0LOINswW_wrkVsP4PjDq1IVh7IY0hLE_W1G1DKlROc5BZEOjcw%3D%3D; BEPIN=%1%16a8c46770b%3Bbak92b.b.tripadvisor.com%3A10023%3B; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*DSM.1557131589173*RS.1*RY.2019*RM.5*RD.6*RH.20*RG.2; CM=%1%RestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7Csesstch15%2C%2C-1%7CCYLPUSess%2C%2C-1%7Ctvsess%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CRestPartSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csesshours%2C%2C-1%7CTARSWBPers%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7Csesslaf%2C%2C-1%7CRestPartPers%2C%2C-1%7CCYLPUPers%2C%2C-1%7CCCUVOwnSess%2C%2C-1%7Cperslaf%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CSPMCPers%2C%2C-1%7Cperswifi%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTrayssess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7Cbooksticks%2C%2C-1%7CSPMCWBSess%2C%2C-1%7Cbookstickp%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Csesswifi%2C%2C-1%7Ct4b-pc%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C9%2C-1%7CPremiumSURPers%2C%2C-1%7CCCUVOwnPers%2C%2C-1%7CTBPers%2C%2C-1%7Cperstch15%2C%2C-1%7CCCSess%2C2%2C-1%7CCYLSess%2C%2C-1%7Cpershours%2C%2C-1%7CPremiumORSess%2C%2C-1%7CRestAdsPers%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CTrayspers%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CMCPPers%2C%2C-1%7CSPMCSess%2C%2C-1%7Cpers_rev%2C%2C-1%7Cmdpers%2C%2C-1%7Cmds%2C1557131565748%2C1557217965%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CHomeAPers%2C%2C-1%7CRCSess%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7Cpssamex%2C%2C-1%7CCYLPers%2C%2C-1%7Ctvpers%2C%2C-1%7CTBSess%2C%2C-1%7CAdsRetSess%2C%2C-1%7CMCPSess%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7Cmdsess%2C%2C-1%7C; fbsr_162729813767876=wtGNSIucBSm5EusyRkPyX_GfZwxNkyHLxTRli46iHoM.eyJjb2RlIjoiQVFBUHV3SlZpOVNXQXVkMDh1bUdaYjZ2R3hBMkdfdFBZdm9Bb2l2cDEzSDNvaG1ESjRkamo1V1A3dnB5WloxWmwzeWxFTmdCT0dCbTB6dzc1S2pwUHFKak5nQVNKMGNqOEtvUVY1YzZXNHhNQ1FlMURNNXJOUUpMeEJldjlBS2xKNnhVVjVXQ1ZaajZjN1k4X1ZWeGdxbzlIclhKT3BvUDZSLTVzNkVUZ3Q5Q0xMNmg0ZnZIY0pMSm1KdXJwN0lGVFBSOUdvX0Z4M0FiM0VWQ1RnVFNGNzc2NFFuU29fdER5VFk3TWY0V0VKSFZXZi11ME1pa2ZWS1ZzUHdHQlBOOE1xZkVQNjZfZHpZMVdnSEVfcWR4d2FHN2xNODNyR1BWaDVwdDdodlFQQmFBbGtzU21IYjZiSktEaGVGajM4WTg3TGxUUF9hNEVGUjVjOVdoOVNhY2RmV04iLCJ1c2VyX2lkIjoiMTY1NjQ2NDcxNSIsImFsZ29yaXRobSI6IkhNQUMtU0hBMjU2IiwiaXNzdWVkX2F0IjoxNTU3MTMzMTgxfQ; TAReturnTo=%1%%2FRestaurants-g304551-New_Delhi_National_Capital_Territory_of_Delhi.html; roybatty=TNI1625!APyGsDM6tcKypRo49myenvbO5Zyk367lJP3JEhTSBrfno%2F4Bbienyfvs6Q2DU%2F2UmkzjN1pKquiSNGeY2cXQm8s8oX1jKwXT8hgK3GL%2B6psZHdp4k7TF4F52uoI2kQ1e9Ni2k9Ub8D5ak%2FXgN%2F9as9m2HZIB0G6SZnZMT%2FPD73Fo%2C1; SRT=%1%enc%3A8yMCW7EtdBqPX0oluvfOS5mBk6DRMHXwNEAPJlcpaDumiCWsxs%2BxfBbTYsxpa%2F9l%2FJzCllshf9g%3D; TASession=V2ID.2C4059CFCBC27797DA97994A5CF94A28*SQ.233*LS.PageMoniker*GR.7*TCPAR.44*TBR.80*EXEX.60*ABTR.87*PHTB.57*FS.2*CPU.54*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*LF.en*FA.1*DF.0*IR.4*TRA.false*LD.304551; TAUD=LA-1557055610999-1*RDD-1-2019_05_05*RD-75954750-2019_05_06.9784431*HDD-75978369-2019_05_19.2019_05_20.1*HC-76743574*LG-77588176-2.1.F.*LD-77588177-.....',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
}



def get_hotel_ids(region_id, star=None, driver=None,  sleep_min=0.05, sleep_max=0.1 ):

    if driver is None:
        chromedriver_path = r"D:\programlar\chromedriver 95.exe"
        driver = get_browser(chromedriver_path, download_dir)

    baseurl = 'https://www.tripadvisor.com/Hotels-g' + region_id
    #baseurl2 = 'https://www.tripadvisor.com/Hotel_Review-g'
    ids = list()

    oastep = 30
    citypage = 0
    otelIDre = re.compile(r'property_([0-9]+)',  re.M | re.S)
    bolgekodure = re.compile(r'g([0-9]+)')
    otelkodure = re.compile(r'd([0-9]+)')
    #otelyildizire = re.compile(r'class="ui_star_rating star_[0-9]', re.M)
    #otelyildizi = ""

    i = 0
    total = None


    while True:
        if star is not None:
            strYildiz = '-zfc%s' % star
        else:
            strYildiz = ''

        if citypage == 0:
            cityurl = '%s' % baseurl + strYildiz
        else:
            cityurl = '%s-oa%s' % (baseurl, citypage * oastep) + strYildiz

        driver.get(cityurl)

        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

        try:
            btn_accept = driver.find_element_by_id('_evidon-accept-button')
            if btn_accept is not None:
                btn_accept.click()
        except:
            pass

        htmlpage = driver.page_source

        if total is None:
            count = driver.find_element_by_class_name("eMoHQ").text.split(" ")[0]
            total = int(count.replace(',',''))

        [ids.append(x) for x in re.findall(otelIDre, str(htmlpage))]


        if citypage * oastep >= total:
            break

        citypage += 1
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

    ids = list(set(ids))

    return ids


def find_next_button(driver):

    # div = driver.find_element_by_class_name("prw_common_standard_pagination_resp")
    try:
        btnNext = driver.find_element_by_xpath('//div[@data-trackingstring="pagination_h"]//a[text()="Next"]')

    except:
        return None

    return btnNext

def click_btnAccept_privacy(driver):

    try:
        #btn_accept = driver.find_element_by_id( 'onetrust-accept-btn-handler')

        btn_accept_privacy = driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']")

        if btn_accept_privacy is not None:
            btn_accept_privacy.click()
    except:
        pass


def get_hotel_ids_with_next_button(region_id, star=None, driver=None,  sleep_min=0.05, sleep_max=0.1 ):

    if driver is None:
        chromedriver_path = r"D:\programlar\chromedriver 97.exe"
        driver = get_browser(chromedriver_path, download_dir)

    baseurl = 'https://www.tripadvisor.com/Hotels-g' + region_id
    #baseurl2 = 'https://www.tripadvisor.com/Hotel_Review-g'
    ids = list()

    oastep = 30
    citypage = 0
    otelIDre = re.compile(r'property_([0-9]+)',  re.M | re.S)
    bolgekodure = re.compile(r'g([0-9]+)')
    otelkodure = re.compile(r'd([0-9]+)')
    #otelyildizire = re.compile(r'class="ui_star_rating star_[0-9]', re.M)
    #otelyildizi = ""

    i = 0
    total = None




    while True:
        if star is not None:
            strYildiz = '-zfc%s' % star
        else:
            strYildiz = ''

        if citypage == 0:
            cityurl = '%s' % baseurl + strYildiz
        else:
            cityurl = '%s-oa%s' % (baseurl, citypage * oastep) + strYildiz

        driver.get(cityurl)

        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

        driver.implicitly_wait(3, )

        try:
            btn_accept = driver.find_element_by_id('_evidon-accept-button')
            if btn_accept is not None:
                btn_accept.click()
        except:
            pass

        driver.implicitly_wait(3, )
        # better to sleep a while

        click_btnAccept_privacy(driver)
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        htmlpage = driver.page_source

        if total is None:
            count = driver.find_element_by_class_name("eMoHQ").text.split(" ")[0]
            total = int(count.replace(',',''))
            print("total ", total)

        [ids.append(x) for x in re.findall(otelIDre, str(htmlpage))]

        btnNext = find_next_button(driver)

        citypage +=1
        print('Sayfa: ', citypage, "  gezildi.")
        if btnNext is not None and btnNext.text == "Next":
            btnNext.click()
        else:
            break

        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while



    ids = list(set(ids))

    return ids



def main():
    sehir = "Istanbul"
    otelyildizi = None # tüm yıldızlı oteller ya da # 5 (yıldızlı demek için)

    sehir_ve_ID = {"London":186338, "NewYork":60763, "Paris":187147, "Tokyo":298184, "Beijing":294212,
                   "Istanbul": 293974, "Belek": 312725, 'Girit': 189413,
                   "Mayorka": 187462, 'Antalya': 297962}

    sehirler =('London', 'NewYork', 'Paris', 'Tokyo', 'Beijing')
    sehirler =( 'NewYork', 'Paris', 'Tokyo', 'Beijing')


    for sehir in sehirler:

        chromedriver_path = r"D:\programlar\chromedriver 106.exe"
        download_dir = r"d:\calisma\projeler\tripadvisor\data"
        driver = get_browser(chromedriver_path, download_dir)

        region_id = str(sehir_ve_ID[sehir])


        ids = get_hotel_ids_with_next_button(region_id, star=None, driver=driver,  sleep_min=0.05, sleep_max=0.1 )

        print(sehir + ' için ' , len(ids), "Otel ID'si alındı")

        with codecs.open(join(download_dir, sehir + '_oteller.csv'), 'w', encoding='utf8') as cikti:
            yazici = csv.writer(cikti, )
            for x in list(ids):
                yazici.writerow([x])

        driver.close()
        sleep(4)

"""

for otelID in re.findall(otelIDre, str(htmlpage)) :
    i += 1
    # tree = html.fromstring(htmlpage.content)
    # tree = html.fromstring(str(htmlpage))
    # tree = html.fromstring(driver.execute_script("return document.documentElement.outerHTML;"))

    html= BeautifulSoup(htmlpage, features="lxml")

    otelismi = driver.find_element_by_xpath('//a[@id="property_' + otelID + '"]').text

    otelyildizi = driver.find_element_by_xpath("//svg[@class = 'RWYkj']")


    driver.find_element("svg", "")


    otelyildizi = tree.xpath(
        '//[svg[@class="TkRkB"]]')

    kodlar = tree.xpath('//*[@id="property_' + otelID + '"]/@href')
    bolgekodu = re.search(bolgekodure, str(kodlar)).group().strip('g')
    otelkodu = re.search(otelkodure, str(kodlar)).group().strip('d')

    # kısayol kapa=ctrl+k+c, aç=ctrl+k+u
    # baseurlget = baseurl2 + bolgekodu + '-d' + otelkodu
    # otelpage = requests.get(baseurlget)

    # if re.search(otelyildizire, str(otelpage.content)) is not None:
    #     otelyildizi = re.search(otelyildizire, str(otelpage.content)).group()
    #     otelyildizi = re.search('[0-9]', otelyildizi).group()
    # else:
    #     otelyildizi = None
    # i += 1
    # print(str('{}. otel için otel yildiz degeri:{}'.format(i, otelyildizi)))
    yorumYaz: List[Any] = ["Antalya", bolgekodu,
                           otelkodu, otelismi, otelyildizi]
    yazici.writerow(yorumYaz)
    print("{}. otel indirildi".format(i))
    #baseurlget = baseurl2
citypage += 1
if citypage == 2:
    print("bitti")
"""


main()

#
# if __name__ == '__main__':
#     main()
