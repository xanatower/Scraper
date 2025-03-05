import pandas as pd
import os


class Cleaner():

    '''
    Preprocessing
    '''

    def __init__(self, raw_dataset_location, processed_dataset_path, uuid):
        #empty df
        self.raw_dataset_location = raw_dataset_location
        self.dirty_df = pd.read_csv(self.raw_dataset_location)
        # self.clean_df = pd.DataFrame()
        # self.ambiguous_df= pd.DataFrame()
        self.prepped_df = pd.DataFrame()
        self.processed_dataset_path = processed_dataset_path
        self.uuid = uuid

        # Wait until the end to fill
        self.prepped_df_path = None


    def clean_dat_shit(self):

        ambiguous_df = pd.DataFrame()
        clean_df = pd.DataFrame()

        # Remove any apostrophes from the Address column
        self.dirty_df['Address'] = self.dirty_df['Address'].str.replace("'", "", regex=False)

        # Create a new column 'Suburb' by extracting the part after the last comma
        self.dirty_df['Suburb'] = self.dirty_df['Address'].str.split(',').str[-1].str.strip()

        # Identify rows where the Address column contains brackets OR "Address available on request"
        brackets_mask = self.dirty_df['Address'].str.contains(r"\(", regex=True)
        address_on_request_mask = self.dirty_df['Address'].str.contains("Address available on request", case=False, na=False)
        exclamation_mark_mask = bargin_mask = self.dirty_df['Address'].str.contains("!", case=False, na=False)
        bargin_mask = self.dirty_df['Address'].str.contains("bargin", case=False, na=False)

        ambiguous_mask = brackets_mask | address_on_request_mask | bargin_mask | exclamation_mark_mask

        # Store rows with brackets or "Address available on request" in ambiguous_df
        ambiguous_df = self.dirty_df[ambiguous_mask].copy()

        # Store remaining rows in clean_df
        clean_df = self.dirty_df[~ambiguous_mask].copy()

        # 
        ambiguous_df['Status'] = 'Ambiguous'
        clean_df['Status'] = 'To be Scraped'

        # 
        self.prepped_df = pd.concat([clean_df, ambiguous_df], axis=0)
        prepped_df_filename = self.uuid + "_" + "prepped_dataset.xlsx"
        self.prepped_df.to_excel(os.path.join(self.processed_dataset_path, prepped_df_filename), index=True)
        self.prepped_df_path = os.path.join(self.processed_dataset_path, prepped_df_filename)
        # Save the DataFrames to files
        # clean_df_filename = self.uuid + "_" + "clean_data.xlsx"
        # ambiguous_df_filename = self.uuid + "_" + "ambiguous_data.xlsx"
        # self.clean_df.to_excel(os.path.join(self.processed_dataset_path, clean_df_filename), index=True)
        # self.ambiguous_df.to_excel(os.path.join(self.processed_dataset_path, ambiguous_df_filename), index=True)