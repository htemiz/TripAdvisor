# import re
# import codecs
# from lxml import html
# import requests
# import csv
# from typing import List, Any
# import urllib.request as request
# from contextlib import closing
# from time import sleep
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.touch_actions import TouchActions
# from selenium.webdriver.support.select import Select
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options

# from selenium.webdriver.support.select import Select

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd
from utils.utils import *
import gc
from os.path import abspath, join
from sys import argv


sleep_min = 1.5
sleep_max = 3
wait_time = 3.5

width, height = 1250, 1000



def parse_about(data, driver, ):
    try:
        div_about = driver.find_element(By.XPATH,"//div[@data-tab='TABS_ABOUT']")
        # div_about = driver.find_element_by_xpath("//div[@data-placement-name='hr_community_content:ssronly']")
    except:
        print('The element TABS_ABOUT cannot be found! Returning without parsing the about section')
        return None

    divs_puanlar = div_about.find_elements(By.CLASS_NAME, 'HXCfp')

    if divs_puanlar is not None and len(divs_puanlar) > 0:
        for d in divs_puanlar:
            span = d.find_element(By.TAG_NAME, 'span')
            rating = span.get_attribute('class').split('bubble_')[-1]
            rating = str(int(rating) / 10)
            key =d.find_element(By.TAG_NAME, 'div').text
            data[key] = rating
    #
    # # div_about.find_element_by_class_name("cmZRz")
    # # data-placement-name="hr_community_content:ssronly"
    # div_puanlar = div_about.find_element_by_class_name('SSDgd')
    # s = BeautifulSoup(div_puanlar.get_attribute('innerHTML'),  'lxml')
    # r = s.find_all("div", {"class":"WdWxQ"})
    # if r is not None and len(r) >0:
    #     for e in r:
    #         try:
    #             key =  e.span.text
    #             text = e.div.next_sibling.text
    #             data[key] = text
    #             return True
    #         except:
    #             pass


def kullanici_id_al(data, r):
    try:
        a = r.find("a", {'class': 'uyyBf'})
        if a is not None:
            userID = a.attrs['href'].split('/')[-1]
            data['UserID'] = userID
    except:
        print("Kullanıcı ID'si alınamadı")
        pass


def yorum_id_al(data, r):
    try:
        div_rev_id = r.find("div", {'class': 'WAllg'})
        if div_rev_id is not None:
            revID = div_rev_id.attrs['data-reviewid']
            data['ReviewID'] = revID
    except:
        print("Yorum ID'si alınamadı")
        pass


def kullanici_bolgesini_al(data, r):
    try:
        span_region = r.find("span", {'class': 'LXUOn'})
        if span_region is not None:
            data['UserRegion'] = span_region.text
    except:
        print("Kullanıcı Bölgesi alınamadı")
        pass


def yorum_tarihi_al(data, r):
    try:
        a_review_date = r.find("a", {'class': 'uyyBf'})
        if a_review_date is not None:
            data['ReviewDate'] = a_review_date.next_sibling.split(' wrote a review ')[-1] # ingilizce, .com adresine gidince
            data['ReviewDate'] = a_review_date.next_sibling.split(', şu tarihte bir yorum yazdı: ')[-1] # Türkçe, .com.tr adresine gidince
    except:
        print("Kullanıcı Yorum Tarihi alınamadı")
        pass


def puan_balonlari_al(data, r):
    try:
        div = r.find("div", {'data-test-target':"review-rating"})  # with data-reviewid attribute
        if div is not None:
            userRating = str(int(div.span.attrs['class'][-1].split('_')[-1]) / 10.0)
            data['UserRating'] = userRating
    except:
        print("Kullanıcı puanı alınamadı")
        pass




def yorum_basligini_al(data, r):
    # review başlık
    # <div class="fpMxB MC _S b S6 H5 _a" dir="ltr" data-test-target="review-title">
    #   <a href="/ShowUserReviews-g293974-d15398698-r669762411-Istanbul_In_Hotel-Istanbul.html" class="fCitC" dir="">
    #       <span><span>Scam! Terrible</span></span></a></div>
    try:
        div = r.find("div", {'data-test-target': "review-title"})

        if div is not None:
            rTitle = div.span.span.text
            data['Title'] = rTitle
    except:
        print("Kullanıcı Yorum Başlığı alınamadı")
        pass


