from config import configuration
from utils.utils import click_and_press_esc, sleep_a_while, get_element, click_accept_button
from utils.utils import sleep_min, sleep_max
from selenium.webdriver.common.by import By



def dil_secenekleri_divini_ver(driver, ):
    """
    'Diğer' metinli divi verir ya da dillerin listelendiği <ul> nesnesini verir.
    Yorumlar çok az dilde ise 'Diğer' divi bulunmaz. Bu durumda, dillerin bulunduğu <ul> elemanından yararlanarak
    mevcut diller alınmalıdır.


    :return div_diğer, ul
    ya div_diğer ya da ul nesnesi None olur. 'Diğer' divi var ise ul nesnesi None'dır; ya da tersi.
    """
    try:
        click_and_press_esc(driver)
        sleep_a_while(sleep_min=sleep_min*1.5, sleep_max=sleep_max*1.5)  # better to sleep a while

        div_rev_filters = get_element(driver, 'hrReviewFilters', by='id')
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        column_dil = div_rev_filters.find_elements(By.CLASS_NAME, 'ui_column')[-1]
        ul_dil = column_dil.find_element(By.TAG_NAME,'ul')
        try:
            div = ul_dil.find_element(By.TAG_NAME, 'div')  # 'Diğer' metnin yazıldığı div
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

        try:
            div_menu_diller = driver.find_element(By.CLASS_NAME, 'TocEc')
        except Exception as  ex:
            print('\nDiller Menüsü bulunamadı. Hata şuydu:\n', ex, '\n\n')
            return None

        diller = div_menu_diller.find_elements(By.TAG_NAME, 'li')[1:] # ilki tüm diller seçeneğidir.
        # text_diller_listesi = [dil.text.split(' ')[0] for dil in diller if 'İngilizce' not in dil.text] #ingilizceyi çıkar
        diller = [x for x in diller if '(0)' not in x.text] # yorumu olmayan dilleri alma
        text_diller_listesi = [dil.text.split(' ')[0] for dil in diller] #tüm diller. ingilizce dahil
        click_and_press_esc(driver)
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        return text_diller_listesi
    else: #bu durumda dil sayısı az olduğu için ul_diller elemanında listelenen dilleri alacağız
        li_diller = ul_diller.find_elements(By.TAG_NAME, 'li')  # diller li elemanlarında yazılı
        li_diller =  [x for x in li_diller if 'Tüm diller' not in x.text and '(0)' not in x.text]
        text_diller_listesi = [dil.find_element(By.TAG_NAME, 'span').text for dil in li_diller]  # tüm diller. ingilizce dahil
        click_and_press_esc(driver)
        sleep_a_while(sleep_min=sleep_min, sleep_max=sleep_max)  # better to sleep a while
        return text_diller_listesi


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


