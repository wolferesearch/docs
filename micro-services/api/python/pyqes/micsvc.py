'''
tool functions to facilitate the Microservice API python functionality
- Connection Class
'''

import requests
import time
import os
import datetime
import pandas as pd
import json
import io

TYPE_RISKMODEL = 1
TYPE_OPTIMIZATION = 2

class Connection:
    '''
    Connenection Class
    gets initialized using username and password
    simplify the process to call functional APIs
    '''
    def __init__(self, username, password, URL = 'https://feed.luoquant.com'):
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
        session.auth = (self.username, self.password)
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
        return response.text

    # getter
    def get_jobs(self):
        if self.jobs is None:
            self.refresh_jobs()
        return self.jobs

    def refresh_jobs(self):
        job_response = self.session.get(self.URL +'/job')
        self.jobs = pd.read_json(job_response.text)
        self.jobs['STARTTIME'] = self.jobs['STARTTIME'].apply(lambda dt: datetime.datetime.fromtimestamp(dt / 1000))
        self.jobs['ENDTIME'] = self.jobs['ENDTIME'].apply(lambda dt: datetime.datetime.fromtimestamp(dt / 1000) if not dt else dt)
        return True

    def failed_jobs(self, type_id):
        '''return list of failed jobs'''
        self.refresh_jobs()
        return self.jobs[(self.jobs.STATUS == 'FAILED') & (self.jobs.TYPEID == type_id)]

    def success_jobs(self, type_id):
        '''return list of successful jobs'''
        # filter func. to select out successful jobs
        self.refresh_jobs()
        return self.jobs[(self.jobs.STATUS == 'SUCCESS') & (self.jobs.TYPEID == type_id)]
    
    def get_template(self, name):
        templates = self.templates()
        templates = templates[templates.NAME == name]
        if templates.size == 0:
            raise Exception('Template ' + name + 'not found')
        
        t1 = templates.TYPE.iloc[0]
        if t1 == 'Risk-Model':
            return RiskModelTemplate(self,templates.iloc[0])
        elif t1 == 'Optimization':
            return OptimizerTemplate(self,templates.iloc[0])
        
    def templates(self):
        # access the list of templates
        return pd.read_json(self.get('template'))

    def risk_templates(self):
        templates = self.templates()
        return templates[templates.TYPE == 'Risk-Model']

    def optimization_templates(self):
        templates = self.templates()
        return templates[templates.TYPE == 'Optimization']

    def upload_portfolio(self, id, filename):
        # portfolio argument body
        body = {'portfolioName':id, 'file': open(filename,'rb')}
        # post the upload request
        self.session.post(self.URL + '/portfolio',headers = self.headers,
                          data = body)

    # Functional Method to interact with the inner class
    def get_risk_model_builder(self):
        return RiskModel(self)

    def get_optimizer(self):
        return Optimizer(self)

    def get_catalog(self):
        return Catalog(self)


class Catalog:
    '''
    Catalog Class to browse universes, factors and templates
    '''
    def __init__(self, conn):
        self.conn = conn
        
    def __as_df__(self,nm):
        return pd.read_json(self.conn.get(nm))

    def get_universe(self):
        '''return the list of available universe'''
        return self.__as_df__('universe')
    
    def get_factors(self):
        '''return the list of available factor'''
        return self.__as_df__('factor')
        
    def get_meta_factors(self):
        '''return the list of available meta factor'''
        return self.__as_df__('meta')
    
    def get_portfolios(self):
        '''return the list of available '''
        return self.__as_df__('portfolio')
    
    def get_templates(self):
        '''return the list of API function templates'''
        return self.__as_df__('template')

    
class EdgarFiling:
    
    def __init__(self, conn, year, month, day):
        self.conn = conn
        self.year = '{:04d}'.format(int(year))
        self.month = '{:02d}'.format(int(month))
        self.day = '{:02d}'.format(int(day))
        self.meta = json.loads(self.conn.get('/'.join(['edgar-filing',self.year,self.month,self.day])))
        self.info = pd.DataFrame(json.loads(self.conn.get('edgar-filing/sections/')))[['FILING','ID','NAME']]
        
    def get_filings(self):
        return self.meta
    
    def get_file(self,cik,fiscaldate,filing,file):
        key = '/'.join(['edgar-filing',self.year,self.month,self.day,cik,fiscaldate,filing,file])
        return self.conn.session.get(self.conn.URL + '/' + key).content.decode('utf-8')
    
    def download_files_by_tickers(self, tickers):
        for com in self.meta:
            if not com['TICKER'] in tickers:
                continue   
            for f in com['FILE']:
                txt = self.get_file(cik=com['CIK'], fiscaldate=com['FISCALDATE'], filing=com['FILING'], file=f)
                with open('_'.join([com['TICKER'],com['FISCALDATE'],com['FILING'],f]),"w") as f1:
                    f1.write(txt)
                    
    
