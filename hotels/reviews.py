from config import configuration
from utils.utils import *
from .language import *
from bs4 import BeautifulSoup
from .helpers import *

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
                    print("Hiçbir Yorum Bulunamadı! Dil: ", text_dil)
                    # yorum_olmayanlari_yaz(hotel_id, download_dir)
                    break # devam etmeye gerek yok.

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
                    # if int(nReviews) <= 4:
                    #     break
                    btnNext = driver.find_element(By.XPATH, "//a[text()='Sonraki']")
                    if btnNext is not None and 'disabled' not in btnNext.get_attribute('class'):
                        # print("Sonraki sayfaya geçiliyor...")
                        btnNext.click()
                    else: # < span class ="ui_button nav next primary disabled" > Next < / span >
                        print("Next button either is disabled or not clickable. Passing to next language...")
                        break
                except Exception as e:
                    print(nReviewsOfLanguage, text_dil, " yorum alındı.")
                    break

            except Exception as e:
                print( "\n\n", text_dil, " dilindeki yorumlar alınırken şu hata ile karşılaşıldı:\n", e, "\n\n" )
                yorum_olmayanlari_yaz(hotel_id)
                break

            sayfa  +=1

    if df is not None and df.shape[0]>0:
        print("\n", df.shape[0], " yorum alındı.\n")
        return df
    else:
        return None
