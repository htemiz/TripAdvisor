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
import pandas as pd
from utils import *
import gc
from os import getcwd, listdir, makedirs
from os.path import join, abspath, basename, dirname, exists


url_user_prefix = 'https://www.tripadvisor.com/Profile/'

def get_element(driver, name, by='class'):
    found = False
    element = None
    try:
        if by =='class':
            element = driver.find_element_by_class_name(name)
        elif by =='id':
                element = driver.find_element_by_id(name)
        found = True
        return element

    except:
        if found:
            return element

        return None

def click_accept_button(driver):
    # print('Accept buton içindeyiz')

    try:
        #btn_accept = driver.find_element_by_id( 'onetrust-accept-btn-handler')

        btn_accept = driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']")

        if btn_accept is not None:
            btn_accept.click()

            driver.execute_script("arguments[0].click();", btn_accept)

    except:
        pass


def click_and_press_esc(driver):

    try:
        btn_accept = driver.find_element_by_id('_evidon-accept-button')
        if btn_accept is not None:
            btn_accept.click()

    except:
        pass

    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def parse_about(data, driver, ):


    try:
        div_about = driver.find_element_by_xpath("//div[@data-tab='TABS_ABOUT']")
    except:
        print('The element TABS_ABOUT cannot be found! Returning without parsing the about section')
        return


    # div_about.find_element_by_class_name("cmZRz")

    s = BeautifulSoup(div_about.get_attribute('innerHTML'),  'lxml')

    r = s.find_all("div", {"class":"yplav"})

    if r is not None and len(r) >0:
        for e in r:
            try:
                cls = str(int(e.span.attrs['class'][-1].split('_')[-1] )/ 10.0)
                key = "R" + e.div.text

                data[key] = cls
            except:
                pass


