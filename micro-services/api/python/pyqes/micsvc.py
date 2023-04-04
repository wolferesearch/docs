'''
tool functions to facilitate the Microservice API python functionality
- Connection Class
'''

import requests
import time
import os
import tempfile
from datetime import datetime
import pandas as pd
import json
import io
import urllib.parse

TYPE_RISKMODEL = 1
TYPE_OPTIMIZATION = 2
TYPE_BLACKLITTERMAN = 7
TYPE_ATTRIBUTION = 3
TYPE_SIMULATOR = 8

class Connection:
    '''
    Connenection Class
    gets initialized using username and password
    simplify the process to call functional APIs
    '''
    def __init__(self, username = os.environ.get('LQUANT_MICSVC_USER'), password = os.environ.get('LQUANT_MICSVC_PWD'), URL = 'https://feed.luoquant.com'):
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

    def delete(self, endpoint):
        print(endpoint)
        response = self.session.delete(self.URL + '/' + endpoint, headers = self.headers)
        return response.text

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

    # getter
    def get_jobs(self):
        if self.jobs is None:
            self.refresh_jobs()
        return self.jobs

    def refresh_jobs(self):
        job_response = self.session.get(self.URL +'/job')
        self.jobs = pd.read_json(job_response.text)
        if self.jobs.empty:
            self.jobs = None
        else:
            self.jobs['STARTTIME'] = self.jobs['STARTTIME'].apply(lambda dt: datetime.fromtimestamp(dt / 1000))
            #self.jobs['ENDTIME'] = self.jobs['ENDTIME'].apply(lambda dt: datetime.fromtimestamp(dt / 1000) if dt is not None else None)
            #self.jobs = self.jobs.sort_values(by=['STARTTIME'], ascending = False)
            self.jobs = self.jobs.sort_values(by='STARTTIME', ascending = False)
        return True

    def has_jobs(self):
        if self.jobs is None:
            return False
        if self.jobs.empty:
            return False
        return True

    def failed_jobs(self, type_id):
        '''return list of failed jobs'''
        self.refresh_jobs()
        if self.has_jobs():
            return self.jobs[(self.jobs.STATUS == 'FAILED') & (self.jobs.TYPEID == type_id)]
        else:
            return None

    def success_jobs(self, type_id):
        '''return list of successful jobs'''
        # filter func. to select out successful jobs
        self.refresh_jobs()
        if self.has_jobs():
            return self.jobs[(self.jobs.STATUS == 'SUCCESS') & (self.jobs.TYPEID == type_id)]
        else:
            return None

    def delete_job_data(self, uuids):
        for uid in uuids:
            print(self.delete(endpoint = 'job/data/' + uid))
        return self
    
    def get_template(self, name, type_ = 'Risk-Model'):
        templates = self.templates()
        templates = templates[(templates.NAME == name) & (templates.TYPE == type_) ]
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
        files={'file': open(filename,'rb')}
        data={'portfolioName': id}
        return self.session.post(self.URL + '/portfolio', files = files, data = data)

    def user_data(self):
        return UserData(self)
        

    # Functional Method to interact with the inner class
    def get_risk_model_builder(self):
        return RiskModel(self)

    def get_optimizer(self):
        return Optimizer(self)
    
    def get_black_litterman(self):
        return BlackLitterman(self)

    def get_portsimulator(self):
        return PortfolioSimulator(self)

    def get_attribution(self):
        return Attribution(self)

    def get_catalog(self):
        return Catalog(self)

    def upload_file(self,file_loc, name, end_point = 'port'):
        print('Calling Uploading {} to {} ...'.format(file_loc, name))
        response = self.session.post(self.URL + '/' + end_point, files = {'file': open(file_loc,'rb')}, data = {'name': name})
        print(response.text)
        return response

class Catalog:
    '''
    Catalog Class to browse universes, factors and templates
    '''
    def __init__(self, conn):
        self.conn = conn
        
    def __as_df__(self,nm):
        v = self.conn.get(nm)
        if v:
            return pd.read_json(v)
        else:
            return None

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

class MappedUserData:
    def __init__(self, user_data):
        self.user_data = user_data

    def get_data(self, dated):
        v = pd.DataFrame([self.user_data[x][dated] for x in self.user_data.keys()]).T
        v.columns = list(self.user_data.keys())
        return v
    
