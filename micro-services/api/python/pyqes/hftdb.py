from datetime import datetime
import pytz
import json
import pandas as pd

class HFTDB:
    def __init__(self, conn):
        """ QES API to access High Frequency Data

        Args:
            conn (pyqes.conn.Connection): Connection Object 
        """
        self.conn = conn
        self.TZ = pytz.timezone('America/New_York')
        self.FMT = "%Y-%m-%dT%H:%M:%S.000Z"
        self.SFMT = "%Y-%m-%dT%H:%M:%S.000"
        
    def _localtime_(self, tz, hour, minute):
        return datetime.now(tz) \
            .replace(hour=hour, minute=minute, second=0, microsecond=0) \
            .astimezone(pytz.utc)
    
    def _nvld_(self, x, default_val):
        x = self._nvl_(x,default_val)
        return x.strftime(self.SFMT)
    
    def _nvl_(self, x, default_val):
        if x is None:
            return default_val
        return x
  
    def _localize_(self, v, tz = None):
        return pytz.utc.localize(datetime.strptime(v,self.FMT),pytz.utc).astimezone(self._nvl_(tz,self.TZ))
  

    def _parse_(self, text):
        data = json.loads(text)
        dates = [self._localize_(x) for x in data['$rows']]
        series = pd.Series(data['$vals'], dates)
        return series
        
    
    def _marketopen_(self):
        return self._localtime_(tz = self.TZ, hour = 9, minute = 30)
    
    def _marketclose_(self):
        return self._localtime_(tz = self.TZ, hour = 16, minute = 0)
        
    def __get__(self, id2: str, starttime: datetime = None, endtime: datetime = None, region: str = 'US'):
        svc = "intraday/db/ts/{}/{}/{}/{}".format(region,id2,
                                                  self._nvld_(starttime,self._marketopen_()), 
                                                  self._nvld_(endtime,self._marketclose_()),
                                                 )
        response = self.conn.session.get(self.conn.URL + '/' + svc)
        if not response.status_code == 200:
            raise Exception("Unexpected Status Code {}. Error ==> {}".format(response.status_code,response.text))
        
        return self._parse_(response.text)
    
    def get_factor_returns(self, factor: str, sector: str = 'ALL', starttime: datetime = None, 
                          endtime: datetime = None, region: str = 'US'):
        """ Pulls Returns from QES High Frequency Returns data for factors

        Args:
            factor (str): Mnemonic of the factor to be queries
            sector (str, optional): Sector Name. Defaults to 'ALL'.
            starttime (datetime, optional): Start time of the data. Defaults to None.
            endtime (datetime, optional): End time of the data. Defaults to None.
            region (str, optional): Region. Only US is supported. Defaults to 'US'.

        Returns:
            pandas.Series: Time series of wealth for the 
        """
        id2 = "SWPORTVAL.{}.{}".format(factor,sector)
        return self.__get__(id2 = id2, starttime = starttime, endtime = endtime, region = region)
    
    def get_risk_factor_returns(self, factor: str, model: str = 'AC', starttime: datetime = None, 
                          endtime: datetime = None,  region = 'US', version = 'V2'):
        """ Pulls returns from QES High Frequency for risk model factors. Only US is supported currently

        Args:
            factor (str): Mnemonic of the risk model factor
            model (str, optional): _description_. Defaults to 'AC'.
            starttime (datetime, optional): _description_. Defaults to None.
            endtime (datetime, optional): _description_. Defaults to None.
            region (str, optional): _description_. Defaults to 'US'.
            version (str, optional): _description_. Defaults to 'V2'.

        Returns:
            _type_: _description_
        """
        id2 = "FMPLEV{}.{}.{}".format(version,factor,model)
        #print(id2)
        return self.__get__(id2 = id2, starttime = starttime, endtime = endtime, region = region)