def yorum_metnini_al(data, r):
    # yorum
    # < q class ="XllAv H4 _a" >
    # < span > text here ...
    try:

        # q =r.find("div", {'data-test-target': "review-title"}).next_sibling.next_sibling
        q = r.find("div", {'class': "vTVDc"})

        if q is not None:
            rText = q.span.text
            data['Text'] = rText
    except:
        print("Kullanıcı Yorum Metni alınamadı")
        pass


def konaklama_tarihini_al(data, r):
    # data of stay
    # <span class="euPKI _R Me S4 H3">
    #   <span class="CrxzX">Date of stay:</span>
    # April 2019</span>
    try:
        span = r.find("span", {'class': 'teHYY'})
        if span is not None:
            rStayDate = span.text.split(':')[-1].strip()
            data['StayDate'] = rStayDate
    except:
        print("Kullanıcı Kalma Tarihi alınamadı")
        pass


def contribution_helpfulness_al(data, r):
    # Contributions and Helpfulness
    try:
        span_contr_help = r.find_all("span", {"class": "phMBo"})
        if span_contr_help is not None:
            for span in span_contr_help:
                if 'contribution' in span.parent.text:
                    data['Contribution'] = span.text.split(' ')[0]
                elif 'helpful' in span.parent.text:
                    data['HelpfulVotes'] = span.text.split(' ')[0]
    except:
        print("Contribution / Helpful Votes alınamadı")
        pass


def seyahat_turunu_al(data, r):
    # trip type
    # < span class ="eHSjO _R Me" >
    #   < span class ="trip_type_label" > Trip type: </span >
    #   Traveled as a couple < / span >
    try:
        TripType = r.find("span", {'class': 'trip_type_label'})
        if TripType is not None:
            TripType = TripType.next_sibling
            if TripType is not None:
                data['TripType'] = TripType
    except:
        print("Kalma Türü alınamadı")
        pass


def konuk_detayli_puanlari_al(data, r):
    # scores için bu olmalı
    # <div class="fFwef S2 H2 cUidx">
    #   <span class="YDXMO Nd">
    #       <span class="ui_bubble_rating bubble_50"></span>
    #   </span><span>Value</span>
    # </div>
    try:

        divs = r.find_all("div", {'class': 'WWOoy'})
        if divs is not None:
            for div in divs:
                score_name = div.text
                score = str(int(div.span.span.attrs['class'][-1].split('_')[-1]) / 10.0)
                data['UDS_' + score_name] = score
    except:
        print("Kullanıcı Detaylı Puanları alınamadı")
        pass


def otelin_cevabini_al(data, r):
                    # Hotel Response
                    try:
                        div_response = r.find("div", {'class':'ajLyr'})
                        if div_response is not None:
                            div_header = div_response.find("div", {'class':'nNoCN'} )
                            header = div_header.text.replace(div_header.div.text, '')
                            ResponseDate = div_header.div.text.split('Responded')[-1].strip()
                            # ResponseDate = div_response.find("div", {'class':'mzAim'}).text.split('Responded')[-1].strip() if div_response.find("div", {'class':'mzAim'}) else None
                            span_resp_text = div_response.find("span", {'class':'MInAm'})
                            response_text = span_resp_text.span.prettify().replace('<span>', '').replace('<br/>', '').replace('</span>','').replace('\n \n', '')
                            data['ResponseHeader'] = header
                            data['ResponseDate'] = ResponseDate
                            data['ResponseText'] = response_text
                            # print('yanıt:', response_text)
                    except:
                        pass


def resimleri_al(driver, data, r, rCount):
    # resimler
    try:
        split_text= 'https://dynamic-media-cdn.tripadvisor.com/media/'
        # resimlerin varlığı için ilk yol
        # div_pictures = r.find("div", {'class': 'pDrIj'})
        # if div_pictures is not None:

        # resimlerin varlığı için ikinci yol. HR_CC_CARD divi (yani r)
        # 3 elemanlı ise resim var; 2 elemanlı ise resim yok demektir.
        if len(list(r.children)) > 2:  # resim var ise
            element = driver.find_elements(By.XPATH, '//div[@data-test-target="HR_CC_CARD"]')[rCount]
            # ikinci div resimleri kapsıyor
            cnt = 1
            driver.execute_script("arguments[0].scrollIntoView();", element)  # elemana scroll etmezsek
            driver.implicitly_wait(wait_time /2, )
            sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

            for img in element.find_element(By.XPATH,'./div[2]').find_elements(By.TAG_NAME, 'img'):
                a = img.get_attribute('src').split('?')[0]

                data['Image_' + str(cnt)] = a.split(split_text)[-1]
                cnt += 1

    except:
        pass