class JobOutput:
    
    def __init__(self, conn, uuid, files):
        self.conn = conn
        self.uuid = uuid
        self.files = files
        self.udata = None
        self.data = {}

    def __file__(self, key):
        return key[(key.find('_')+1):len(key)]
        
    def _append(self,keys,v,data):
        key = keys[0]
        if len(keys) == 1:
            key = key.split('.')[0]
            k = key[(key.find('_')+1):len(key)]
            data[k] = v
            return data
            
        keys.pop(0)
        child_data = data.get(key)

        if child_data is None:
            child_data = {}

        data[key] = self._append(keys,v,child_data)
        
        return data

    def _get_raw_(self, key):
        return self.conn.get('job/data/' + self.uuid + '/' + key.replace('/','::'))

    def _fetch(self,key):
        file = os.path.basename(key) 

        structure = file[:1]
        data_type = file[1:2]

        content = self._get_raw_(key)
        data = io.StringIO(content)
        if structure == 'M': # Matrix
            return pd.read_csv(data, index_col=0)
        elif structure == 'V':
            return pd.read_csv(data, index_col=0)
        elif structure == 'D':
            return pd.read_csv(data, index_col=0)
        elif structure == 'S':
            val = pd.read_csv(data, index_col=0)
            val.x.iloc[0]
            return val
        else:
            raise Exception("Unexpected Data Structure Found {}".format(structure))
    
    def get_keys(self):
        return [ self.__file__(x) for x in self.files.Key]

    def get_single_data(self, key):
        keys = self.get_keys()
        v = self.files.iloc[[k == key for k in keys]]
        fullkey = v['Key'].iloc[0]
        return self._fetch(fullkey)

    def get_data(self, prefix = None):
        keys = self.files.Key
        if prefix is not None:
            b = [s.startswith(prefix) for s in self.files.Key]
            keys = keys[b]
        
        data = {}
        for key in keys:
            v = self._fetch(key)
            data = self._append(keys = key.split('/'), v= v, data = data)
        return data
    
    def get_user_data(self):
        if self.udata is not None:
            return self.udata
        
        user_data = self.get_data(prefix = 'user_data')
        if user_data:
            self.udata = MappedUserData(user_data['user_data'])
            return self.udata
        else:
            return None
  
class EntityService:
    '''
    Entity class to manage for the service
    conn: connection object to interact with the server
    svc: service option
    uuid: generated unique id
    '''
    def __init__(self, conn, svc, uuid, version = 1):
        self.conn = conn
        self.svc = svc
        self.uuid = uuid
        self.version = version

    def info(self):
        if self.version == 1:
            return json.loads(self.conn.get(self.svc+'/'+self.uuid))
        elif self.version == 2:
            return json.loads(self.conn.get('job/info' + '/'+self.uuid))
        else:
            raise Exception("Unsupported version for info")

    @property
    def get_id(self):
        return self.uuid

    def get_logs(self):
        return self.conn.get('logs/' + self.uuid)

    def get(self, path):
        if self.version == 1:
            return self.conn.get(self.svc+'/'+self.uuid+'/'+path)
        elif self.version == 2:
            if len(path) > 0:
                return self.conn.get('job/data/' + self.uuid + '/' + urllib.parse.quote(path))
            else:
                return self.conn.get('job/data/' + self.uuid)
            
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
    
    def get_job_output(self):
        if self.uuid is None:
            raise Exception("No UUID attached to the service. Please run a new request or attach an existing UUID")
        
        info = self.info()
        status = info.get('status')
        if status != 'SUCCESS':
            raise Exception("The job is not completed, current status ==> [{}]".format(status))
        
        content = self.conn.get('job/content/' + self.uuid)
        content = pd.read_csv(io.StringIO(content))
        return JobOutput(conn = self.conn, uuid = self.uuid, files = content)

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
    def __init__(self, version = 1):
        self.conn = None
        self.esvc = None
        self.version = version

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
        self.esvc = EntityService(self.conn, self.endPoint, uuid, self.version)

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
        if self.version == 1:
            response = self.conn.post(endPoint, req)
        elif self.version == 2:
            response = self.conn.post('job/submit/' + endPoint, req)
        else:
            raise Exception("Unexpected Version {}. Only Version=1/2 are supported.".format(self.version))

        self.req = req
        self.esvc = EntityService(self.conn, endPoint, response, self.version)
        return self
    
    def get_logs(self):
        if self.esvc is None:
            raise Exception("Either attach an existing UUID or run a new one")
        
        return self.esvc.get_logs()
    
    def get_output(self):
        if self.esvc is None:
            raise Exception("Either attach an existing UUID or run a new one")
        return self.esvc.get_job_output()

    def set_user_data(self, name, data, overwrite = True):
        user_data = UserData(self.conn)

        if not overwrite and user_data.exists(name):
            raise Exception("Data {} and overwrite is not set. Will not overwrite.".format(name))

        user_data.upload_data(data,name)
        self.req['user_data'] = {
            'format' : 'csv',
            'name': name
        }
        return self

    def submit(self):
        self.submit_new_request(self.req)
        return self
    