class EntityService:
    '''
    Entity class to manage for the service
    conn: connection object to interact with the server
    svc: service option
    uuid: generated unique id
    '''
    def __init__(self, conn, svc, uuid):
        self.conn = conn
        self.svc = svc
        self.uuid = uuid

    def info(self):
        return json.loads(self.conn.get(self.svc+'/'+self.uuid))

    @property
    def get_id(self):
        return self.uuid

    def get(self, path):
        return self.conn.get(self.svc+'/'+self.uuid+'/'+path)

    def getdf(self, path):
        content = self.get(path)
        return pd.read_csv(io.StringIO(content), index_col = 0)

    def wait(self, max_wait_secs = 300, verbose = False):
        ws = 0  # keep track of the waiting time
        info = self.info()
        while (info.get('status')=='STARTED' and ws<max_wait_secs):
            time.sleep(ws)
            # update information
            info = self.info()
            if verbose and verbose % 15 == 0 and verbose > 0:
                print('function of {} is running for {} seconds'.format(self.svc, ws))
            ws += 5
        return info

class Template:
    '''
    Base Template Class
    set up the argument for API function
    '''
    def __init__(self, conn, val):
        '''
        :param conn: Connection object to call the APIs
        :param val:
        '''
        self.conn = conn
        # assign the content into json
        self.json = val.pop('CONTENT')
        self.val = val
    # Getter Functions
    def name(self):
        return self.val['NAME']

    def type(self):
        return self.val['TYPE']

    def description(self):
        return self.val['DESCRIPTION']

    def content(self):
        return self.json

    def save(self, name):
        self.json['name'] = name
        self.json['__name__'] = name
        typeMap = {
            "Risk-Model": "risk-model",
            "Optimization" : "optimization"
        }
        self.conn.post('template/' + typeMap.get(self.type()), self.json)


class OptimizerTemplate(Template):
    ''' Optimization Template inherited from the pyqes Template class'''
    def __init__(self,conn,raw):
        Template.__init__(self,conn,raw)
        #super(conn,raw)   # parent class

    # Setter Functions
    def set_target_risk(self, target_risk):
        self.json['target_risk'] = target_risk
    def set_bounds(self, bounds):
        self.json['bound'] = bounds
    def set_max_ADV_participation(self, maxADVPart):
        self.json['max_ADV_participation'] = maxADVPart
    def set_max_turnover(self, turnover):
        self.json['turnover'] = turnover
    def set_gross_weight(self, gross_weight):
        self.json['gross_weight'] = gross_weight
    def set_net_weight(self, net_weight):
        self.json['net_weight'] = net_weight
    def set_benchmark(self, benchmark):
        self.json['benchmark'] = benchmark
    # Getter Functions
    def get_objective(self):
        return self.json['objective']
    def get_traget_risk(self):
        return self.json['target_risk']
    def get_bounds(self):
        return self.json['bound']
    def get_max_ADV_participation(self):
        return self.json['max_ADV_participation']
    def get_max_turnover(self):
        return self.json['max_turnover']
    def get_gross_weight(self):
        return self.json['gross_weight']
    def get_net_weight(self):
        return self.json['net_weight']
    def get_benchmark(self):
        return self.json['benchmark']

class RiskModelTemplate(Template):
    '''Risk Model Template inherited from the pyqes Template class'''
    def __init__(self,conn,raw):
        Template.__init__(self,conn,raw)
    def factors(self):
        return self.json['factors']
    def meta(self):
        return self.json['meta']
    def cov_matrix_ags(self):
        return self.json['covArgs']
    def options(self):
        return self.json['options']

    def add_factor(self, mnemonic, name):
        factor_ls = self.factors()
        factor_ls.append({'mnemonic':mnemonic, 'name':name})
        self.json['factors'] = factor_ls

    def add_meta(self, mnemonic, name):
        meta_ls = self.meta()
        meta_ls.append({'mnemonic': mnemonic, 'name': name})
        self.json['meta'] = meta_ls

    def set_cov_matrix_interval(self, interval):
        self.json['covArgs']['interval'] = interval

    def set_cov_matrix_var_half_life(self, var_half_life):
        self.json['covArgs']['var.period'] = var_half_life

    def set_cov_matrix_covar_half_life(self, covar_half_life):
        self.json['covArgs']['cov.period'] = covar_half_life

    def set_specific_risk_shrinkage(self, shrinkage):
        if shrinkage > 1:
            raise ValueError('Shrinkage cannot be greater than one')
        elif shrinkage < 0:
            raise ValueError('Shrinkage cannot be less than 0')
        self.json['options']['spRisk']['shrinkage'] = shrinkage


