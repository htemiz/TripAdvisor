from selenium.webdriver.common.by import By
from .helpers import parse_about
from ..utils.utils import get_element, open_page
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_hotel_information(region_id, hotel_id, driver, url):
    hotel_data = dict()

    open_page(driver, url)
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
        div_reviews_tab = driver.find_element(By.XPATH, '//div[@data-test-target="hotels-tab"]')

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