class OptimizerResult:

    def __init__(self, output):
        self.output = output

    def __get__(self, name):
        return self.output.get_single_data(name)

    def get_old_weights(self):
        return self.__get__('old_weights.csv')

    def get_old_weights_2(self):
        return self.__get__('old_weights_2.csv')

    def get_weights(self):
        return self.__get__('weights.csv')
        
    def get_notional_value(self):
        return self.__get__('notional_value.csv')

    def get_tracking_error(self):
        return self.__get__('tracking_error.csv')

    def get_alpha(self):
        return self.__get__('alpha.csv')

    def get_old_notional_value(self):
        return self.__get__('old_notional_value.csv')

    def get_required_turnover(self):
        return self.__get__('required_turnover.csv')
    
    def get_risk(self):
        return self.__get__('risk.csv')

    def get_turnover(self):
        return self.__get__('turnover.csv')
    
    def get_portfolio(self, dated):
        user_data = self.output.get_user_data()
        df = user_data.get_data(dated)
        weights = self.get_weights()[[dated]]
        weights.columns = ['WEIGHT']
        return pd.merge(df, weights, left_index=True, right_index=True)
        
        



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
        super().__init__(version = 2)
        self.set_conn(conn)
        self.req = {}
        self.endPoint = 'optimization'
        self.typeid = TYPE_OPTIMIZATION
        self.no_request_error_msg = 'No Optimization Associated with the class, either set id or create new optimization request'

    def set_template(self, template: str):
        self.req['template'] = template
        return self

    def set_objective(self, objective: str):
        self.req['objective'] = objective
        return self
    
    def set_alpha(self, alpha: str):
        self.req['alpha'] = alpha
        return self

    def set_adv_factor(self, adv_factor: str):
        self.req['adv_factor'] = adv_factor
        return self
    
    def set_htb_threshold(self, threshold: float):
        self.req['threshold'] = threshold
        return self

    def set_benchmark(self, benchmark: str):
        self.req['benchmark'] = benchmark
        return self
    
    def set_init_portfolio(self, init_portfolio: str):
        self.req['init_portfolio'] = init_portfolio
        return self
    
    def add_group_constraint(self, grouping_factor: str, min_exposure: float, max_exposure: float, benchmark: bool):
        """Add Group Constraints to the optimization. 
        
        This ensures that within the Group the aggregate exposure is within the bounds. For when the benchmark is selected

        Parameters
        ----------
        grouping_factor: str
            Name of the factor to put constraint on. For GICS factors, please use GICS1, GICS2, GICS3, GICS4
        min_exposure: float
            Minimum Exposure for each of the group
        max_exposure: float
            Maximum Exposure for each of the group
        benchmark: bool
            Boolean indicator if the exposure should be relative to the benchmark

        Returns
        -------
        Optimizer Class Instances

        """
        group_constraints = self.req.get('group_constraints')
        if group_constraints is None:
            group_constraints = []
            self.req['group_constraints'] = group_constraints
        group_constraints.append({'factor': grouping_factor, 'min' : min_exposure, 'max': max_exposure, 'benchmark' :str(benchmark)})
        return self

    def add_stock_bounds(self, lb: str, ub: str, benchmark: bool):
        """Add Stock by Stock bounds

        Sets the lower bound and upper bound for the portfolio holdings

        Parameters
        ----------
        lb: str
            Column corresponding to the lower bound
        ub: str
            Column corresponding to the upper bound
        benchmark: bool
            Boolean indicator if the bound should be relative to the benchmark weight
        """
        bounds = self.req.get('bounds')
        if bounds is None:
            bounds = {}
            self.req['bounds'] = bounds
        
        if benchmark:
            bounds['relative'] = {'lb': lb, 'ub': ub}
        else:
            bounds['absolute'] = {'lb': lb, 'ub': ub}
        return self
    
    def set_abs_risk(self):
        """Sets risk to absolute risk instead of trcking error
        """
        self.req['abs_risk'] = 'true'
        return self
    
    def set_risk_neutralization_factors(self, neutralization_factors, factor_min_exposure, factor_max_exposure):
        """Controls exposure corresponding to risk factors
        
        Parameters
        ----------
        neutralization_factors: list [str]
            List of neutralization factors. This should be referenced in the risk model. 
        factor_min_exposure: float
            Minimum exposure for the risk factor
        factor_max_exposure: float
            Maximum exposure for the risk factor
        
        """
        self.req['neutralization_factors'] = {
            'Factor': neutralization_factors,
            'Min' : factor_min_exposure,
            'Max' : factor_max_exposure
        }
        return self
    
    def set_risk_neutralization_factors_abs(self, neutralization_factors, factor_max_exposure):
        """Controls absolute exposure corresponding to risk factors
        
        Parameters
        ----------
        neutralization_factors: list [str]
            List of neutralization factors. This should be referenced in the risk model. 
        factor_min_exposure: float
            Minimum exposure for the risk factor
        
        """
        self.req['neutralization_factors_abs'] = {
            'Factor': neutralization_factors,
            'Max' : factor_max_exposure
        }
        return self

    def add_neutralization_matrix(self, neutralization_factors, factor_min_exposure, factor_max_exposure,
                                         grouping_matrix = None, benchmark= False):
        """Controls  exposure corresponding to custom factors 
        
        Parameters
        ----------
        neutralization_factors: list [str]
            List of neutralization factors. This should be referenced in the risk model. 
        factor_min_exposure: float
            Minimum exposure for the custom factor
        factor_max_exposure: float
            Maximum exposure for the custom factor
        grouping_matrix: str
            Control exposure at each group level. Default can be none so entire universe is kept in one group
        benchmark: bool
            Boolean indicator when set the exposure are computed relative to the benchmark
        
        """
        self.req['neutralization_matrix'] = {
            'bounds': {
                 'Factor': neutralization_factors,
                 'Min' : factor_min_exposure,
                 'Max' : factor_max_exposure
            },
            'benchmark': benchmark,
            'grouping_matrix': grouping_matrix 
        }
        return self

    def set_benchmark(self, benchmark:str):
        self.req['use_benchmark'] = 'TRUE'
        self.req['benchmark'] = benchmark
        return self

    def set_bounds(self,lb:float, ub: float):
        self.req['lb'] = lb
        self.req['ub'] = ub
        return self

    def set_target_risk(self, target_risk: float):
        self.req['target_risk'] = target_risk
        return self

    def set_max_turnover(self, turnover: float):
        self.req['max_turnover'] = turnover
        return self

    def set_max_number_securities(self, max_securities: int):
        self.req['limit_number'] = max_securities
        return self
    
    def set_risk_model(self, risk_model: str):
        self.req['risk_model'] = {'risk_model_id' : risk_model}
        return self
    
    def set_lambda(self, _lambda: float):
        self.req['lambda'] = _lambda
        return self
    
    def set_implied_alpha(self, implied_alpha: bool):
        self.req['implied_alpha'] = str(implied_alpha)
        return self

    def set_min_holding(self, min_holding: float):
        self.req['min_holding'] = min_holding
        return self

    def set_min_long_weight(self, min_long_weight: float):
        self.req['min_long_weight'] = min_long_weight
        return self

    def set_max_long_weight(self, max_long_weight: float):
        self.req['max_long_weight'] = max_long_weight
        return self

    def set_min_short_weight(self, min_short_weight: float):
        self.req['min_short_weight'] = min_short_weight
        return self
    
    def set_max_short_weight(self, max_short_weight: float):
        self.req['max_short_weight'] = max_short_weight
        return self

    def set_use_adv(self, use_adv: bool):
        self.req['use_adv'] = str(use_adv)
        return self

    def set_use_tcm(self, use_tcm: bool):
        self.req['use_tcm'] = str(use_tcm)
        return self
    
    def set_transaction_cost_model(self, transaction_cost_model: str):
        self.req['transaction_model'] = transaction_cost_model
        return self

    def set_transaction_cost(self, transaction_cost: float):
        self.req['trans_cost'] = transaction_cost
        return self

    def set_soft_turnover_penalty(self, soft_turnover_penalty: float):
        self.req['soft_turnover_penalty'] = soft_turnover_penalty
        return self

    def set_soft_relative_weight_penalty(self, soft_relative_weight_penalty: float):
        self.req['soft_relative_weight_penalty'] = soft_relative_weight_penalty
        return self

    def set_relative_weight_min(self, relative_weight_min: float):
        self.req['relative_weight_min'] = relative_weight_min
        return self

    def set_relative_weight_max(self, relative_weight_max: float):
        self.req['relative_weight_max'] = relative_weight_max
        return self

    def get_results(self):
        return OptimizerResult(self.get_output())

