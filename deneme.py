import pandas as pd
from parse_hotels_with_reviews import main

download_dir = "../data/"
# chromedriver_path = "crawler/chromedriver.exe"
# driver = get_browser(chromedriver_path, download_dir)

# find_hotels.get_hotels_of_region(driver, '28930', 'Florida', download_dir )

data_file = "../data/Florida/Florida_hotels.feather"

data = pd.read_feather(data_file)
data = data.drop_duplicates()

main(data, 'Florida', download_dir )

a=5