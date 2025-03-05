
import os
from Scraper import Scraper
from Cleaner import Cleaner
from Analyser import Analyser

import uuid # add run ID

RAW_DATASET_PATH  = "./raw_dataset"
# RAW_DATA_SET = "gpt2.csv"
# RAW_DATA_SET = "realestate_com_au_250117.csv"
RAW_DATA_SET = "realestate_com_au_southeast_suburbs_250305.csv"
# RAW_DATA_SET = "test2.csv"

PROCESSED_DATASET_PATH  = "./processed_dataset"

#uuid str as run id
uuid_str = str(uuid.uuid4()).upper()

raw_dataset_location = os.path.join(RAW_DATASET_PATH, RAW_DATA_SET)
processed_dataset_path = PROCESSED_DATASET_PATH

cleaner = Cleaner(raw_dataset_location,PROCESSED_DATASET_PATH, uuid_str)
cleaner.clean_dat_shit()

scraper = Scraper(cleaner.prepped_df, uuid_str)
scraper.scrape_dat_shit()


# ------------------------------------------------
# post processing
analyser = Analyser(uuid = uuid_str, prepped_df_file_path=cleaner.prepped_df_path, scrapped_df_path=scraper.scraped_df_path)
analyser.merger()
analyser.update_status()


