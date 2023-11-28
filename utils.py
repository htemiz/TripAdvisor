from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service

sleep_min = .15
sleep_max = .25
slp_factor = 15
slp_small_factor = 7.5

def sleep_a_while(factor= 1.0, sleep_min = sleep_min, sleep_max = sleep_max):
    sleep(sleep_min * factor)
    # sleep( ((sleep_max-sleep_min) * random() + sleep_min ) * factor)



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



"""
"""
def parse_img_url(url):

    parts = url.split("https//", True)[0].split(' ')[0].split('?')[0]

    path = parts.split('.')
    ext = path[-1] # extension (like jpg)
    part_slashes = path[2].split('/')

    #name of file designated after all / 's )
    name = part_slashes[-1]
    hex_name = "".join(part_slashes[-5:-1])
    return name, hex_name, ext
