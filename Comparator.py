import pandas as pd

class Comparator():

    def __init__(self, previous_raw_file_path, current_raw_file_path):
        self.previous_raw_file_path = previous_raw_file_path
        self.current_raw_file_path = current_raw_file_path

    def compare(self):
        '''
        compare two raw datasets from REA of different weeks 
        '''
        previous_raw_data_df = pd.read_csv(self.previous_raw_file_path)
        current_raw_data_df = pd.read_csv(self.current_raw_file_path)

        # Initialize changes_raw_df with contents from previous_raw_data_df
        changes_raw_df = previous_raw_data_df.copy()

        # Add Status column initialized with 'Unchanged'
        changes_raw_df['Status'] = 'Unchanged'

        # Get unique addresses from both dataframes
        previous_addresses = set(previous_raw_data_df['Address'])
        current_addresses = set(current_raw_data_df['Address'])

        # Find deleted addresses (in previous but not in current)
        deleted_addresses = previous_addresses - current_addresses
        changes_raw_df.loc[changes_raw_df['Address'].isin(deleted_addresses), 'Status'] = 'Deleted'

        # Find new addresses (in current but not in previous)
        new_addresses = current_addresses - previous_addresses
        # For new addresses, we need to append rows from current_raw_data_df
        new_rows = current_raw_data_df[current_raw_data_df['Address'].isin(new_addresses)].copy()
        new_rows['Status'] = 'New'

        # Concatenate the existing changes_raw_df with new rows
        changes_raw_df = pd.concat([changes_raw_df, new_rows], ignore_index=True)
        changes_raw_df.to_csv("CHANGED_RAW.CSV", index= False)

        # TODO translate this into the scrape dataset

        # 

        # 

RAW_DATASET_PATH  = "./raw_dataset/"

if __name__ == "__main__":
    previous_raw_file_path = RAW_DATASET_PATH+ "realestate_com_au_northern_suburbs_250123.csv"
    current_raw_file_path = RAW_DATASET_PATH+ "realestate_com_au_northern_suburbs_250207.csv"
    comparator = Comparator(previous_raw_file_path=previous_raw_file_path, current_raw_file_path=current_raw_file_path)
    comparator.compare()
