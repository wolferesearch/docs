DATEFMT='%Y%m%d'

import os
import pandas as pd
class FactorLibraryReader:
    
    def __init__(self, path = 'equityfactor_daily'):
        self.path = path
        self.corr_factors_date = {'EV_FACTORS': '20220117',
                                  'GRO_FL_YLD': '20200318',
                                  'NEWS_SENT': '20200327'}
        self.corr_factors = list(self.corr_factors_date.keys())
        self.corr_path = "{}/corrections".format(self.path)
        self.corr_path_factors = "{}/others".format(self.corr_path)
        
    def _filename_(self, region, date, factor = None):
        fmt = date.strftime(DATEFMT)
        if factor is None:
            return '{}_{}.csv'.format(region,fmt)
        else:
            if factor == 'EV_FACTORS': 
                return '20220117/{}_{}_{}.csv'.format(region,factor,fmt)    
            else: 
                return '{}_{}_{}.csv'.format(region,factor,fmt)
    
    def _path_(self, region, date, path = None):
        if path is None:
            path = self.path
        return "{}/{}/{}".format(path,date.strftime('%Y'),self._filename_(region,date))
    
    def _corr_files_(self,region,date):
        """
            Loads regular correction files
        """
        path = "{}/{}".format(self.corr_path,date.strftime('%Y'))
        if not os.path.exists(path):
            return None
        
        corr_dates = os.listdir(path)
        if len(corr_dates) == 0:
            return None
        
        files = [[corr_dates,
                  '{}/{}/{}'.format(path,corr_date,self._filename_(region,date)) ,
                  'Regular']
                 for corr_date in corr_dates]
        
        df = pd.DataFrame(files)
        df.columns = ['Date','File','Type']
        
        df = df[[os.path.isfile(x) for x in df.File]]
        if len(df) == 0:
            return None
        
        return df
    
    def _factor_correction_(self,region,date,factor):
        """
            Gets factor corrections
        """
        file = "{}/{}/{}".format(self.corr_path_factors,factor,self._filename_(region,date,factor))
        if os.path.isfile(file):
            return [self.corr_factors_date[factor],file,'Factor']
        return None
    
    def _all_factor_corrections_(self,region,date):
        factor_corr = [self._factor_correction_(region,date,factor) for factor in self.corr_factors]
        factor_corr = [i for i in factor_corr if i is not None]
        if len(factor_corr) == 0:
            return None
        else:
            df = pd.DataFrame(factor_corr)
            df.columns = ['Date','File','Type']
            return df
        
    
    def all_corrections(self, region, date):
        files = self._corr_files_(region,date)
        if files is None:
            return self._all_factor_corrections_(region,date)
        
        factor_corr = self._all_factor_corrections_(region,date)
        if factor_corr is None:
            return files
        df = pd.concat(files,factor_corr)
        return df.sort_values(by=['Date'])
    
    def _apply_correction_(self, df, file):
        col_index = df.columns
        
        print("Applying Correction {}".format(file))
        df_corr = pd.read_csv(file)
        df_corr.drop('DATE',axis=1,inplace = True)
        corr_cols = list(df_corr.columns)
        corr_cols.remove('SEDOL')
        
        old_cols = [x + '_x' for x in corr_cols]
        new_cols = [x + '_y' for x in corr_cols]
        
        df1 = df.merge(df_corr, on='SEDOL', how='left')
        
        df1.drop(old_cols, inplace=True, axis=1)
        ucols = dict(map(lambda i,j : (i,j) , new_cols,corr_cols))
        df1.rename(columns=ucols, inplace=True)
        
        return df1[col_index.tolist()]
        
    
    def get_corrected_data(self, region, date):
        """
            Returns corrected data by reading through correction in order
        """
        corrections = self.all_corrections(region,date)
        if corrections is None:
            # No corrections
            return pd.read_csv(self._path_(region,date))
        
        last_index = len(corrections)-1
        if corrections.Type[last_index] == 'Regular':
            # If the last file is a regular correction just return that
            print("Reading last regular correction file {}".format(corrections.File[last_index]))
            return pd.read_csv(corrections.File[last_index])
        
        regular_corr_idx = corrections.index[corrections.Type == 'Regular']
        if len(regular_corr_idx) > 0:
            # Use the last regular correction
            last_index = regular_corr_idx[len(regular_corr_idx)-1]
            df = pd.read_csv(corrections.File[last_index])
            print("Reading last regular correction file {}".format(corrections.File[last_index]))
            corrections = corrections.iloc[(last_index+1):]
            # Truncate the corrections
        else:
            # No Regular Corrections
            df = pd.read_csv(self._path_(region,date))
        
        if len(corrections) == 0:
            return df
        
        # Apply Factor correction
        for file in corrections.File:
            df = self._apply_correction_(df,file)
        return df