class RiskModel(Base):
    '''Risk Model Class'''
    def __init__(self, conn):
        super().__init__(version = 1)
        self.set_conn(conn)
        self.typeid = TYPE_RISKMODEL
        self.req = {}
        self.endPoint = 'risk-model'
        self.no_request_error_msg = 'Please create a new risk model or attach it to existing by doing set_id'
        self.jobs = None
        self.set_latest()

    def dates(self):
        if self.esvc is None:
            raise ValueError(self.no_request_error_msg)
        info = json.loads(self.esvc.get(""))
        return info['dates']

    def add_risk_factors(self, factors):
        self.req['add_factors'] = factors
        return self

    def remove_risk_factors(self, factors):
        self.req['remove_factors'] = factors
        return self
    
    def set_grouping(self, grouping_variable_name):
        self.req['grouping'] = grouping_variable_name
        return self

    def set_template(self, template):
        self.req['template'] = template
        return self

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
        request = self.req

        if request.get('user_data') is not None:
            print('Risk Model API: User data specified, will use dates/frequency from user data')
        
        request['universe'] = universe
        request['template'] = template
        request['startDate'] = startDate
        request['endDate'] = endDate
        request['freq'] = freq
        self.submit_new_request(request)

class BlackLitterman(Base):

    def __init__(self, conn):
        super().__init__(version = 2)
        self.set_conn(conn)
        self.req = {}
        self.endPoint = 'black-litterman'
        self.typeid = TYPE_BLACKLITTERMAN
        self.no_request_error_msg = 'No Black litterman request associated with the instance. Either run a new one or attach successful UUID'    

    def set_prior_return(self, prior_return, horizon):
        self.req['prior'] = {
            'factor': prior_return,
            'horizon' : horizon
        }
        return self
        
    def _views_(self):
        views = self.req.get('views')
        if views is None:
            views = []
            self.req['views'] = views
        return views

    def _check_exclusive_(self, v1, v2, n1, n2, f1):
        if v1 is not None and v2 is not None:
            raise Exception("Cannot Specify {} and {} in the call to {}",n1,n2,f1)

    def add_view_model_scores(self, view_name, model_scores,return_horizon,information_coefficient = None,
                              information_coefficient_half_life = None,
                              volatility_adj_scores = False,
                              uncertainty_kappa_empirical = None,
                              uncertainty_diagonal_empirical = None
                              ):
        view = {
            'name': view_name,
            'type': 'factor',
            'factor': model_scores,
            'return_horizon': return_horizon
        }
        self._check_exclusive_(information_coefficient,information_coefficient_half_life,'information_coefficient','information_coefficient_half_life','add_view_model_scores')
        if information_coefficient is not None:
            view['information_coefficient'] = information_coefficient
        
        if information_coefficient_half_life is not None:
            view['information_coefficient_half_life'] = information_coefficient_half_life

        if volatility_adj_scores:
            view['volatility_adj_scores'] = "TRUE"
        
        if not uncertainty_kappa_empirical is None:
            view['uncertainty_kappa_empirical'] = uncertainty_kappa_empirical
        
        if not uncertainty_diagonal_empirical is None:
            view['uncertainty_diagonal_empirical'] = uncertainty_diagonal_empirical
        
        self._views_().append(view)
        return self
    
    def add_view_price_target(self, view_name, price_target,return_horizon, uncertainty_kappa):

        view = {
            'name': view_name,
            'type': 'price_target',
            'factor': price_target,
            'return_horizon': return_horizon,
            'uncertainty_kappa': uncertainty_kappa
        }
        self._views_().append(view)
        return self
    
    def add_view_buy_sell_rating(self, view_name, buy_sell_rating,return_horizon, information_coefficient,information_coefficient_half_life,
                volatility_adj_scores, uncertainty_kappa):
        view = {
            'name': view_name,
            'type': 'recommendation',
            'factor': buy_sell_rating,
            'return_horizon': return_horizon,
            'uncertainty_kappa': uncertainty_kappa
        }
        self._check_exclusive_(information_coefficient,information_coefficient_half_life,'information_coefficient','information_coefficient_half_life','add_view_buy_sell_rating')
        if information_coefficient is not None:
            view['information_coefficient'] = information_coefficient
        
        if information_coefficient_half_life is not None:
            view['information_coefficient_half_life'] = information_coefficient_half_life
            
        if volatility_adj_scores:
            view['volatility_adj_scores'] = "TRUE"
        if volatility_adj_scores:
            view['volatility_adj_scores'] = "TRUE"

        self._views_().append(view)
        return self