def dil_secenekleri_divini_ver(driver, url ):
    """
    'Diğer' metinli divi verir ya da dillerin listelendiği <ul> nesnesini verir.
    Yorumlar çok az dilde ise 'Diğer' divi bulunmaz. Bu durumda, dillerin bulunduğu <ul> elemanından yararlanarak
    mevcut diller alınmalıdır.


    :return div_diğer, ul
    ya div_diğer ya da ul nesnesi None olur. 'Diğer' divi var ise ul nesnesi None'dır; ya da tersi.
    """
    try:
        click_and_press_esc(driver)
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

        div_rev_filters = get_element(driver, 'hrReviewFilters', by='id')
        column_dil = div_rev_filters.find_elements(By.CLASS_NAME, 'ui_column')[-1]
        ul_dil = column_dil.find_element(By.TAG_NAME,'ul')
        try:
            div = ul_dil.find_element(By.TAG_NAME, 'div')  # 'Diğer' metninin yazıldığı div
        # span_diger = div.find_element(By.TAG_NAME, 'span')
            return div, None
        except Exception as ex:
            # print('Dil seçenekleri divi bulunamadı. Muhtemelen az sayıda dilde yorum var. Dillerin olduğu <ul> nesnesi '
            #       'döndürülecek ve div_diger ise None değerine sahip olacak')
            return None, ul_dil

    except Exception as ex:
        # print('Dil seçenekleri divi ve diller kısmı bulunamadı. didiger ve ul elemanı None olarak döndürülecek')
        return None, None

        # print('Dil seçenekleri divi bulunamadı. otelin sayfası yenien yükelenerek tekrar denenecek')
        # otel_sayfasini_ac(driver, url)
        # hosgeldiniz_penceresini_kapat(driver)
        # click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
        #
        # try:
        #     click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
        #     div_rev_filters = get_element(driver, 'hrReviewFilters', by='id')
        #     column_dil = div_rev_filters.find_elements_by_class_name('ui_column')[-1]
        #     ul_dil = column_dil.find_element_by_tag_name('ul')
        #     div = ul_dil.find_element(By.TAG_NAME, 'div')  # 'Diğer' metninin yazıldığı div
        #     # span_diger = div.find_element(By.TAG_NAME, 'span')
        #     return div
        # except Exception as ex:
        #     print('Dil seçenekleri divi bulunamadı. Muhtemelen az sayıda dilde yorum var. Dillerin olduğu <ul> nesnesi '
        #           'döndürülecek.')
        #     return ul_dil
        # except Exception as ex:
        #     print('Sayfa Yeniden yüklenmesine rağmen Div Seçenekleri divi bulunamadı. Hata şuydu: \n', ex, '\n')
        #     return None



def dilleri_listele(driver, div_diller, ul_diller ):
    # driver.execute_script("arguments[0].scrollIntoView();", div_diller)
    # move_mouse_to_element(driver, div_diller)
    sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

    if div_diller is not None: # 'Diğer' menti bulunan div var ise

        # bazen gizlilik kabulü gibi mesajlar, pop-up'lar çıktığı için
        # div e tıklanamıyor. engellemek için
        try:
            div_diller.click()

        except:
            sleep_a_while(sleep_min=sleep_min /2, sleep_max=sleep_max/2)
            click_and_press_esc(driver)
            click_accept_button(driver)
            div_diller.click() #

        div_menu_diller = driver.find_element(By.CLASS_NAME, 'TocEc')
        diller = div_menu_diller.find_elements(By.TAG_NAME, 'li')[1:] # ilki tüm diller seçeneğidir.
        # text_diller_listesi = [dil.text.split(' ')[0] for dil in diller if 'İngilizce' not in dil.text] #ingilizceyi çıkar
        text_diller_listesi = [dil.text.split(' ')[0] for dil in diller] #tüm diller. ingilizce dahil
        click_and_press_esc(driver)
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        return text_diller_listesi
    else: #bu durumda dil sayısı az olduğu için ul_diller elemanında listelenen dilleri alacağız
        li_diller = ul_diller.find_elements(By.TAG_NAME, 'li')  # diller li elemanlarında yazılı
        li_diller =  [x for x in li_diller if 'Tüm diller' not in x.text]
        text_diller_listesi = [dil.find_element(By.TAG_NAME, 'span').text for dil in li_diller]  # tüm diller. ingilizce dahil
        click_and_press_esc(driver)
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        return text_diller_listesi



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