def parse_reviews(driver, hotel_id):
    sleep_min = .95
    sleep_max = 1.75
    wait_time = 1.75

    df = pd.DataFrame()

    first = True
    tag_reviews ='qqniT'
    nReviews = int(get_element(driver,tag_reviews ).text.split(' ')[0].replace(',','')) if get_element(driver,tag_reviews) is not None else None

    sayfa =1
    sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

    while True:
        # print("Sayfa:", sayfa)
        try:
            sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
            driver.implicitly_wait(wait_time, )

            try:
                tag_read_more = 'Ignyf'
                read_more = driver.find_element_by_class_name(tag_read_more) # 'eljVo') eskisi
                if read_more is not None:
                    read_more.click()
            except:
                try:
                    driver.implicitly_wait(wait_time, )
                    # sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

                    read_more = driver.find_element_by_class_name(tag_read_more) # 'eljVo') eskisi
                    if read_more is not None:
                        read_more.click()
                except:
                    # print("Hiç Bir Yorum Bilgisi Bulunamadı: otelID:", hotel_id)
                    yorum_olmayanlari_yaz(hotel_id, download_dir)
                    pass

            driver.implicitly_wait(wait_time, )
            WebDriverWait(driver, wait_time)

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            reviews = soup.find_all('div', {'data-test-target':"HR_CC_CARD"})

            if reviews is None:
                print("Hiçbir Yorum Bulunamadı! Otel ID:", hotel_id)
                yorum_olmayanlari_yaz(hotel_id)
                return None # devam etmeye gerek yok. Metoddan çık

            rCount= 0  # to track nth review
            for r in reviews:
                data = dict()
                data["HotelID"] = hotel_id

                try:
                    a  = r.find("a", {'class':'uyyBf'})
                    if a is not None:
                        userID = a.attrs['href'].split('/')[-1]
                        data['UserID'] = userID
                except:
                    print("Kullanıcı ID'si alınamadı")
                    pass

                try:
                    div_rev_id  = r.find("div", {'class':'WAllg _T'})
                    if div_rev_id is not None:
                        revID = div_rev_id.attrs['data-reviewid']
                        data['ReviewID'] = revID
                except:
                    print("Yorum ID'si alınamadı")
                    pass

                # user region
                try:
                    span_region = r.find("span", {'class': 'LXUOn'})
                    if span_region is not None:

                        data['UserRegion'] = span_region.text
                except:
                    print("Kullanıcı Bölgesi alınamadı")
                    pass

                # Review Date
                try:
                    a_review_date = r.find("a", {'class': 'uyyBf'})
                    if a_review_date is not None:

                        data['ReviewDate'] = a_review_date.next_sibling.split(' wrote a review ')[-1]
                except:
                    print("Kullanıcı Yorum Tarihi alınamadı")
                    pass

                # puan balonları
                try:
                    # div = r.find("div", {'class': 'cqoFv'})  # with data-reviewid attribute, eski yöntem
                    div =  r.find('div', {'data-test-target': 'review-rating'})

                    if div is not None:
                        userRating = str(int(div.span.attrs['class'][-1].split('_')[-1]) / 10.0)
                        data['UserRating'] = userRating
                except:
                    print("Kullanıcı puanı alınamadı")
                    pass


                #review başlık
                #<div class="fpMxB MC _S b S6 H5 _a" dir="ltr" data-test-target="review-title">
                #   <a href="/ShowUserReviews-g293974-d15398698-r669762411-Istanbul_In_Hotel-Istanbul.html" class="fCitC" dir="">
                #       <span><span>Scam! Terrible</span></span></a></div>
                try:
                    # div = r.find("div", {'class':'KgQgP'})
                    div = r.find("div", {'data-test-target':'review-title'})
                    if div is not None:
                        rTitle = div.span.span.text
                        data['Title'] = rTitle
                except:
                    print("Kullanıcı Yorum Başlığı alınamadı")
                    pass

                # yorum
                # < q class ="XllAv H4 _a" >
                # < span > text here ...
                try:
                    q = r.find("q", {'class':'QewHA'})
                    if q is not None:
                        rText = q.span.text
                        data['Text'] = rText
                except:
                    print("Kullanıcı Yorum Metni alınamadı")
                    pass

                # data of stay
                # <span class="euPKI _R Me S4 H3">
                #   <span class="CrxzX">Date of stay:</span>
                # April 2019</span>
                try:
                    # span = r.find("span", {'class':'teHYY'})
                    span = r.find('span', text='Date of stay:')

                    if span is not None:
                        rStayDate = span.next_sibling.strip()
                        data['StayDate'] = rStayDate
                except:
                    print("Kullanıcı Kalma Tarihi alınamadı")
                    pass

                # Contributions and Helpfulness
                try:
                    span_contr_help = r.find_all("span", {"class":"yRNgz"})
                    if span_contr_help is not None:
                        for span in span_contr_help  :
                            if 'contribution' in span.parent.text:
                                data['Contribution'] = span.text
                            elif 'helpful' in span.parent.text:
                                data['HelpfulVotes'] = span.text
                except:
                    print("Contribution / Helpful Votes alınamadı")
                    pass
                #trip type
                # < span class ="eHSjO _R Me" >
                #   < span class ="trip_type_label" > Trip type: </span >
                #   Traveled as a couple < / span >
                try:
                    span = r.find("span", {'class':'trip_type_label'})
                    if span is not None:
                        # TripType = span.text.split(':')[-1].strip()
                        TripType = span.next_sibling
                        data['TripType'] = TripType
                except:
                    print("Kalma Türü alınamadı")
                    pass

                # scores için bu olmalı
                # <div class="fFwef S2 H2 cUidx">
                #   <span class="YDXMO Nd">
                #       <span class="ui_bubble_rating bubble_50"></span>
                #   </span><span>Value</span>
                # </div>
                try:

                    divs = r.find_all("div", {'class':'ZzICe'})
                    if divs is not None:
                        for div in divs:
                            score_name = div.text
                            score = str(int(div.span.span.attrs['class'][-1].split('_')[-1]) / 10.0)
                            data['UDS_'+ score_name] = score
                except:
                    print("Kullanıcı Detaylı Puanları alınamadı")
                    pass

                # Hotel Response
                try:
                    div_response = r.find("div", {'class':'ajLyr'})
                    if div_response is not None:
                        div_header = div_response.find("div", {'class':'nNoCN'} )
                        header = div_header.text.replace(div_header.div.text, '')
                        ResponseDate = div_header.div.text.split('Responded')[-1].strip()
                        # ResponseDate = div_response.find("div", {'class':'mzAim'}).text.split('Responded')[-1].strip() if div_response.find("div", {'class':'mzAim'}) else None
                        span_resp_text = r.find("span", {'class':'MInAm'})
                        response_text = span_resp_text.span.prettify().replace('<span>', '').replace('<br/>', '').replace('</span>','').replace('\n \n', '')
                        data['ResponseHeader'] = header
                        data['ResponseDate'] = ResponseDate
                        data['ResponseText'] = response_text
                        # print('yanıt:', response_text)
                except:
                    pass


                # resimler
                try:

                    # resimlerin varlığı için ilk yol
                    # div_pictures = r.find("div", {'class': 'pDrIj'})
                    # if div_pictures is not None:

                    #resimlerin varlığı için ikinci yol. HR_CC_CARD divi (yani r)
                    # 3 elemanlı ise resim var; 2 elemanlı ise resim yok demektir.
                    if len(list(r.children)) >2: # resim var ise
                        element = driver.find_elements_by_xpath('//div[@data-test-target="HR_CC_CARD"]')[rCount]
                        pics = element.find_elements_by_class_name('KSVvt')
                        if pics is not None and len(pics) > 0:
                            cnt = 1
                            for img in pics:
                                a = img.get_attribute('src')
                                data['Image_' + str(cnt)] = a
                                # print(a)
                                cnt += 1

                except:
                    pass

                if first:
                    df = pd.DataFrame.from_records(data, columns=data.keys(), index=[0])
                    first = False
                else:
                    df = df.append(data, ignore_index=True, )

                rCount +=1

            # next butonu var mı?
            try:
                btnNext = None

                # toplam yorum sayısı 4'ten az ise bu sayfa harici bir sayfa aramaya gerek yok
                if int(nReviews) <= 4:
                    break

                div_reviews_tab = driver.find_element_by_xpath('//div[@data-test-target="reviews-tab"]')
                btnNext = div_reviews_tab.find_element_by_class_name('next')

                if btnNext is not None:
                    # print("Sonraki sayfaya geçiliyor...")
                    btnNext.click()
                    # sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while

                else: # < span class ="ui_button nav next primary disabled" > Next < / span >
                    print("Next button cannot be found. Terminating searching reviews for this hotel...")
                    break
                # else:
                #     print("Pagination cannot be found! Probably no review for hotel ID:", hotel_id , " Terminating...")
                #     break

            except:
                try:
                    # btnNext = div.find_element_by_xpath("//span[text()='Next']")
                    btnNext = driver.find_element_by_class_name('next')

                    if  btnNext is not None:
                        print("End of reviews.")
                        break
                    else:
                        if df is not None and df.shape[0]>0:
                            print(df.shape[0], " yorum alındı.")
                            return df
                        else:
                            return None
                except:
                    if df is not None and df.shape[0]>0:
                        print(df.shape[0], " yorum alındı.")
                        return df
                    else:
                        return None

        except:
            # print("Yorumlar bulunamadı.")
            yorum_olmayanlari_yaz(hotel_id)
            return None

        sayfa  +=1

    if df is not None and df.shape[0]>0:
        print(df.shape[0], " yorum alındı.")
        return df
    else:
        return None



