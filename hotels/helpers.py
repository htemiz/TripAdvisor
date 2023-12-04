from selenium.webdriver.common.by import By
from ..utils.utils import sleep_a_while,  sleep_max, sleep_min, wait_time
from ..utils.utils import click_and_press_esc


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


def parse_about(data, driver, ):
    try:
        div_about = driver.find_element(By.XPATH,"//div[@data-tab='TABS_ABOUT']")
        # div_about = driver.find_element_by_xpath("//div[@data-placement-name='hr_community_content:ssronly']")
    except:
        print('The element TABS_ABOUT cannot be found! Returning without hotels the about section')
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

def get_region_id_and_name_from_url(url_and_name):
    """give region id and hotel id from given hotel url"""
    t = url_and_name[0].split('-g')[-1].split('-')[0:2]
    region = t[0]
    id = t[1].replace('d','')
    return region, id, url_and_name[1]

def parse_img_url(url):

    parts = url.split("https//", True)[0].split(' ')[0].split('?')[0]

    path = parts.split('.')
    ext = path[-1] # extension (like jpg)
    part_slashes = path[2].split('/')

    #name of file designated after all / 's )
    name = part_slashes[-1]
    hex_name = "".join(part_slashes[-5:-1])
    return name, hex_name, ext


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
