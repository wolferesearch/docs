import pandas as pd
from gics_util import build_sector_universe
from RankAnalyzer import RankAnalyzer
from RankAnalyzer import rankdb_dynamic

# Quick function to get pandas data frame. !Caution! The function uses global variable references
def get_r3k_hist_data(env, year, starting_gics, min_mktcap, exclude_gics, method = 'z_normal'):
    analyzer = RankAnalyzer(env, 'r3k_hist_' + str(year))
    return analyzer.get_filtered_data(starting_gics = starting_gics, start_date = str(year)+'-01-31', 
                                       end_date = str(year+4) + '-12-31', min_mktcap = min_mktcap, 
                                      exclude_gics = exclude_gics, method = method)

### Name: Features Data Deep History with Alternative Data
### Description: Notebook illustrates how to extract data from saved files
###              and combine it with other singnals
### Steps
###         1. Initialize LQuant
###         2. Get Saved Data From Historical Files (/mnt/ebs1/data/rankdb)
###         3. Fetch Alternative Data and cast it to RankDB format
###         4. Join all data to get a final data frame

class R3KDataFetcher:
    def __init__(self, wq, starting_gics, latest_db = 'r3k_scores_20200831', end_date = '2020-08-30', 
                 exclude_gics = [], min_mktcap = 1e9, method = 'z_normal'):
        self.wq = wq
        self.starting_gics = starting_gics
        self.exclude_gics = exclude_gics
        self.end_date = end_date
        self.min_mktcap = min_mktcap
        self.method = method
        
        # 1. Concatenate all historical data into one Pandas data frame
        all_hist_data = pd.concat([get_r3k_hist_data(env = wq.env(), year = 1987 + 5*y1, 
                                                     starting_gics = starting_gics, 
                                                     min_mktcap = min_mktcap, 
                                                     exclude_gics = exclude_gics, 
                                                     method = method) for y1 in list(range(4))])
        # 2. Load up Current
        analyzer = RankAnalyzer(self.wq.env(), latest_db)
        
        curr_data = analyzer.get_filtered_data(starting_gics = starting_gics, start_date = '2007-01-31', 
                                       end_date = '2020-08-31', min_mktcap = 1e9, exclude_gics = exclude_gics)
        
        # 3. Concatenate the all historic data and current data
        all_data = pd.concat([all_hist_data,curr_data])
        
        self.wq.env().clean_temp_var()
        
        self.all_data = all_data
    
    def append_data(self, start_date, factors, freq = '1me'):
        """
            Appends Data to all_data member object
        """
        
        univ_id = build_sector_universe(wq = self.wq, id = 'Custom_Universe_10', starting_univ = 'USC_2668795', 
                      starting_gics = self.starting_gics, start_date = start_date, 
                      min_mktcap = self.min_mktcap,
                      end_date = self.end_date, freq = freq, exclude_gics = self.exclude_gics)
        
        data2 = self.wq.get_data(self.wq.new_request().runFor(univ_id).start('2007-01-31')
                    .to(self.end_date).at('1me').attr(*factors).a('COMPANYNAME')
                    .a('TICKER').a('MKTCAP').a('GSUBIND').a('FXRATE_USD')
                    .a('BETA_LOCAL').a('IN_USC_2668795').a('IN_USC_2668794').addForwardReturn().addInFlag())
        
        analyzer = rankdb_dynamic(env = self.wq.env(), data = data2,   subindices = {'Russell 1K' : 'IN_USC_2668794'})
        alt_data = analyzer.get_filtered_data(starting_gics = self.starting_gics, start_date = start_date, 
                                       end_date = self.end_date, min_mktcap = self.min_mktcap, exclude_gics = self.exclude_gics, 
                                             method = self.method)
        self.wq.env().run("rm({})".format(data2.name()))
        
        self.all_data = self.all_data.merge(right = alt_data[['DATE','TICKER',*factors]], how = 'left', 
                                            on = ['DATE','TICKER'])
        
        self.wq.env().clean_temp_var()
        return True

