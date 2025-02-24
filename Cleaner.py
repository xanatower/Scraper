import pandas as pd
import os


class Cleaner():

    def __init__(self, raw_dataset_location, processed_dataset_path, uuid):
        #empty df
        self.raw_dataset_location = raw_dataset_location
        self.dirty_df = pd.read_csv(self.raw_dataset_location)
        self.clean_df = pd.DataFrame()
        self.ambiguous_df= pd.DataFrame()
        self.processed_dataset_path = processed_dataset_path
        self.uuid = uuid


    def clean_dat_shit(self):

        # Remove any apostrophes from the Address column
        self.dirty_df['Address'] = self.dirty_df['Address'].str.replace("'", "", regex=False)

        # Create a new column 'Suburb' by extracting the part after the last comma
        self.dirty_df['Suburb'] = self.dirty_df['Address'].str.split(',').str[-1].str.strip()

        # Identify rows where the Address column contains brackets
        ambiguous_mask = self.dirty_df['Address'].str.contains(r"\(", regex=True)

        # Store rows with brackets in ambiguous_df
        self.ambiguous_df = self.dirty_df[ambiguous_mask].copy()

        # Store rows without brackets in clean_df
        self.clean_df = self.dirty_df[~ambiguous_mask].copy()

        # Display or save the DataFrames as needed
        # print("Clean DataFrame:")
        # print(self.clean_df.head())

        # print("Ambiguous DataFrame:")
        # print(self.ambiguous_df.head())

        # Optionally save the DataFrames to CSV files
        clean_df_filename = self.uuid+"_"+"clean_data.xlsx"
        ambiguous_df_filename  = self.uuid+"_"+"ambiguous_data.xlsx"
        self.clean_df.to_excel(os.path.join(self.processed_dataset_path,clean_df_filename), index=True)
        self.ambiguous_df.to_csv(os.path.join(self.processed_dataset_path,ambiguous_df_filename), index=True)