def get_hotel_information(region_id, hotel_id, driver):
    hotel_data = dict()

    url_root= "https://www.tripadvisor.com/Hotel_Review-g"
    url = url_root + str(region_id) + "-d" + str(hotel_id)

    driver.get(url)
    driver.implicitly_wait(5)
    click_accept_button(driver)
    driver.implicitly_wait(2)
    click_and_press_esc(driver)


    hotel_data['RegionID'] = region_id
    hotel_data['HotelID'] = hotel_id
    hotel_data['Name'] = get_element(driver, "HEADING", "id").text if get_element(driver, "HEADING", "id") is not None else None
    print("Hotel ID:", hotel_id, hotel_data['Name'])

    hotel_data['Star'] = get_element(driver, "euDRl").find_element_by_tag_name('svg').get_attribute('aria-label').split(' of 5 bubbles')[0] if get_element(driver, "euDRl") is not None else None
    hotel_data['Reviews'] = get_element(driver, "qqniT").text.replace(',','').split(' ')[0] if get_element(driver, "qqniT") is not None else None
    hotel_data['Rank'] = get_element(driver, "cGAqf").text.replace('#', '').replace(',','').split(' ')[0] if get_element(driver, "cGAqf") is not None else None
    hotel_data['Address'] = get_element(driver, "fHvkI").text if get_element(driver, "fHvkI") is not None else None

    # About Section
    hotel_data['Rating'] = get_element(driver, "IHSLZ ").text if get_element(driver, "IHSLZ ") is not None else None
    parse_about(hotel_data, driver)

    try:
        div_reviews_tab = driver.find_element_by_xpath('//div[@data-test-target="reviews-tab"]')

        if div_reviews_tab is not None:
            list_traveler_ratings = div_reviews_tab.find_element_by_class_name('LojWi')
            sp = BeautifulSoup(list_traveler_ratings.get_attribute('innerHTML'), 'html.parser')

            traveler_ratings = sp.find_all('li')
            for li in traveler_ratings:
                hotel_data['Rating_' + li.label.text] =  li.find('span', {'class': 'NLuQa'}).text
    except:
        pass
    #
    # with codecs.open('d:/' + 'Istanbul' + '_oteller_bilgileri.txt', 'a', encoding='utf8') as cikti:
    #     yazici = csv.DictWriter(cikti, hotel_data.keys() )
    #     yazici.writerow(hotel_data)
    reviews  = parse_reviews(driver, hotel_id)

    return hotel_data, reviews


