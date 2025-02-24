
import os
from Scraper import Scraper
from Cleaner import Cleaner

import uuid # add run ID

RAW_DATASET_PATH  = "./raw_dataset"
# RAW_DATA_SET = "gpt2.csv"
# RAW_DATA_SET = "realestate_com_au_250117.csv"
# RAW_DATA_SET = "realestate_com_au_250117 - Copy.csv"
RAW_DATA_SET = "realestate_com_au_northern_suburbs_250123.csv"

PROCESSED_DATASET_PATH  = "./processed_dataset"

#uuid str as run id
uuid_str = str(uuid.uuid4())

raw_dataset_location = os.path.join(RAW_DATASET_PATH, RAW_DATA_SET)
processed_dataset_path = PROCESSED_DATASET_PATH

cleaner = Cleaner(raw_dataset_location,PROCESSED_DATASET_PATH, uuid_str)
cleaner.clean_dat_shit()

scraper = Scraper(cleaner.clean_df, uuid_str)
scraper.scrape_dat_shit()


# ------------------------------------------------
# post analyser 