def dili_sec(driver, div_diger_diller, ul_diller, text_dil=None ):
    # driver.execute_script("arguments[0].scrollIntoView();", div_diger_diller)
    # div_diger_diller.find_element(By.TAG_NAME, 'span').click()
    # move_mouse_to_element(driver, div_diger_diller)
    # move_mouse_to_mid_window(driver)
    if div_diger_diller is None and ul_diller is None:
        print('Diğer diller divi ve dilleri listeleyen ul elemanı mevcut değil!')
        return False
    click_and_press_esc(driver)
    sleep_a_while(sleep_min=sleep_min/2, sleep_max=sleep_max/2)  # better to sleep a while
    click_and_press_esc(driver)

    if div_diger_diller is not None:
        div_diger_diller.click()
        # sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        div_menu_diller = driver.find_element(By.CLASS_NAME, 'TocEc')
        diller = div_menu_diller.find_elements(By.TAG_NAME, 'li')[1:] # ilki tüm diller seçeneğidir.

        for dil in diller:
            if text_dil == dil.text.split(' ')[0]:

                if dil.find_element(By.TAG_NAME, 'input').is_selected():
                    click_and_press_esc(driver)
                else:
                    dil.click()

                sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
                return True

    else:
        li_diller = ul_diller.find_elements(By.TAG_NAME, 'li')  # diller li elemanlarında yazılı
        li_diller = [x for x in li_diller if 'Tüm diller' not in x.text]

        for li in li_diller:
            if text_dil == li.find_element(By.TAG_NAME, 'span').text:
                click_and_press_esc(driver)
                li.click()
                sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
                return True

    return False


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


def ceviri_mi(r):
    try:
        q = r.find("div", {'class': "IGEcd"})  # varsa bu yorum bir çeviridir
        if q is not None:
            # print('Bu bir çeviridir. Geçiliyor...')
            return True
    except:
        pass
    try:
        # sitenin kendi çevirisi olup olmadığı bu divdeki metinde yaıyor
        q = r.find("div", {'class': "XCJRC"})  #

        if q is not None:
            if 'Orijinalini görüntüleyin' in q.text:
                # print('Bu bir TripAdvisor çevirisidir. Geçiliyor...')
                return True
    except:
        pass

    return False


