import requests
from io import StringIO
import pandas as pd
class Connection:
    '''
    Connenection Class
    gets initialized using username and password
    simplify the process to call functional APIs
    '''
    #def __init__(self, username, password, URL = 'https://feed.luoquant.com'):
    def __init__(self, username = None, password = None, URL = 'http://tsdb1.qes.com:6481'):
        # assign the feature
        self.username = username
        self.password = password
        self.URL = URL
        self.session = self.authorize()
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} # headers for json HTTP access
        self.jobs = None

    def authorize(self):
        '''authorize the HTTP with username and password'''
        session = requests.Session()
        if self.username:
            session.auth = (self.username, self.password)
        return session

    def authorize(self):
        '''authorize the HTTP with username and password'''
        session = requests.Session()
        return session
    
    def post(self, svc, body):
        '''
        HTTP POST the request
        :param svc: service function {optimization|riskmodel}
        :param body: json format arguments
        :return: requests response text
        '''
        # convert body into valid json string if dictionary type
        if type(body) == dict:
            body = str(body).replace('\'', '"')
        response = self.session.post(self.URL + '/' + svc,
                                data = body, headers = self.headers)
        return response.text

    def get(self, svc):
        '''
        HTTP GET the request
        :param svc: service function {optimization|riskmodel}
        :return: requests API uid
        '''
        response = self.session.get(self.URL + '/' + svc)
        if response.ok:
            return response.text
        else:
            print("Error when querying ==> [{}]".format(response.text))
            return None

class DocsApi:
    def __init__(self, connection):
        self.connection = connection
        
    def _as_pandas_(self, path):
        print(path)
        data = self.connection.get(path)
        csvStringIO = StringIO(data)
        types_dict = {'QESID': str}
        return pd.read_csv(csvStringIO, sep = ",", dtype = types_dict)
        
    def search_docs(self, doctype, formtype, idtype, _id, startdate, enddate):
        path = "docs/search/" + "/".join([idtype,_id,doctype,formtype,startdate,enddate])
        return self._as_pandas_(path)
    
    def get_docs(self, doctype,formtype,date):
        path = "docs/list/" + "/".join([doctype,formtype,date])
        return self._as_pandas_(path)
    
    def get_keys(self, doctype,formtype,date,_id):
        path = "docs/keys/" + "/".join([doctype,formtype,date,str(_id)])
        return self.connection.get(path)

    def get_content(self,doctype,formtype,key: str):
        key = key.replace('/','::')
        path = "docs/data/" + "/".join([doctype,formtype,key])
        if key.endswith('csv'):
            return self._as_pandas_(path)
        else:
            return self.connection.get(path)
        
    def get_transcript_content(self, key: str):
        return self.get_content('transcripts','all',key)
        
    def get_transcript_keys(self, companyid, date):
        return self.get_keys('transcripts','all',key,date,companyid)
    
    def search_transcripts(self, idtype, _id, startdate, enddate):
        return self.search_docs('transcripts','all',idtype,_id,startdate,enddate)
    
    def get_edgar_content(self, formtype, key: str):
        return self.get_content('edgar-filing',formtype,key)
        
    def get_edgar_keys(self, formtype, cik, date):
        return self.get_keys('edgar-filing',formtype, date, str(cik))
    
    def get_transcripts(self, date):
        return self.get_docs('transcripts','all',date)
    
    def search_edgar(self, formtype, idtype, _id, startdate, enddate):
        return self.search_docs('edgar-filing',formtype,idtype,_id,startdate,enddate)
    
    def get_edgar_filings(self, formtype, date):
        return self.get_docs('edgar-filing',formtype,date)
