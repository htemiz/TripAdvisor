
from config import configuration
from config.update import update_config
from sys import argv
from hotels.reviews import *
from hotels.parse import get_hotel_information
from hotels.reviews import parse_reviews
from utils.utils import get_browser, write_last_index, write_or_append_data
import pandas as pd
from time import sleep
from os.path import abspath
import gc

from region.find_hotels import get_hotels_of_region


width, height = configuration['width'], configuration['height']
file_type = configuration['file_type']

chromedriver_path = "crawler/chromedriver.exe"



if __name__ == "__main__":
    region_id, region_name  = argv[1], argv[2]
    if len(argv) ==4:
        download_dir = argv[3]
    else:
        download_dir = "../data/"

    # chromedriver_path = "../crawler/chromedriver.exe"
    driver = get_browser(chromedriver_path, download_dir)

    get_hotels_of_region(driver, region_id, region_name, download_dir, star=5,
                                   page='oa30', sleep_min=4, sleep_max=5 )