def find_next_button(driver):

    # div = driver.find_element_by_class_name("prw_common_standard_pagination_resp")
    try:
        btnNext = driver.find_element_by_xpath('//div[@data-trackingstring="pagination_h"]//a[text()="Next"]')

    except:
        return None

    return btnNext

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


chromedriver_path = r"D:\programlar\chromedriver 103.exe"
download_dir = r"D:\calisma\projeler\tripadvisor\data"



def parse_user(driver, user_id, ):

    user_data = dict()
    user_pictures_list = list() # kullanıcının tüm resimleri. {<user_id, review_id, img_url>}
    review_data_list = list()  # kullanıcının yorumları listesi

    user_data['contributions'] = get_element(driver, 'Skngi')


    # kullanıcı bilgisi başlık bölümündeki contrib, followers, follow kısmı
    div_cff = driver.find_element_by_class_name("BNUSk")
    span_cff_list = div_cff.find_elements_by_class_name("rNZKv")
    cff_keys = ['contributions', 'followers', 'follow']
    for i, k in enumerate(span_cff_list):
        user_data[cff_keys[i]] = k.text


    # ana div
    div_ana_icerik = driver.find_element_by_class_name('XLQnn')
    div_sol_intro = div_ana_icerik.find_element_by_xpath('./div[3]/div[1]/div/div[2]') # soldaki Intro kısmı
    # div_content = div_ana_icerik.find_element_by_xpath('./div[3]/div[2]') # sağdaki yorumlar kısmı
    div_content = driver.find_element_by_id('content') # sağdaki yorumlar kısmı. id ile bul

    user_data['location']  = div_ana_icerik.find_element_by_xpath('./div[3]/div[1]/div/div[2]/span[1]').text if div_ana_icerik.find_element_by_xpath('./div[3]/div[1]/div/div[2]/span[1]') is not None else None
    user_data['joined']  = div_ana_icerik.find_element_by_xpath('./div[3]/div[1]/div/div[2]/span[2]').text if div_ana_icerik.find_element_by_xpath('./div[3]/div[1]/div/div[2]/span[2]') is not None else None
    user_data['joined'] = user_data['joined'].split('Joined in')[-1].strip()


    # çok fazla review varsa 'Show more' butonu çıkıyor.
    # bu butona basarak tüm yorumların sayfaya gelmesini bekleyelim.
    # sonra parse edelim.
    while True:
        try:
            btn_show_more = div_content.find_element_by_xpath('./div[2]/*//span[contains(text(),"Show more")]')
            if btn_show_more:
                btn_show_more.click()
                sleep_a_while(3)
            else:
                break
        except:
            break


    # her bir review
    div_reviews = div_content.find_elements_by_xpath("./div/child::*")

    for rev_div in div_reviews: # her bir reviewi gezelim:

        sleep_a_while(.2)

        dict_review_data = dict()
        dict_review_data['user_id'] = user_id

        """
            bu divin altında 4 div var.
            1. div, <kullanıcı> wrote a review cümlesi ve tarih bilgisini barındırıyor
            2. div, yorum bilgilerini ve resimleri barındırıyor.
            3. div, kesikli çizgi satırı
            4. div, helpful, save ve share butonlarının olduğu kısım
            
        """

        r = rev_div.find_element_by_xpath('./div/div/div') #birinci div

        dict_review_data['review_date'] = r.find_element_by_xpath('./div/div/div[3]').text \
            if r.find_element_by_xpath('./div/div/div[3]').text is not None else None # tarih bilgisinin olduğu div

        # resim ve yorumların olduğu div (ikinci div)
        r = rev_div.find_element_by_xpath('./div/div/div[2]') # ikinci div

        # resim divi var mı ?
        resimler_var = len(r.find_elements_by_xpath('./div')) == 3 # üç div var ise resimler var

        # resimler var ise yorumlar ikinci div'de bulunuyor. Diğer türlü birinci divde
        str_idx = '2' if resimler_var else '1'
        dict_review_data['review_title'] = r.find_element_by_xpath('./div['  + str_idx + ']/div/a/div/div[1]').text
        print('Yorum Başlığı: ', dict_review_data['review_title'])

        # yorum_url = r.find_element_by_xpath('./div[2]/div/a').get_attribute('href')
        yorum_url = r.find_element_by_xpath('./div[' + str_idx + ']/div/a').get_attribute('href')
        dict_review_data['review_url'] = yorum_url
        dict_review_data['hotel_id'] = yorum_url.split('-d')[-1].split('-r')[0] # yorum yapılan otelin id'si
        dict_review_data['hotel_region_id'] = yorum_url.split('-g')[-1].split('-')[0] # yorum yapılan otelin id'si
        dict_review_data['review_id'] = yorum_url.split('-r')[-1].split('-')[0] # yorum id'si
        div_yorum = r.find_element_by_xpath('./div[' + str_idx + ']/div/a/div').text

        # kullanıcı puanı class niteliği içerisinde; örneğin, bubble_50 şeklinde en sonda veriliyor.
        str_span_rating = r.find_element_by_xpath('./div[' + str_idx + ']/div/a/div/span').get_attribute('class').split(' ')[-1].split('_')[-1]
        dict_review_data['user_rating'] = str(int(str_span_rating)/10)



        #   kullanıcının tam yorumunu yorum_url'den almak daha iyi  ---- #
        #   Örnek:
        #   'https://www.tripadvisor.com/ShowUserReviews-g641737-d6619150-r825478360-Hotel_Abelhof-Neukirchen_am_Grossvenediger_Austrian_Alps.html'
        #   adresindeki sayfadan çekilebilir.
        #
        dict_review_data['reivew'] = r.find_element_by_xpath('./div['  + str_idx + ']/div/a/div/div[2]').text
        dict_review_data['stay_date'] = r.find_element_by_xpath('./div['  + str_idx + ']/div/a/div/div[3]').text.split(':')[-1].strip()


        # RESİMLER VAR MI?
        if resimler_var : # resimler listesi var ise

            ul_resimler = r.find_element_by_xpath('./div/div/a/div/ul')

            try:
                # kaç adet resim var? ul'nin parentinin son elemanı olan div bu bilgiyi tutuyor.
                str_n_imgs = ul_resimler.find_element_by_xpath('../div[last()]').text
                n_imgs = int(str_n_imgs.split('/')[-1])

            except:
                print('Kaç adet resim olduğunu metinden bulmada hata! resim adedini veren metin şu: ', str_n_imgs)
                print('Resimler alınmadan devam ediliyor...')
                continue

            #
            # kullanıcının yüklediği tüm resimler sayfada hazır değil.
            # next butonuna tıklayarak hepsini gezince hazır hale geliyorlar.
            # bu aşamdan sonra tüm resimlere ait bilgileri almak mümkün olacak.
            #
            e = ul_resimler.find_element_by_xpath('../div[2]')

            #user_id butonun olduğu yere inelim
            # driver.execute_script("arguments[0].scrollIntoView(true);", e)

            # pencere minimize edilmişse görünür hale getirilmeli. yoksa resimler indirilmiyor.
            if driver.execute_script("return document.hidden"):
                driver.switch_to_window(driver.current_window_handle)

            div_to_scroll = rev_div.find_element_by_xpath('./div/div/div[2]')  # ikinci div
            driver.execute_script("arguments[0].scrollIntoView();", div_to_scroll)


            for i in range(n_imgs):

                driver.execute_script("arguments[0].click();", e)
                sleep(.15)

            sleep_a_while(.1)
            # driver.minimize_window()

            # artık resimleri alabiliriz
            # kullanıcının bu otel için yüklediği resimler
            resimler = r.find_elements_by_xpath('./div/div/a/div/ul//*//img') # tüm resimler
            print('Linki bulunan resim sayısı: ', len(resimler))
            resim_urller = [x.get_attribute('src') for x in resimler] # resimlerin yolları
            # resim_urller = [x.split('https://dynamic-media-cdn.tripadvisor.com/media/photo-o/')[-1] for x in resim_urller]
            for res_url in resim_urller:
                res_url = res_url.split('https://dynamic-media-cdn.tripadvisor.com/media/photo-o/')[-1].split('?')[0]

                user_pictures_list.append((user_id, dict_review_data['review_id'], res_url))


        else:
            print('\tBu yorumda resim bulunamadı.')

        review_data_list.append(dict_review_data)

    return  user_data, review_data_list, user_pictures_list


