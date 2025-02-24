import pandas as pd

class Analyser():
    # def __init__(self, clean_data, ambiguous_data, scraped_data, unsuccessful_data, uuid):
    def __init__(self, uuid):
        # self.clean_data = clean_data
        # self.ambiguous_data  = ambiguous_data
        # self.scraped_data = scraped_data
        # self.unsuccessful_data = unsuccessful_data
        self.uuid = uuid

    def merger(self):
        '''
        Merge scraped data with clean data
        '''
        #HACK risky index column
        clean_data_df = pd.read_csv("./processed_dataset" + "/ac72ca18-6202-495e-87a3-4b2d17f389b2_clean_data.csv",index_col='Unnamed: 0')

        scraped_data_df = pd.read_excel("./processed_dataset" + "/ac72ca18-6202-495e-87a3-4b2d17f389b2_scraped-2025-23-01-20-17-29.xlsx", index_col='Index')
        scraped_data_df.rename(columns={"Input Address":"Address"},  inplace=True)

        merged_df = pd.merge(clean_data_df,scraped_data_df, how= 'left', left_index=True, right_index=True, suffixes=("_clean", "_scraped"))

        #print(merged_df )
        merged_df.to_excel("./output_dataset" + "/ac72ca18-6202-495e-87a3-4b2d17f389b2_output_20250123-201729.xlsx", index=True)

        

if __name__ == "__main__":
    analyser = Analyser('dummy')
    analyser.merger()
