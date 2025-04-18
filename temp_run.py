
import os
from Scraper import Scraper
from Cleaner import Cleaner
from Analyser import Analyser

import uuid # add run ID

# ------------------------------------------------
# post processing
analyser = Analyser(uuid = '2B7FC21F-92E4-4C00-9D15-58DB23894344', prepped_df_file_path='./processed_dataset\\2B7FC21F-92E4-4C00-9D15-58DB23894344_prepped_dataset.xlsx', scrapped_df_path='./processed_dataset/2B7FC21F-92E4-4C00-9D15-58DB23894344_scraped_20250321-063656.xlsx')
#analyser.merger()
#analyser.update_status()

analyser.run_geo_social()