class PortSimulatorOutput:
    
    def __init__(self, init_cash, output, data = None):
        self.output = output
        self.init_cash = init_cash
        if data is None:
            self.data = output.get_data()['result']
        else:
            self.data = data['result']
        dates = list(self.data.keys())
        dates.sort()
        self.dates = dates
        
    def _v_(self,name):
        v = pd.concat([self.data[dt][name] for dt in self.dates])
        v.index = [datetime.strptime(x,'%Y-%m-%d') for x in v.index]
        return v

    def _v2_(self,name):
        return pd.Series([self.data[dt][name].x.iloc[0] for dt in self.dates], index = self.dates)
    
    def _m_(self,name):
        return pd.concat([self.data[dt][name] for dt in self.dates],axis=1)
    
    def cash(self):
        return self._v_('cash')
    
    def shares_traded(self):
        return self._m_('shares_traded')
    
    def shares(self):
        return self._m_('shares')
    
    def short_values(self):
        return self._v_('short_values')
    
    def long_values(self):
        return self._v_('long_values')
    
    def net_values(self):
        return self.values().add(self.cash())
    
    def value_traded(self):
        return self._m_('value_traded')
    
    def next_notional(self):
        return self._v2_('next_notional')
    
    def target_notional(self):
        return self._v2_('target_notional')
    
    def realized_notional(self):
        return self._v2_('realized_notional')
    
    def values(self):
        return self._v_('values')
    
    def exec_price(self):
        return self._m_('exec_prc')

    def div_payout(self):
        return self._v_('div_accum')
    
    def returns(self):
        return self.net_values().pct_change()
    
    def get_user_data(self):
        return self.output.get_user_data()