def parse_reviews(driver, hotel_id, url):
    df = pd.DataFrame()
    hosgeldiniz_penceresini_kapat(driver)
    click_and_press_esc(driver) # arada pop-up falan çıkarsa diye
    click_accept_button(driver)

    div_diger_diller, ul_diller = dil_secenekleri_divini_ver(driver, url )

    if div_diger_diller is None and ul_diller is None:
        print('\nDillerle ilgili hiçbir buton bulunamadı. Muhtemelen bu otelin yorum bilgilerine erişilemiyor.'
              'Bu otel geçilecek...\n')
        return None

    click_and_press_esc(driver) # arada pop-up falan çıkarsa diye
    text_diller_listesi = dilleri_listele(driver, div_diger_diller, ul_diller) # div_diger_diller, None ise hata yapacak ve devam etmeyecek
    #bir şekilde, dil_secenekleri_divini_ver fonksiyonu bu divi bazen bulamıyor. Bulamadığında None olacağı için
    # dilleri_listele fonksiyonunda hata ile karşılaşılıyor. kasıtlı olarak bu fonksiyonda bu hata meydana gelirse
    #bu otelden yeniden deva metmek üzere işin yarıda kesilmesini istiyorum.

    print(text_diller_listesi)
    first = True

    for text_dil in text_diller_listesi:

        click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
        div_diger_diller, ul_diller = dil_secenekleri_divini_ver(driver, url) # diğer diller divi

        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.TAG_NAME, 'body'))
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
        hosgeldiniz_penceresini_kapat(driver)
        click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
        sleep_a_while(sleep_min=sleep_min /2, sleep_max=sleep_max /2)  # better to sleep a while
        click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
        if not dili_sec(driver, div_diger_diller, ul_diller, text_dil):
            print('dil bulunamadı!', text_dil)
            continue
        print('[', text_dil, ']')

        click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
        makine_cevirisini_kapat(driver)

        nReviews = get_element(driver, "hkxYU").text.split(' ')[0] if get_element(driver,"hkxYU") is not None else None

        if nReviews is not None:
            nReviews =int(nReviews.replace(',','').replace('.',''))
        else:
            print('Yorum Sayısı bulunamadı! Bu bir otel olmayabilir.')
            nReviews = 0

        sayfa =1
        # sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        nReviewsOfLanguage =0

        while True:
            try:
                sleep_a_while(sleep_min=sleep_min / 2, sleep_max=sleep_max /2)  # better to sleep a while
                driver.implicitly_wait(wait_time / 2, )
                click_and_press_esc(driver)  # arada pop-up falan çıkarsa diye
                makine_cevirisini_kapat(driver)
                sleep_a_while(sleep_min=sleep_min / 2, sleep_max=sleep_max /2)  # better to sleep a while

                read_more_butonuna_bas(driver)
                driver.implicitly_wait(wait_time / 2, )
                # WebDriverWait(driver, wait_time / 2 )
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                reviews = soup.find_all('div', {'data-test-target':"HR_CC_CARD"})

                if reviews is None:
                    print("Hiçbir Yorum Bulunamadı! Otel ID:", hotel_id)
                    yorum_olmayanlari_yaz(hotel_id, download_dir)
                    return None # devam etmeye gerek yok. Metoddan çık

                rCount= 0  # to track nth review
                for r in reviews:

                    if ceviri_mi(r): # bu bir çeviri yorumu ise devam etme
                        rCount += 1 #resimlerin olduğu yorumun sırasını takip etmek için artır
                        continue

                    driver.implicitly_wait(wait_time /2 , )
                    sleep_a_while(sleep_min=sleep_min /2, sleep_max=sleep_max / 2)  # better to sleep a while

                    data = dict()
                    data['Language'] = text_dil
                    data["HotelID"] = hotel_id

                    kullanici_id_al(data, r)
                    yorum_id_al(data, r)
                    kullanici_bolgesini_al(data, r)
                    yorum_tarihi_al(data, r)
                    puan_balonlari_al(data, r)
                    yorum_basligini_al(data, r)
                    yorum_metnini_al(data, r)
                    konaklama_tarihini_al(data, r)
                    contribution_helpfulness_al(data, r)
                    seyahat_turunu_al(data, r)
                    konuk_detayli_puanlari_al(data, r)
                    otelin_cevabini_al(data, r)
                    resimleri_al(driver, data, r, rCount)

                    if first:
                        df = pd.DataFrame.from_records(data, columns=data.keys(), index=[0])
                        first = False
                    else:
                        tmp =  pd.DataFrame.from_records(data, columns=data.keys(), index=[0])
                        df = pd.concat([df, tmp])

                    rCount +=1
                    nReviewsOfLanguage += 1

                # next butonu var mı?
                try:
                    btnNext = None
                    if int(nReviews) <= 4:
                        break
                    btnNext = driver.find_element(By.XPATH, "//a[text()='Sonraki']")
                    if btnNext is not None and 'disabled' not in btnNext.get_attribute('class'):
                        # print("Sonraki sayfaya geçiliyor...")
                        btnNext.click()

                    else: # < span class ="ui_button nav next primary disabled" > Next < / span >
                        print("Next button cannot be found or disabled. Terminating...")
                        break
                except:
                    if df is not None and df.shape[0]>0:
                        print(nReviewsOfLanguage, text_dil, " yorum alındı.")
                        break
                        # return df
                    else:
                        # return None
                        print('Bilinmeyen bir sorun oluştu. Dil: ', text_dil)
                        break
                        pass

            except Exception as e:
                print("Yorumlar bulunamadı.")
                print('\nHata şuydu:', e, "\n\n")
                yorum_olmayanlari_yaz(hotel_id)
                return None

            sayfa  +=1

    if df is not None and df.shape[0]>0:
        print("\n", df.shape[0], " yorum alındı.\n")
        return df
    else:
        return None


