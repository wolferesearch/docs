import numpy as np
import pandas as pd
import requests
import json
import time

class RemoteMatrixData:
    def __init__(self, matrix_data):
        self.matrix_data = matrix_data
        self.matrix = None
    
    def _type_(self):
        return self.matrix_data['$type']
    
    def _values_(self):
        return self.matrix_data['$values']
    
    def cols(self):
        return self.matrix_data['$cols']
    
    def rows(self):
        return self.matrix_data['$rows']
    
    def dates(self):
        return self.matrix_data['$colnames']
    
    def ids(self):
        return self.matrix_data['$rownames']
    
    def version(self):
        return self.matrix_data['$version']
    
    def as_matrix(self):
        if self.matrix is not None:
            return self.matrix
        m1 = np.asmatrix(np.array(self._values_()).reshape((self.cols(),-1)).transpose())
        df = pd.DataFrame(m1, index = self.ids(), columns = self.dates())
        self.matrix = df
        return self.matrix
    
    def vals(self, dates: str):
        return self.as_matrix().loc[:,dates]
    
    def flat_vals(self,dates):
        return self.vals(dates).values.T.flatten()

    
class RemoteFactorData:
    def __init__(self, factor_data):
        names = factor_data['$names']
        values = factor_data['$values']
        self.names = names
        self.factor_data = { names[i] : RemoteMatrixData(values[i]) for i in range(len(names)) }
        
    def as_large_data_frame(self, dates = None, cols = None):
        first = self.factor_data[self.names[0]]
        if dates is None:
            dates = first.dates()
        if cols is None:
            cols = self.names
            
        ids =  first.ids()
        flat_dates = [c for c in dates for _ in range(len(ids))]
        df = pd.DataFrame({"DATE": flat_dates, "ID": list(ids)*len(dates)})
        for n1 in cols:
            df[n1] = self.factor_data[n1].flat_vals(dates)
        return df
    
    def __getitem__(self, key):
        return self.factor_data[key]

class RemoteDataRequest:
    """
    Data Request Object. A convenient class to build the request to send to LQuant remote server

    ...

    Attributes
    ----------
    json : dictionary
        Dictionary with all the parameters for request
    uuid : str
        UUID of the request. Only generated when an async request is sent
    executor : RemoteExecutor
        Handle to remote executor. Only set when an async request is sent

    Methods
    -------
    runFor(universeId)
        Sets the universe id for the request
    start(startDate)
        Sets the start date of data download. Should be YYYY-mm-dd
    to(endDate)
        Sets the end date of data download Should be YYYY-mm-dd
    at(frequency)
        Frequency of data pull
    addForwardReturn()
        Sets the request to add forward return to the data set
    attr(attributes:list)
        List of attributes to download
    """
    def __init__(self, _async = True):
        self.json = {"async": str(_async).lower()}
        self.uuid = None
        self.executor = None

    def runFor(self, universeId: str):
        self.json['universeId'] = universeId
        return self
    
    def start(self, startDate: str):
        self.json['startTime'] = startDate
        return self
    
    def to(self, endDate: str):
        self.json['endTime'] = endDate
        return self
    
    def at(self, frequency: str):
        self.json['rawFrequency'] = frequency
        return self
    
    def addForwardReturn(self):
        self.json['addForwardReturn'] = True
        return self
    
    def attr(self, attributes: list):
        self.json['attributes'] = attributes
        return self
    
    def outfile(self, outfile: str):
        self.json['outfile'] = outfile
        return self
    
    def weekdaysOnly(self):
        self.json['weekdaysOnly'] = True
        return self
    
    def sync(self):
        self.json['async'] = "false"
        return self
    
    def is_async(self):
        if "true" == self.json['async']:
            return True
        _format = self.json['format']
        if _format is None:
            return True
        return _format != 'json'
    
    def set_output_json(self):
        self.json['format'] = 'json'
        return self
    
    def _fn_(self,fn):
        return "{}/uuid/{}".format(fn, self.uuid)
    
    def status(self, check_error = False):
        status = self.executor._remote_("GET",self._fn_('status'))
        if check_error:
            if status['status'] == 'error':
                raise Exception("Service Returned an error ==> {}".format(status['error']))
        return status
    
    def is_ok(self):
        if self.uuid is  None:
            raise Exception("Request is not associated with a UUID. Please provide a valid request object")
        status = self.status()
        if status['status'] != 'completed':
            raise Exception("Cannot download and the job is not completed")
        if status['completed'] != 'true':
            raise Exception("Error occurred while running the job ==> {}".format(status['completed']))
        return True

    def get_data(self):
        self.is_ok()
        return self.executor._remote_("GET",self._fn_('get'))

    def cancel(self):
        return self.executor._remote_("DELETE",self._fn_('cancel'))

    def delete(self):
        return self.executor._remote_("DELETE",self._fn_('delete'))

    def is_completed(self):
        status = self.status(check_error = True)
        return status['status'] == 'completed'

    def is_cancelled(self):
        status = self.status(check_error = True)
        return status['status'] == 'cancelled'
    
    def is_error(self):
        status = self.status(check_error = True)
        return status['status'] == 'completed' and status['completed'] != 'true'

    def download(self, outfile):
        self.is_ok()
        return self.executor._download_("download/uuid/{}".format(self.uuid), outfile)

    def execute(self):
        if self.executor is None:
            raise Exception("Executor is not set, create a new object from executor")
        return self.executor.execute(self)
    
    def wait(self, max_time = 1200, sleep = 10):
        total_sleep = 0
        while not self.is_completed() and total_sleep < max_time:
            time.sleep(sleep)
            total_sleep = total_sleep + sleep
        return self.is_completed()
    