class PortfolioSimulator(Base):
    def __init__(self, conn):
        super().__init__(version = 2)
        self.set_conn(conn)
        self.req = {'options':{}}
        self.endPoint = 'portsimulator'
        self.typeid = TYPE_SIMULATOR
        self.cash = None
        self.no_request_error_msg = 'No Portfolio Simulation request associated with the instance. Either run a new one or attach successful UUID' 

    def set_capital(self,currency: str, cash: float,notional: float):
        self.req['currency'] = currency
        self.req['cash'] = cash
        self.cash = cash
        self.req['notional'] = notional
        return self

    def set_weight_factor(self, weight_factor: str):
        self.req['weightFactor'] = weight_factor
        return self
    
    def set_last_date(self, last_date: str):
        self.req['last_date'] = last_date
        return self
    
    def set_txn_cost_function(self, function: str):
        self.req['txn_cost_function'] = function
        return self

    def set_max_vol_participation(self, max_part: float):
        self.req['options']['max_participation'] = max_part
        return self
    
    def use_vwap(self):
        self.req['options']['use_vwap'] = 'true'
        return self

    def set_ignore_dividend(self):
        self.req['options']['ignore_div'] = 'true'
        return self

    def set_grow_notional(self, grow_notional: bool):
        self.req['options']['grow_notional'] = str(grow_notional)
        return self

    def get_results(self):
        return PortSimulatorOutput(self.cash,self.get_output())