def get_hotel_information(region_id, hotel_id, driver, url):
    hotel_data = dict()

    otel_sayfasini_ac(driver, url)
    # sleep_a_while(sleep_min=sleep_min / 2, sleep_max=sleep_max / 2)  # better to sleep a while

    hotel_data['RegionID'] = region_id
    hotel_data['HotelID'] = hotel_id
    hotel_data['Name'] = get_element(driver, "HEADING", "id").text if get_element(driver, "HEADING", "id") is not None else None
    # about divi yoksa muhtemelen otel değil. Bu id 'debir otel yok
    # otelin adı yoksa muhtemelen bu bir otel değil.
    if hotel_data['Name'] is None or 'Antalya Otelleri ve Kalacak Yerler' in hotel_data['Name']:
        return None

    print("\n", "Hotel ID:", hotel_id, '\tName: ', hotel_data['Name'], "\n")

    hotel_data['Star'] = get_element(driver, "JXZuC").get_attribute('aria-label').split(' of 5 bubbles')[0] if get_element(driver, "JXZuC ") is not None else None
    hotel_data['Reviews'] = get_element(driver, "qqniT").text.split(' ')[0] if get_element(driver, "qqniT") is not None else None
    hotel_data['Rank'] = get_element(driver, "cGAqf").text.replace('#', '').replace(',','') if get_element(driver, "cGAqf") is not None else None
    hotel_data['Address'] = get_element(driver, "ERCyA").text if get_element(driver, "ERCyA") is not None else None

    # About Section
    hotel_data['Rating'] = get_element(driver, "uwJeR").get_attribute('innerHTML') if get_element(driver, "uwJeR") is not None else None
    parse_about(hotel_data, driver) # location, cleanlines, service, value puanları

    try:
        div_reviews_tab = driver.find_element(By.XPATH, '//div[@data-test-target="reviews-tab"]')

        if div_reviews_tab is not None:
            div_reviews_tab = div_reviews_tab.find_element(By.CLASS_NAME, 'lXxJN')
            sp = BeautifulSoup(div_reviews_tab.get_attribute('innerHTML'), 'html.parser')

            for li in sp.div.div.findAll('li', {'class': 'XpoVm'}):
                key = li.label.text
                value = list(li.children)[-1].text
                hotel_data[key] = value
    except:
        pass
    #
    # with codecs.open('d:/' + 'Istanbul' + '_oteller_bilgileri.txt', 'a', encoding='utf8') as cikti:
    #     yazici = csv.DictWriter(cikti, hotel_data.keys() )
    #     yazici.writerow(hotel_data)
    return hotel_data


# chromedriver_path = r"D:\Software\chromedriver.exe"
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

    file_hotel = join(download_dir, region_name + "_hotels.feather")
    file_yorum = join(download_dir, region_name + "reviews.feather")
    first = True
    df_review = df_hotel = None
    n_periyot = 1

    ntotal= len(data)
    # last_index = hotelIDs.index(kalinan) # kalinan index
    last_index = 2000
    count =  last_index

    for count in range(last_index, len(data)):#[hotelIDs[x] for x in [1,38, 39]]:
        # id= 507978# 507977
        print('#%d/%d' % (count +1, ntotal), end=',  ')

        region_id = data.iloc[count].RegionID
        hotel_id = data.iloc[count].HotelID

        url = url_root + str(region_id) + "-d" + str(hotel_id)

        driver = get_browser(chromedriver_path, download_dir)
        driver.set_window_size(width, height)

        hotel_data = get_hotel_information(region_id, hotel_id, driver, url)

        #hotel_data None ise, bu id de bir otel yok demektir. sonraki otele eç
        if hotel_data is None:
            print("Bu ID'ye (", str(id), ") sahip bir otel yok! Geçiliyor...\n")
            sleep(.2)
            write_last_index(count, download_dir)
            continue

        reviews = parse_reviews(driver, hotel_id, url)
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
            driver.close()
            sleep(.5)
            write_or_append_data(df_hotel, file_hotel)
            write_or_append_data(df_review, file_yorum)

            first = True
            df_hotel = None
            df_review = None

            gc.collect()
            # sleep(1)
            # driver = get_browser(chromedriver_path, download_dir)
            # driver.set_window_size(1400, 1000)
            # sleep(1)
            # driver.maximize_window()
            # driver.minimize_window()

        write_last_index(count, download_dir)
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

    data = pd.read_feather(data_file)
    data = data.drop_duplicates()
    main(data, region_name, download_dir )


