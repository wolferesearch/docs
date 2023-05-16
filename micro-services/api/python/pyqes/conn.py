from io import StringIO
import pandas as pd
import requests
class Connection:
    '''
    Connenection Class
    gets initialized using username and password
    simplify the process to call functional APIs
    '''
    def __init__(self, username = None, password = None, URL = 'http://feed.luoquant.com'):
        # assign the feature
        self.username = username
        self.password = password
        self.URL = URL
        session = requests.Session()
        session.auth = (username, password)
        self.session = session 
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'} # headers for json HTTP access
        self.jobs = None

    def authorize(self):
        '''authorize the HTTP with username and password'''
        return self.session

    def authorize(self):
        '''authorize the HTTP with username and password'''
        session = requests.Session()
        return session

    def _post_(self,svc,body):
        # convert body into valid json string if dictionary type
        # if type(body) == dict:
        #     body = str(body).replace('\'', '"')
        response = self.session.post(self.URL + '/' + svc,
                                json = body, headers = self.headers)
        return response
    
    def post(self, svc, body):
        '''
        HTTP POST the request
        :param svc: service function {optimization|riskmodel}
        :param body: json format arguments
        :return: requests response text
        '''
        return self._post_(svc,body).text

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