class Base:
    '''
    Base class for Optimizer and Risk Model
    '''
    def __init__(self):
        self.conn = None
        self.esvc = None

    # Getter
    def completed(self):
        self.check_conn() # Check for connection first
        return self.conn.success_jobs(self.typeid)
    def failed(self):
        self.check_conn()
        return self.conn.failed_jobs(self.typeid)
    def info(self):
        '''return the API specific service information'''
        if self.esvc is None:
            raise ValueError('Please create a new {} or attach it to existing by doing set_id'.format(self.endPoint))
        return json.loads(json.dumps(self.esvc.info()))
    def status(self):
        return self.info()['status']

    # Setter
    def set_conn(self, conn):
        self.conn = conn
    def set_id(self, uuid):
        self.data = None
        self.esvc = EntityService(self.conn, self.endPoint, uuid)
    def set_latest(self, k = 0):
        self.jobs = self.completed()
        if self.jobs is None:
            return(False)
        if len(self.jobs) > k:
            self.set_id(self.jobs.iloc[0]['UUID'])
        return(True)

    # Functional Methods
    def check_conn(self):
        if self.conn is None:
            raise ValueError('Please create a connection first using set_conn method.')
            
    def wait(self, max_wait_secs):
        if self.esvc is None:
            raise ValueError('No Optimization Associated with the class, either set id or create new optimization request')
        return self.esvc.wait(max_wait_secs)
    
    def submit_new_request(self, req):
        self.esvc = None
        self.data = None
        endPoint = self.endPoint   # service argument
        if type(req) == dict:
            req = str(req).replace('\'', '"')
        # call the API and get the respective uuid
        response = self.conn.post(endPoint, req)
        self.req = req
        self.esvc = EntityService(self.conn, endPoint, response)


'''
Optimizer class

Class allows to do the following:
    1.Run new optimization
    2.Pull data for previously run optimizations
    3.List all optimization (failed/successful)
    4.Download Weights and Summary file
'''

class Optimizer(Base):
    def __init__(self, conn):
        self.set_conn(conn)
        self.req = None
        self.endPoint = 'optimization'
        self.typeid = TYPE_OPTIMIZATION
        self.no_request_error_msg = 'No Optimization Associated with the class, either set id or create new optimization request'

    def get_data(self):
        '''return a dictionary of function data (Summary, Weight) in pandas DataFrame format'''
        if self.data is not None:
            return self.data
        if self.esvc is None:
            raise ValueError(self.no_request_error_msg)
        information = self.info()
        status = information['status']
        if status == 'STARTED':
            raise TimeoutError('Optimization has not completed yet')
        elif status == 'ERROR':
            raise ConnectionError('{} failed with message ==> [{}]'.format(self.esvc.get_id, information['message']))
        # access the data with respective file name
        data_dic = {}
        file_ls = information['files']
        for file in file_ls:
            # argument name
            file_name = file_ls.replace('.csv', '')
            data_dic[file_name] = self.esvc.getdf(file)
        return data_dic


    def new_request(self, portfolioId, alpha, notional, template,
                    startDate, endDate, freq, baseCurrency = "USD"):
        '''call the optimization function with specifying arguments
        Input arguments
        :param portfolioId: corresponding id of the portfolio
        :param alpha:
        :param notional: notional strategy value
        :param template:
        :param startDate:
        :param endDate:
        :param freq: trading frequency
        :param baseCurrency: currency of value
        '''
        riskModel = {'universe': portfolioId, 'template': "default"}
        request = {'portfolioId':portfolioId,
                   'alpha':alpha,
                   'template':template,
                   'startDate':startDate,
                   'endData':endDate,
                   'notionalValue':notional,
                   'baseCurrency':baseCurrency,
                   'freq':freq,
                   'riskModel':riskModel
        }
        self.submit_new_request(request)


class RiskModel(Base):
    '''Risk Model Class'''
    def __init__(self, conn):
        self.set_conn(conn)
        self.typeid = TYPE_RISKMODEL
        self.endPoint = 'risk-model'
        self.no_request_error_msg = 'Please create a new risk model or attach it to existing by doing set_id'
        self.jobs = None
        self.set_latest()

    def dates(self):
        if self.esvc is None:
            raise ValueError(self.no_request_error_msg)
        info = json.loads(self.esvc.get(""))
        return info['dates']

    def get_data(self, dated):
        info = json.loads(self.esvc.get(dated))
        data_dic = {}
        file_ls = info['files']
        for file in file_ls:
            # argument name
            if 'csv' in file:
                file_name = file.replace('.csv', '')
            else:
                file_name = file
            data_dic[dated + '/'+file_name] = self.esvc.getdf(dated + '/' +file)
        return data_dic

    def download_all(self, out_dir):
        date_ls = self.dates()
        # save the data along time into csv files
        for dt in date_ls:
            # iterate along time
            data_dic_dt = self.get_data(dt)
            for key, df in data_dic_dt.items():
                # save directory
                out_dir = os.path.join(os.path.curdir, out_dir)
                save_dir = os.path.join(out_dir, key.split('/')[0])
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)

                df.to_csv(os.path.join(out_dir, '{}'.format(key)))
        return True

    def new_request(self, universe, template, startDate, endDate, freq):
        request = {'universe':universe,
                   'template':template,
                   'startDate':startDate,
                   'endDate':endDate,
                   'freq':freq

        }
        self.submit_new_request(request)




