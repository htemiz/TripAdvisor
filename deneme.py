import pandas as pd
from parse_hotels_with_reviews import main
from region.find_hotels import get_hotels_of_region
from utils.utils import get_browser

#
# region_id, region_name  = '28930', 'Florida'
# download_dir = "../data/"
# chromedriver_path = "crawler/chromedriver.exe"
# driver = get_browser(chromedriver_path, download_dir)
#
# get_hotels_of_region(driver, region_id, region_name, download_dir, star=5,
#                                page='oa00', sleep_min=3, sleep_max=5 )
#



download_dir = "../data/"
# chromedriver_path = "crawler/chromedriver.exe"
# driver = get_browser(chromedriver_path, download_dir)

# find_hotels.get_hotels_of_region(driver, '28930', 'Florida', download_dir )

data_file = "../data/Florida/Hotels_in_Florida_Region.feather"

data = pd.read_feather(data_file)
data = data.drop_duplicates()

main(data, 'Florida', download_dir )

a=5