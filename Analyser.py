import pandas as pd

ASSETS_DIR = "./assets"
SOCIAL_PROFILE =ASSETS_DIR + "Northern_Social.csv"

from geo_social import check_geo_social_addresses


class Analyser():
    # def __init__(self, clean_data, ambiguous_data, scraped_data, unsuccessful_data, uuid):
    def __init__(self, uuid = None, prepped_df_file_path= None, scrapped_df_path= None):
        # self.clean_data = clean_data
        # self.ambiguous_data  = ambiguous_data
        # self.scraped_data = scraped_data
        # self.unsuccessful_data = unsuccessful_data
        #self.uuid = uuid

        #self.raw_data_path = raw_data_path
        #self.scraped_data_path = 
        self.uuid = uuid
        self.prepped_df_file_path = prepped_df_file_path
        self.scrapped_df_path =scrapped_df_path

        # wont be available until the merger method is run
        self.merged_df = pd.DataFrame()
        

    def merger(self):
        '''
        Merge scraped data with clean data
        '''
        prepped_data_df = pd.read_excel(self.prepped_df_file_path,index_col='Unnamed: 0')

        scraped_data_df = pd.read_excel(self.scrapped_df_path, index_col='Index')
        scraped_data_df.rename(columns={"Input Address":"Address"},  inplace=True)

        self.merged_df = pd.merge(prepped_data_df,scraped_data_df, how= 'left', left_index=True, right_index=True, suffixes=("_clean", "_scraped"))

        #print(merged_df )


    
    def update_status(self):
        self.merged_df.loc[((self.merged_df['Address_scraped'].isna()) | (self.merged_df['Address_scraped'] == ''))  & (self.merged_df['Status'] != 'Ambiguous'), 'Status'] = 'Unsuccessful'

        self.merged_df.loc[(~self.merged_df['Address_scraped'].isna()) & (self.merged_df['Address_scraped'] != '') & (self.merged_df['Status'] == 'To be Scraped'), 'Status'] = 'Successful'

        # write the df to excel
        self.merged_df.to_excel("./output_dataset" + f"/{self.uuid}_merged.xlsx", index=True)

    def make_easy_to_read(self):

        ''''
        Place holder to make the output excel easier to read
        '''
        pass


    
    def run_geo_social(self):
        '''NOT DONE
        '''
        output_df = pd.read_excel("./output_dataset" + f"/{self.uuid}_merged.xlsx", index_col='Unnamed: 0')

        input_geo_social_profile_df = pd.read_csv("H:\\My Drive\\House_Hunting\\Scraper\\assets\\Northern_Social.csv")
        geo_social_profile_df = input_geo_social_profile_df[["SA1", "Percent (%)"]]

        list_of_address = output_df["Address_clean"]
        output_geo_df = check_geo_social_addresses(list_of_address)


        merged_df = output_df.merge(
            output_geo_df,
            left_on='Address_clean',  # Column name in output_df
            right_on='address',       # Column name in addresses_with_sa1
            how='left'                # Keep all rows from output_df
        )

        merged_df = merged_df.drop(columns=['address'])

        # merged_df.rename({"SA1_CODE21":"SA1"}, inplace=True, axis=1)

        merge_df_with_percentage = merged_df.merge(
            geo_social_profile_df,
            left_on='SA1_CODE21',  # Column name in output_df
            right_on='SA1',       # Column name in addresses_with_sa1
            how='left'                # Keep all rows from output_df
        )


        merge_df_with_percentage = merge_df_with_percentage.drop(columns=['SA1'])
        
        # Check for NaN values in SA1_CODE to identify unmatched addresses
        unmatched_count = merge_df_with_percentage['SA1_CODE21'].isna().sum()
        print(f"Number of addresses without matching SA1 code: {unmatched_count}")   

        merge_df_with_percentage.to_excel("./output_dataset" + f"/{self.uuid}_merged_social_housing.xlsx", index=True)


def format_output(self):  
    # merge_df_with_percentage.to_excel("./output_dataset" + f"/{self.uuid}_merged_social_housing.xlsx", index=True)
    pass
    

        

# if __name__ == "__main__":
#     analyser = Analyser()
#     analyser.adhoc_run_geo_social()
