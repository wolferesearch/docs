from lquantPy.LQuant import BaseWrap, LQEnv

def drop_dataset(wq, table_name):
  prep = DataPrep(wq = wq, file = '/mnt/ebs1/karora/test/Test2.csv', table_name = table_name, idcol = 'TICKER', datecol = 'DATE', staleness = '1d')
  return prep.drop()
  
class DataPrep(BaseWrap):
  """
    Data Preparation Class for Uploading the CSV Data
    
    :param wq: LQuant Handle
    :param file: Location of CSV File
    :param table_name: Table (Key) where data to be stored. Should be unique
    :param idcol: Identifier Column (e.g., TICKER, SEDOL)
    :param stalenss: Staleness parameter for the data (e.g., 1d, 1m)
  """
  def __init__(self, wq, file, table_name, idcol, datecol,  staleness):
    BaseWrap.__init__(self, wq.env(), 't1__loader')
    print('Initializing Data Preparation')
    env = wq.env()
    self.wq = wq
    env.run('source("/mnt/ebs1/data/common/R/DataPrep.R")')
    self.env.set(self.handle, 'ltool.DataPrep$new',
                     tableName = LQEnv._quote(table_name),
                     idCol = LQEnv._quote(idcol),
                     dateCol = LQEnv._quote(datecol),
                     csvFile = LQEnv._quote(file),
                     staleness = LQEnv._quote(staleness))
    print(self.msg())

  """
    Returns 1 if there is an error in the execution
  """
  def has_errors(self):
    return self._get('hasErrors()').as_double_array()[0]
    
  """
     Prints the last error message
  """
  def msg(self):
    if self.has_errors() == 0.0:
      return(None)
    else:
      return(self._get('msg'))

  """
      Sets the date column to index. Index starts with 1
      :param indx: Index of Date Column (First Column: 1)
  """
  def set_date_col(self, indx):
    self._invoke('setDateCol',indx)
    return(True)

  def delete_cache(self):
    self._invoke('deleteCache')
    return(True)

  """
      Loads the new schema based on the CSV file
  """
  def load(self):
    self._invoke('load')
    return self.msg()

  """
      Appends data to existing schema. If the schema is not compatible,
      it would throw error
  """
  def append(self):
    self._invoke('append')
    return self.msg()
  
  def attr(self):
    return self._get('attr').as_string_array()

  """
      !WARNING! Drops the existing schema associated with the data.
  """
  def drop(self):
    self._invoke('drop')
    return self.msg()
  
  """
     Provides Ticker by Ticker Summary of the Data
  """
  def summary(self):
    tvar = self.wq.env().get_temp_var()
    self._assign(tvar.name(), 'summary')
    summ = self.wq.env().get(tvar.name())
    return summ.__as_data_frame__()
  
  """
    Queries data for a Single Ticker
  """
  def query(self, iden):
    tvar = self.wq.env().get_temp_var()
    self._assign(tvar.name(), 'query', LQEnv._quote(iden))
    summ = self.wq.env().get(tvar.name())
    return summ.__as_data_frame__()
    
        