user_ids = [
            'Olavi1955',
            'jakudocz',
            'Patricianilsson',
            'tresario',
            'Colyman',
            'mimiclarke98',
            'sarna002',
            'gorgeous44',
            'Clacken',
            '707zeynel_',
            'jimbobs0_0'
            ]

def main():

    #   ----        ----    #
    # pencereyi ilk açım için
    driver = get_browser(chromedriver_path, download_dir)
    # driver.maximize_window()

    count = 0
    first = True

    df_review = df_user = None

    for user_id in user_ids:
        url = url_user_prefix + str(user_id)
        driver.get(url)

        (a, b) = (5, 2) if first else (2,1)
        driver.implicitly_wait(a)
        click_accept_button(driver)
        driver.implicitly_wait(b)
        click_and_press_esc(driver)
        # driver.minimize_window()
        #   ----        ----    #

        user_data, reviews, images = parse_user(driver, user_id)
        user_data['user_id'] = user_id

        if first:
            df_user = pd.DataFrame.from_records(user_data, columns=user_data.keys(), index=[0])
            df_review = pd.DataFrame.from_records(reviews, columns=reviews[0].keys(),)
            df_images = pd.DataFrame.from_records(images, columns=('user_id', 'review_id', 'img_id'))
            first = False

        else:
            df_user = df_user.append( user_data, ignore_index=True)

            if reviews is not None:
                if df_review is not None:
                    df_tmp_review = pd.DataFrame.from_records(reviews, columns=reviews[0].keys(), )

                    df_review = pd.concat([df_review, df_tmp_review], ignore_index=True, sort=False)
                else:
                    df_review = df_tmp_review


            if images is not None:
                if df_images is not None:
                    df_tmp_images =  pd.DataFrame.from_records(images, columns=('user_id', 'review_id', 'img_id'))

                    df_images = pd.concat([df_images, df_tmp_images], ignore_index=True, sort=False)
                else:
                    df_images = df_tmp_images


            if count % n_periyot == 0:  # her n_periyot adet kullanıcıda bir kayıt yap
                driver.close()
                save_data(df_user, df_review, file_hotel, file_yorum, download_dir)

                first = True
                df_user = None
                df_review = None

                gc.collect()
                sleep(1)
                driver = get_browser(chromedriver_path, download_dir)
                sleep(3)
                driver.maximize_window()
                driver.minimize_window()

        # write_last_index(count -1, download_dir)

        count +=1
        # sleep(2)

    try:
        save_data(df_user, df_review, file_hotel, file_yorum, download_dir)

        # df_user.to_excel('d:/otel_bilgileri.xlsx')
        # df_review.to_excel('d:/yorum_bilgileri.xlsx')
    except:
        print("Feather dosyalarını yazarken hata ile karşılaşıldı")
        return



if __name__ == '__main__':
    main()