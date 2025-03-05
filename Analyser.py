import pandas as pd

class Analyser():
    # def __init__(self, clean_data, ambiguous_data, scraped_data, unsuccessful_data, uuid):
    def __init__(self, uuid, prepped_df_file_path, scrapped_df_path):
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

        

# if __name__ == "__main__":
#     analyser = Analyser('dummy')
#     analyser.merger()