class RemoteExecutor:
    """
    Remote Executor class to interact with the Remote API

    ...

    Attributes
    ----------
    URL : str
        URL of the Remote Server
    Key : str
        API Key

    Methods
    -------
    execute(request: RemoteDataRequest)
        Executes a data download request on the server
    list_jobs()
        List down UUID for all remote jobs
    """


    def __init__(self, URL: str, Key: str):
        self.URL = URL
        self.Key = Key
        self.header = self._header_()

    def _header_(self):
        return {
            'Auth-Key': self.Key,
            'Content-Type': 'application/json'
        }
    
    def _url_(self,endpoint):
        return "{}/lquant/api/{}".format(self.URL,endpoint)
        
    def _download_(self,endpoint,outfile):
        response = requests.get(url = self._url_(endpoint), allow_redirects = True, headers = self.header)
        with open(outfile, 'wb') as f:
            f.write(response.content)
        return True
        
    def _remote_(self, method, endpoint, payload = None):
        response = requests.request(method, self._url_(endpoint), headers=self.header, data=payload)
        if response.ok:
            return json.loads(response.content.decode('ascii'))
        else:
            raise Exception("Error occurred == {}".format(response.content.decode('ascii')))
    
    def execute(self, request: RemoteDataRequest):
        """
            Executes a data request
            
            Params
            __________
            
        """
        if request.uuid is not None:
            raise Exception("Request is already associated with a UUID. Please create a new request")
        
        data = self._remote_(method = 'POST', endpoint = 'factor/data', payload = json.dumps(request.json))
        
        if request.is_async():
            request.uuid = data['uuid']
            request.executor = self
            return request
        else:
            data = data[list(data.keys())[0]]
            return RemoteFactorData(data)
    
    def build_sector_universe(self, id, starting_univ, starting_gics, start_date, end_date, freq, 
                exclude_gics = None, min_mktcap = None, max_mktcap = None, min_adv = None, exclude_ma=False, 
                marketcap_factor='MKTCAP*FXRATE_USD'):
        req = {}
        req['id'] = id
        req['starting_univ'] = starting_univ
        req['starting_gics'] = starting_gics
        req['start_date'] = start_date
        req['end_date'] = end_date
        req['freq'] = freq
        req['marketcap_factor'] = marketcap_factor

        if exclude_gics is not None:
            req['exclude_gics'] = exclude_gics

        if min_mktcap is not None:
            req['min_mktcap'] = min_mktcap

        if max_mktcap is not None:
            req['max_mktcap'] = max_mktcap

        if min_adv is not None:
            req['min_adv'] = min_adv
        
        if exclude_ma:
            req['exclude_ma'] = 'true'

        response = self._remote_(method = 'POST', endpoint = 'univ/build', payload = json.dumps(req))
        return id

    def list_jobs(self):
        return self._remote_(method = 'GET', endpoint = 'list/uuid')

    def new_request(self):
        request = RemoteDataRequest() 
        request.executor = self
        return request