class AttributionResult:
    
    def __init__(self, output):
        self.output = output
        
    def get_summary(self):
        return self.output.get_data('MN_summary.csv')['summary']
    
    def __get_ts_data__(self, name, _type = 'MN'):
        return self.output.get_data('ts_data/{}_{}.csv'.format(_type,name))['ts_data'][name]
    
    def get_correlation(self):
        return self.__get_ts_data__('CORRELATION')
    
    def get_cum_return_contribution(self):
        return self.__get_ts_data__('CUM_RETURN_CONTRI')
        
    def get_daily_cum_return_contribution(self):
        return self.__get_ts_data__('DAILY_CUM_RETURN_CONTRI')
    
    def get_daily_factor_cum_return(self):
        return self.__get_ts_data__('DAILY_FACTOR_CUM_RETURN')
    
    def get_daily_factor_return(self):
        return self.__get_ts_data__('DAILY_FACTOR_RETURN')
    
    def get_daily_return_contribution(self):
        return self.__get_ts_data__('DAILY_RETURN_CONTRI')
    
    def get_exposures(self):
        return self.__get_ts_data__('EXPOSURE')
    
    def get_factor_cum_return(self):
        return self.__get_ts_data__('FACTOR_CUM_RETURN')
    
    def get_factor_decile(self):
        return self.__get_ts_data__('FACTOR_DECILE')
    
    def get_factor_return(self):
        return self.__get_ts_data__('FACTOR_RETURN')

    def get_factor_volatility(self):
        return self.__get_ts_data__('FACTOR_VOL')
    
    def get_return_contribution(self):
        return self.__get_ts_data__('RETURN_CONTRI')
    
    def get_risk_contribution(self):
        return self.__get_ts_data__('RISK_CONTRI')
    
    def get_risk_contribution_percentage(self):
        return self.__get_ts_data__('RISK_CONTRI_PCT')
    
    def get_vol_adjusted_exposure(self):
        return self.__get_ts_data__('VOL_ADJ_EXPOSURE')
    
    def get_weight_summary(self):
        return self.__get_ts_data__('WEIGHT_SUMMARY')
    

class Attribution(Base):
    def __init__(self, conn):
        super().__init__(version = 2)
        self.set_conn(conn)
        self.req = {}
        self.endPoint = 'attribution'
        self.typeid = TYPE_SIMULATOR
        self.cash = None
        self.no_request_error_msg = 'No Attribution request associated with the instance. Either run a new one or attach successful UUID' 

    def set_risk_model(self, risk_model: str):
        self.req['risk_model'] = risk_model
        return self

    def set_weight_factor(self, weight_factor = 'WEIGHT'):        
        self.req['weightAttribute'] = weight_factor
        return self
    
    def set_last_date(self, last_date: str):
        self.req['last_date'] = last_date
        return self

    def get_results(self):
        return AttributionResult(self.get_output())

        
class UserData:

    def __init__(self, connection):
        self.connection = connection

    def upload_data(self, file_path_or_data, name):
        '''
        Uploads data to user environment
        Input arguments
        :param data: Pandas Data frame
        :param name: Name to associate the data with
        '''
        if type(file_path_or_data) == str:
            file_path = file_path_or_data
            res = self.connection.upload_file(file_loc = file_path, name = name)
        else:
            file_descriptor, file_path = tempfile.mkstemp(suffix='.csv')
            file_path_or_data.to_csv(path_or_buf=file_path, index=False)
            res = self.connection.upload_file(file_loc = file_path, name = name)
            try: # Try to remove the temporary file
                os.unlink(file_path)
            except:
                print("Failed to remote temporary file")
            
            
        return res.text

    def list_data(self):
        v = self.connection.get('port')
        if v is None:
            return None
        v = pd.read_json(v)
        v.Uploaded = v.Uploaded.apply(lambda x: datetime.fromtimestamp(x / 1e3))
        v = v.sort_values(by=['Uploaded'], ascending = False)
        return v
    
    def delete_data(self, name):
        v = self.connection.delete('port/{}'.format(name))
        return v

    def exists(self,name):
        df = self.list_data()
        if df.empty: 
            return False
        if sum(df.Name == name) > 0:
            return True
        return False
