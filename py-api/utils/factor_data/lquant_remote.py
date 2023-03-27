import numpy as np
import pandas as pd
import requests
import json

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
    
    def __init__(self):
        self.json = {}
    
    def runFor(self, universeId: str):
        self.json['universeId'] = universeId
        return self
    
    def start(self, startDate: str):
        self.json['startTime'] = startDate
        return self
    
    def to(self, endDate: str):
        self.json['endTime'] = endDate
        return self
    
    def at(self, frequency):
        self.json['rawFrequency'] = frequency
        return self
    
    def addForwardReturn(self):
        self.json['addForwardReturn'] = True
        return self
    
    def attr(self, attributes):
        self.json['attributes'] = attributes
        return self
    
    def outfile(self, outfile):
        self.json['outfile'] = outfile
        return self
    
    def weekdaysOnly(self):
        self.json['weekdaysOnly'] = True
        return self
    
def execute_remote(URL: str, Key: str, request: RemoteDataRequest):
    url = "{}/lquant/api/factor/data".format(URL)
    payload = json.dumps(request.json)
    headers = {
        'Auth-Key': '1234',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.ok:
        data = json.loads(response.content.decode('ascii'))
        data = data[list(data.keys())[0]]
        return RemoteFactorData(data)
    else:
        raise Exception("Error occurred == {}".format(response.content.decode('ascii')))
