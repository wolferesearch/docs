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
import re

TYPE_RISKMODEL = 1
TYPE_OPTIMIZATION = 2
TYPE_BLACKLITTERMAN = 7
TYPE_ATTRIBUTION = 3
TYPE_SIMULATOR = 8
TYPE_HEDGE = 9

class Connection:
    """
    Connenection Class gets initialized using username and password simplify the process to call functional APIs.
    This is a gateway class, so it allows you to access other services, such as

    1. Optimizer
    2. Risk Model Builder
    3. Attribution
    4. Black Litterman
    5. Portfolio Simulator
    6. Hedge

    """
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
            body = json.dumps(body,separators=(',', ':'))
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
    
    def delete_template(self, typeid, name):
        return self.delete("template/{}/{}".format(typeid,name))

    def delete_risk_template(self, name):
        return self.delete_template(TYPE_RISKMODEL,name)

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
    
    def get_hedge_builder(self):
        return HedgeBuilder(self)

    def get_catalog(self):
        return Catalog(self)

    def upload_file(self,file_loc, name, end_point = 'port'):
        print('Calling Uploading {} to {} ...'.format(file_loc, name))
        response = self.session.post(self.URL + '/' + end_point, files = {'file': open(file_loc,'rb')}, data = {'name': name})
        print(response.text)
        return response

class Catalog:
    """
    Catalog Class to browse universes, factors and templates
    """
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
    """
    Job Output wrapper. Usually returned by the child class of     :class:`~pyqes.micsvc.Base`

     Class allows to do the following:\n
         1. Get the raw output of the job.\n
         2. Gets the user data associated with the job\n

    """

    def __init__(self, conn, uuid, files):
        self.conn = conn
        self.uuid = uuid
        self.files = files
        self.udata = None
        self.data = {}

    def __file__(self, key):
        return key[(key.find('_')+1):len(key)]

    def sym_mapping(self):
        return self.get_data('D_mapping.csv')['mapping']
        
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
    """
    Entity class to manage for the service. Usually managed by :class:`~pyqes.micsvc.Base`

    """
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
    """
    Base Template Class set up the argument for API function. Templates are saved parameters that can be used across other micro services. Types of services available:

    1. Optimization
    2. Risk Model
    3. Attribution
    4. Black-Litterman
    5. Portfolio Simulator

    """
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
        """Returns name of the template.

        Returns: str
        -------
        Name of the Template
        """
        return self.val['NAME']

    def type(self):
        """Type of the template.

        Returns: int
        -------
        The type can be either TYPE_OPTIMIZATION, TYPE_RISKMODEL, TYPE_ATTRIBUTION, TYPE_PORTSIMULATOR, TYPE_BLACKLITTERMAN
        """
        return self.val['TYPE']

    def description(self):
        return self.val['DESCRIPTION']

    def content(self):
        """ Returns content of the template

        Returns: dict
        -------
        Content of the template. The dictionay can be nested. 
        """
        return self.json

    def save(self, name):
        """ Saves the template with a name. Note that templates are immutable, hence in order to save changes it should be assigned a unique name. 

        Returns: self
        -------
        
        """
        self.json['name'] = name
        self.json['__name__'] = name
        typeMap = {
            "Risk-Model": "risk-model",
            "Optimization" : "optimization"
        }
        self.conn.post('template/' + typeMap.get(self.type()), self.json)
        return self

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
    """Risk Model Template inherited from the main template class. Allows users to save parameters. The template allows user to do the following:
    
    1. Add factors
    2. Add meta factors
    3. Update options. For more information on options, please contact QES Team
    4. Modify covariance arguments. For more information on covariance arguments, please contact QES Team
    5. Update specific risk shrinkage

    The template should be saved after modifying in order to use in risk mode calculations. 
    """
    def __init__(self,conn,raw):
        Template.__init__(self,conn,raw)

    def factors(self):
        """Get list of factors in the template.

        Returns: list
        -------
        List of factors in the template
        """       
        return self.json['factors']
    
    def meta(self):
        """Get list of meta factors in the template.

        Returns: list
        -------
        List of meta factors in the template
        """ 
        return self.json['meta']
    
    def cov_matrix_ags(self):
        """Get covariance matrix args. For full list of arguments, please contact QES Team.

        Returns: dictionary
        -------
        Parameters of Covariance Matrix. 
        """ 
        return self.json['covArgs']
    
    def options(self):
        """Get options for the risk model. For full list of options, please contact QES Team.

        Returns: dictionary
        -------
        Dictionary with parameters for risk model 
        """ 
        return self.json['options']

    def add_factor(self, mnemonic, name):
        """Add factor the template.

        Parameters
        ----------
        mnemonic: str
            ID of the factor. Should be one of the factors in QES library or uploaded user data.
        name: str
            Name of the factor
            
        Returns: self
        -------
        
        """ 
        factor_ls = self.factors()
        factor_ls.append({'mnemonic':mnemonic, 'name':name})
        self.json['factors'] = factor_ls
        return self

    def add_meta(self, mnemonic, name):
        """Add meta factor to the template.

        Parameters
        ----------
        mnemonic: str
            ID of the factor. Should be one of the factors in QES library or uploaded user data.
        name: str
            Name of the factor
            
        Returns: self
        -------
        Returns instance of itself
        """         
        meta_ls = self.meta()
        meta_ls.append({'mnemonic': mnemonic, 'name': name})
        self.json['meta'] = meta_ls
        return self

    def set_cov_matrix_interval(self, interval):
        """Sets covariance matrix interval (sampling frequency).

        Parameters
        ----------
        interval: int
            Frequency for the sample covariance matrix. Should be in business days. 
            
        Returns: self
        -------
        Returns instance of itself
        """            
        self.json['covArgs']['interval'] = interval
        return self

    def set_cov_matrix_var_half_life(self, var_half_life):
        """ Sets the half life for Variance computation (Diagonal).

        Parameters
        ----------
        var_half_life: int
            Half life in # of intervals. If the interval is 1 day, and half life is 60, it is 60 days. If interval is 3 days, and half life is 40, it would be 120 days.  
            
        Returns: self
        -------       
        Returns instance of itself 
        """
        self.json['covArgs']['var.period'] = var_half_life
        return self

    def set_cov_matrix_covar_half_life(self, covar_half_life):
        """ Sets the half life for Covariance computation (Off-Diagnoal).

        Parameters
        ----------
        covar_half_life: int
            Half life in # of intervals. If the interval is 1 day, and half life is 60, it is 60 days. If interval is 3 days, and half life is 40, it would be 120 days.  
            
        Returns: self
        ------
        Returns instance of itself
        """
        self.json['covArgs']['cov.period'] = covar_half_life
        return self
    
    def set_beta_shrinkage(self, shrinkage: float):
        """
            Sets shrinkage for beta estimator. The value should be between 0 and 1. 
            
        Parameters
        ----------
        shrinkage: float [0-1]
            Intensity of shrinkage. 0 is no shrinkage and 1 is shrunk to all way to Z-score.  
            
        Returns: self
        ------
            Returns instance of itself
        """ 
        if shrinkage > 1:
            raise ValueError('Shrinkage cannot be greater than one')
        elif shrinkage < 0:
            raise ValueError('Shrinkage cannot be less than 0')
        self.json['options']['betaShrinkageFactor'] = shrinkage
        return self           

    def set_specific_risk_shrinkage(self, shrinkage):
        """ Sets shrinkage for specific risk. If 0 then specific risk is not shrunk to industry/global median. 

        Parameters
        ----------
        shrinkage: float [0-1]
            Intensity of shrinkage. 0 is no shrinkage and 1 is shrunk to all way to Industry and Global medians.   
            
        Returns: self
        ------
            Returns instance of itself
        """        
        if shrinkage > 1:
            raise ValueError('Shrinkage cannot be greater than one')
        elif shrinkage < 0:
            raise ValueError('Shrinkage cannot be less than 0')
        self.json['options']['spRisk']['shrinkage'] = shrinkage
        return self
       
class Base:
    """
     Base class for Optimizer/RiskModel/Attribution/Black Litterman job runners.

     Class allows to do the following:\n
         1. Check status of the job.
         2. Get Info about the job, i.e, Start Time End Time etc\n
         3. Get output for the job. The child class wraps the output object\n
         4. Get logs for the job\n
         
     """
    def __init__(self, version = 1):
        self.conn = None
        self.esvc = None
        self.version = version

    # Getter
    def completed(self):
        """Get list of completed job for this type of jobs.

        Returns
        -------
        Jobs as Pandas data frame
        """

        self.check_conn() # Check for connection first
        return self.conn.success_jobs(self.typeid)

    def failed(self):
        """Get list of failed job for this type of jobs.

        Returns
        -------
        Jobs as Pandas data frame
        """

        self.check_conn()
        return self.conn.failed_jobs(self.typeid)

    def info(self):
        """Gets info as dictionary of the runner

       Returns: dict
       -------
       Dictionary. Information about the job.
       """

        if self.esvc is None:
            raise ValueError('Please create a new {} or attach it to existing by doing set_id'.format(self.endPoint))
        return json.loads(json.dumps(self.esvc.info()))

    def status(self):
        """Gets status of the job. Completed/Started/Error

       Returns: str
       -------
       String. Status of the job
       """
        return self.info()['status']

    # Setter
    def set_conn(self, conn):
        self.conn = conn

    def set_id(self, uuid):
        """Sets UUID for a previously run. Useful when trying to fetch data for a previously run job

        Parameters
        ----------
        uuid: str
            UUID. Unique identifier for the job.
       Returns: None
       -------

       """

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
        """Waits for job to finish.

        Parameters
        ----------
        max_wait_secs: int
            Maximum wait time.
       Returns:
       -------
       Entity Service Class
       """

        if self.esvc is None:
            raise ValueError('No Optimization Associated with the class, either set id or create new optimization request')
        return self.esvc.wait(max_wait_secs)
    
    def submit_new_request(self, req):
        """Submits the job.

        Parameters
        ----------
        req: dict
            Request object with parameters
       Returns: self
       -------
       Instance of the job runner class.
       """
        self.esvc = None
        self.data = None
        endPoint = self.endPoint   # service argument
        # if type(req) == dict:
        #     req = str(req).replace('\'', '"')
        # call the API and get the respective uuid
        if self.version == 1:
            response = self.conn.post(endPoint, req)
        elif self.version == 2:
            response = self.conn.post('job/submit/' + endPoint, req)
        else:
            raise Exception("Unexpected Version {}. Only Version=1/2 are supported.".format(self.version))

        # self.req = req
        self.esvc = EntityService(self.conn, endPoint, response, self.version)
        return self
    
    def get_logs(self):
        """Gets logs associated with the job

       Returns: str
       -------
       Logs as a string
       """
        if self.esvc is None:
            raise Exception("Either attach an existing UUID or run a new one")
        
        return self.esvc.get_logs()
    
    def get_output(self):
        if self.esvc is None:
            raise Exception("Either attach an existing UUID or run a new one")
        return self.esvc.get_job_output()

    def set_user_data(self, name, data, overwrite = True):
        """Get a pandas data frame with User data and Optimized Weights for a single date

        Parameters
        ----------
        name: str
            Name to identify the portfolio
        data: `panda.DataFrame`
            Pandas data frame with Identifier, Date, Metrics
        overwrite: bool
            Boolean flag if the data should be overwritten


       Returns
       -------
       Returns object of the job runner
       """
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
    """
    Optimizer Result Class

    Class allows to do the following:\n
        1. Inspect optimized weight matrix.
        2. Inspect the turnover\n
        3. Inspect the notional and returns\n
        4. Get portfolio on a date\n
        5.Uploads custom data
    """
    def __init__(self, output):
        self.output = output

    def sym_mapping(self):
        return self.output.sym_mapping()

    def __get__(self, name):
        return self.output.get_single_data(name)

    def get_old_weights(self):
        return self.__get__('old_weights.csv')

    def get_old_weights_2(self):
        return self.__get__('old_weights_2.csv')

    def get_weights(self):
        """Gets the Weight of the optimization portfolio. This will return a matrix with
        security ids in rows and dates in columns

        Returns
        -------
        Pandas data matrix with security in rows and dates in column

        """
        return self.__get__('weights.csv')
        
    def get_notional_value(self):
        """Gets the notional value of the portfolio. This will be a time series of float.

        Returns
        -------
        Pandas data series with dates as rows and one column
        """
        return self.__get__('notional_value.csv')

    def get_tracking_error(self):
        """Gets the tracking error as time series. Only available when benchmark is set

       Returns
       -------
       Pandas data series with dates as rows and one column with tracking error
       """
        return self.__get__('tracking_error.csv')

    def get_alpha(self):
        """Gets the ex-ante alpha score. This is computed by taking the inner product of weight and alpha vectors
        on each date.

       Returns
       -------
       Pandas data series with dates as rows and one column with alpha
       """
        return self.__get__('alpha.csv')

    def get_old_notional_value(self):
        return self.__get__('old_notional_value.csv')

    def get_required_turnover(self):
        """Gets the required (minimum) turnover. This is based on the constraints for new portfolio compare to
        the previous portfolio prior to rebalance

       Returns
       -------
       Pandas data series with dates as rows and one column with required turnover
       """

        return self.__get__('required_turnover.csv')
    
    def get_risk(self):
        """Gets the ex-ante risk of the strategy as time series.

       Returns
       -------
       Pandas data series with dates as rows and one column with ex-ante risk
       """

        return self.__get__('risk.csv')

    def get_turnover(self):
        """Gets the turnover of the strategy as time series.

       Returns
       -------
       Pandas data series with dates as rows and one column with turnover
       """

        return self.__get__('turnover.csv')
    
    def get_portfolio(self, dated):
        """Get a pandas data frame with User data and Optimized Weights for a single date

        Parameters
        ----------
        dated: str YYYY-mm-dd
            Date for which the portfolio is needed


       Returns
       -------
       Pandas data frame joined with user data and identifier
       """

        user_data = self.output.get_user_data()
        df = user_data.get_data(dated)
        weights = self.get_weights()[[dated]]
        weights.columns = ['WEIGHT']
        return pd.merge(df, weights, left_index=True, right_index=True)
        


class Optimizer(Base):
    """
    Optimizer class for interfacing with the QES Hosted Optimizer

    Class allows to do the following:\n
        1.Run new optimization\n
        2.Pull data for previously run optimizations\n
        3.List all optimization (failed/successful)\n
        4.Download Weights and Summary file\n
        5.Uploads custom data
    """
    def __init__(self, conn):
        super().__init__(version = 2)
        self.set_conn(conn)
        self.req = {}
        self.endPoint = 'optimization'
        self.typeid = TYPE_OPTIMIZATION
        self.no_request_error_msg = 'No Optimization Associated with the class, either set id or create new optimization request'

    def set_max_ADV_trading_participation(self, max_ADV_part: float):
        """Sets upper limit on the trading to be fraction of the % of average trading volumne. 

        Parameters
        ----------
        max_ADV_part: float
            Maximum ADV Allowed to trade during rebalance.  

        Returns
        -------
        Optimizer Class Instances

        """        
        self.req['max_ADV_trading_participation'] = max_ADV_part
        self.req['use_ADV'] = True
        return self
    
    def set_max_ADV_holding_participation(self, max_ADV_part: float):
        """Sets upper limit on the holding to be fraction of the % of average trading volume. Note that this is evaluated only at the rebalance time. Between the 
        rebalance the portfolio can have holding > limit 

        Parameters
        ----------
        max_ADV_part: float
            Maximum ADV Allowed to hold on the rebalance date.   

        Returns
        -------
        Optimizer Class Instances

        """        
        self.req['max_ADV_holding_participation'] = max_ADV_part
        self.req['use_ADV'] = True
        return self
    
    def set_soft_ADV_trading_penalty(self, soft_ADV_penalty: float):
        """Sets penalty for ADV. This allows the ADV constraint to be soft.  

        Parameters
        ----------
        soft_ADV_penalty: float
            Penalty for violating the Trading ADV Constraint. A high value will ensure that optimizer stays within the limit. 

        Returns
        -------
        Optimizer Class Instances

        """        
        self.req['soft_ADV_trading_penalty'] = soft_ADV_penalty
        return self

    def set_soft_ADV_trading_penalty(self, soft_ADV_penalty: float):
        """Sets notional value for the portfolio. Is used when ADV consraint is used. 

        Parameters
        ----------
        soft_ADV_penalty: float
            Penalty for violating the Holding ADV Constraint. A high value will ensure that optimizer stays within the limit. 

        Returns
        -------
        Optimizer Class Instances

        """        
        self.req['soft_ADV_holding_penalty'] = soft_ADV_penalty
        return self

    def set_use_adv(self, use_adv: bool):
        self.req['use_ADV'] = use_adv
        return self


    def set_notional(self,init_notional_value: float, notional_value: float):
        """Sets notional value for the portfolio. Is used when ADV consraint is used. 

        Parameters
        ----------
        init_notional_value: float
            Initial Notional Value 
        notional_value: float
            Notional value of each rebalance

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['init_notional_value'] = init_notional_value
        self.req['notional_value'] = notional_value
        return self
    
    def set_template(self, template: str):
        """Sets the template to use. The template is the base optimizer template that provides default parameters
        for the optimization. List of templates can be pulled from Connection object.

        Parameters
        ----------
        objective: template
            Name of the template to be used, e.g., default

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['template'] = template
        return self

    def set_objective(self, objective: str):
        """Sets the objective function for the optimization. The optimizer supports:
        - MVO: Mean Variance Optimization. Lambda and Alpha should be provided in order to use this.
        - minRisk: Minimize Risk.
        - maxAlpha: Maximize Alpha. Alpha should be provided.

        Parameters
        ----------
        objective: str
            Objective Function, e.g., MVO, minRisk, or maxAlpha

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['objective'] = objective
        return self
    
    def set_alpha(self, alpha: str):
        """Sets the Alpha column in the CSV file.

        Parameters
        ----------
        alpha: str
            Column name of the alpha score. This is used when the objective function is either maxAlpha or MVO

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['alpha'] = alpha
        return self

    def set_adv_factor(self, adv_factor: str):
        """Sets the ADV factor to use for ADV control in the .

        Parameters
        ----------
        adv_factor: str
            Name of the supported ADV Factor

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['adv_factor'] = adv_factor
        return self
    
    def set_htb_threshold(self, threshold: float):
        """Sets the High to Borrow Threshold for excluding the short position. The threshold takes a value from 2-10.
        Higher value of this threshold will include securities in the short portfolio that are harder to short.
        Value of 10 will include all securities, same as default.

        Parameters
        ----------
        threshold: float
            Threshold of Hard to Borrow. This will exclude any securities from short securities that have score > threshold.

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['threshold'] = threshold
        return self

    def set_benchmark(self, benchmark: str):
        """Sets the Benchmark column in the CSV file.

        Parameters
        ----------
        benchmark: str
            Column name of the benchmark weight

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['use_benchmark'] = 'TRUE'
        self.req['benchmark'] = benchmark
        return self
    
    def set_init_portfolio(self, init_portfolio: str):
        """Sets the initial portfolio. This should be set as one of the column name.

        Parameters
        ----------
        init_portfolio: str
            Column name of the start initial portfolio in the uploaded CSV file

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['init_portfolio'] = init_portfolio
        return self
    
    def add_group_constraint(self, grouping_factor: str, min_exposure: float, max_exposure: float, benchmark: bool, 
                             transformation = None):
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
        transformation: dictionary
            Transformer function to convert the grouping_factor to categorical function.
            For example {'transformer':'binner',bins:[100,1000,10000,100000]}

        Returns
        -------
        Optimizer Class Instances

        """
        group_constraints = self.req.get('group_constraints')
        if group_constraints is None:
            group_constraints = []
            self.req['group_constraints'] = group_constraints
        group_constraints.append({'factor': grouping_factor, 'min' : min_exposure, 'max': max_exposure, 'benchmark' :str(benchmark), 
                                  'factor_tranformer': transformation})
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

        Returns
        -------
        Optimizer Class Instances

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

        Returns
        -------
        Optimizer Class Instances

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

        Returns
        -------
        Optimizer Class Instances

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

        Returns
        -------
        Optimizer Class Instances

        """
        neut_matrix = self.req.get('neutralization_matrix')
        if neut_matrix is None:
            neut_matrix = []

        neut_matrix.append({
            'bounds': {
                 'Factor': neutralization_factors,
                 'Min' : factor_min_exposure,
                 'Max' : factor_max_exposure
            },
            'benchmark': benchmark,
            'grouping_matrix': grouping_matrix 
        })
        self.req['neutralization_matrix'] = neut_matrix
        return self

    def set_benchmark(self, benchmark:str):
        self.req['use_benchmark'] = 'TRUE'
        self.req['benchmark'] = benchmark
        return self

    def set_bounds(self,lb:float, ub: float):
        """Sets weight bound for securities

        Parameters
        ----------
        lb: float
            Lower Bound. Minimum weight allowed for any security to take
        ub: float
            Upper Bound. Maximum weight allowed for any security to take

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['lb'] = lb
        self.req['ub'] = ub
        return self

    def set_target_risk(self, target_risk: float):
        """Sets the target risk. The value is in decimal, so 0.2 will indicate 20% annualized risk

        Parameters
        ----------
        target_risk: flowt
            Target Risk. Maximum risk allowed. Value is in decimal, so 0.2 will indicate 20% annualized risk

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['target_risk'] = target_risk
        return self

    def set_max_turnover(self, turnover: float):
        """Sets the maximum allowed turnover. The value is in fraction, e.g., 1.5 will be 150% turnover for each rebalance.
        For when the required turnover > max_turnover, the optimizer will fail

        Parameters
        ----------
        turnover: float
            Maximum Turnover Allowed.

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['turnover'] = turnover
        return self

    def set_max_number_securities(self, max_securities: int):
        """Sets the maximum number of securities with non-zero weight in the portfolio

        Parameters
        ----------
        max_securities: int
            Maximum number of securities with non-zero weights. The optimizer will try to keep the number
            of securities with non-zero weights below this number

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['limit_number'] = max_securities
        return self
    
    def set_min_number_securities(self, min_securities: int):
        """Sets the minimum number of securities with non-zero weight in the portfolio

        Parameters
        ----------
        min_securities: int
            Minimum number of securities with non-zero weights. The optimizer will try to keep the number
            of securities with non-zero weights above this number

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['min_number'] = min_securities
        return self
    
    def set_risk_model(self, risk_model: str):
        """Sets the risk model to use for the optimizer. For list of available risk model, please contact QES Team
        at luo.qes@wolferesearch.com

        Parameters
        ----------
        risk_model: str
            Risk Model Id. QES has several risk models that can be used for optimizer. Please contact the team for access.

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['risk_model'] = {'risk_model_id' : risk_model}
        return self
    
    def set_lambda(self, _lambda: float):
        """Sets the lambda for MVO problem. Note that this should be chosen carefully based on the units of Alpha.

        Parameters
        ----------
        _lambda: float
            Risk Aversion Factor(Lambda). The value is used to build objective function with Alpha (Linear)
            and Variance (Quadratic). Note that Variance

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['lambda'] = _lambda
        return self
    
    def set_implied_alpha(self, implied_alpha: bool):
        self.req['implied_alpha'] = str(implied_alpha)
        return self

    def set_min_holding(self, min_holding: float):
        """Sets the minimum holding weight for securities. This should be set to prevent optimizer from
        selecting securities with very small weights.

        Parameters
        ----------
        min_holding: float
            Minimum Weight for Holdings. THe value is in decimal, so a value of 0.002 will indicate that
            no securities with less than 20bps weight will be allowed in the optimized portfolio

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['min_holding'] = min_holding
        return self

    def set_min_long_weight(self, min_long_weight: float):
        """Sets the lower bound for total long exposure. A value of 0.9 will indicate that at least 90% of notional
        will be allocated to the long side of the portfolio

        Parameters
        ----------
        min_long_weight: float
            Minimum Long Side Exposure. The optimizer will allocate at least this much to the long side of the
            optimized portfolio

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['min_long_weight'] = min_long_weight
        return self

    def set_max_long_weight(self, max_long_weight: float):
        """Sets the upper bound for total long exposure. A value of 1.1 will indicate that at most 110% of notional
        will be allocated to the long side of the portfolio

        Parameters
        ----------
        max_long_weight: float
            Maximum Long Side Exposure. The optimizer will allocate at most this much to the long side of the
            optimized portfolio

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['max_long_weight'] = max_long_weight
        return self

    def set_min_short_weight(self, min_short_weight: float):
        """Sets the lower bound for total short exposure. A value of 0.9 will indicate that at least 90% of notional
        will be allocated to the short side of the portfolio

        Parameters
        ----------
        min_short_weight: float
            Minimum Short Side Exposure. The optimizer will allocate at least this much to the short side of the
            optimized portfolio

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['min_short_weight'] = min_short_weight
        return self
    
    def set_max_short_weight(self, max_short_weight: float):
        """Sets the upper bound for total short exposure. A value of 1.1 will indicate that at most 110% of notional
        will be allocated to the short side of the portfolio

        Parameters
        ----------
        max_short_weight: float
            Maximum Long Side Exposure. The optimizer will allocate at most this much to the short side of the
            optimized portfolio

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['max_short_weight'] = max_short_weight
        return self


    def set_use_tcm(self, use_tcm: bool):
        self.req['use_tcm'] = str(use_tcm)
        return self
    
    def set_transaction_cost_model(self, transaction_cost_model: str):
        """Sets the transaction cost model to be used. Please contact luo.qes@wolferesearch.com on getting access to these.

        Parameters
        ----------
        transaction_cost_model: str
            Id of the transaction cost model to be used. Please contact luo.qes@wolferesearch.com on getting access to these.

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['transaction_model'] = transaction_cost_model
        return self

    def set_transaction_cost(self, transaction_cost: float):
        """Sets a fixed transaction cost that is applied to turnover for return computation

        Parameters
        ----------
        transaction_cost: float
            Transaction Cost. Transaction cost as fraction of turnover, a 0.0005 cost will indicate 5bp of turnover
            value will be deducted

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['trans_cost'] = transaction_cost
        return self

    def set_soft_turnover_penalty(self, soft_turnover_penalty: float):
        """Sets the penalty function for turnover. The turnover function is added to the objective function when
        this is selected.

        Parameters
        ----------
        soft_turnover_penalty: float
            Multiplier for turnover term when added to the objective function.

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['soft_turnover_penalty'] = soft_turnover_penalty
        return self

    def set_soft_relative_weight_penalty(self, soft_relative_weight_penalty: float):
        """Sets the penalty function for weight deviation from the benchmark

        Parameters
        ----------
        soft_relative_weight_penalty: float
            Multiplier for weight deviation from benchmark.

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['soft_relative_weight_penalty'] = soft_relative_weight_penalty
        return self

    def set_relative_weight_min(self, relative_weight_min: float):
        """Sets lower bound constraint for the deviation from benchmark weight

        Parameters
        ----------
        relative_weight_min: float
            Minimum deviation from the benchmark. The value should be less than 0 to allow optimizer
            to select weights less than the benchmark for securities

        Returns
        -------
        Optimizer Class Instances

        """
        self.req['relative_weight_min'] = relative_weight_min
        return self

    def set_relative_weight_max(self, relative_weight_max: float):
        """Sets upper bound constraint for the deviation from benchmark weight

        Parameters
        ----------
        relative_weight_max: float
            Maximum deviation from the benchmark. The value should be greater than 0 to allow optimizer
            to select weights greater than the benchmark for securities

        Returns
        -------
        Optimizer Class Instances

        """

        self.req['relative_weight_max'] = relative_weight_max
        return self

    def get_results(self):
        """Gets the data associated with the optimizer. Prior to calling this submit and wait should be called to ensure
        there is an associated optimization. This will only when the status of the optimization is "Completed".


        Returns
        -------
        Optimizer Result Object :class:`~micsvc.OptimizerResult`

        """

        return OptimizerResult(self.get_output())

class RiskModel(Base):
    """Risk Model Generator. The class provides a simple interface for building custom risk model. It allows the caller to do the following:

    1. Choose a standard template for risk model 
    2. Choose a risk universe
    3. Change the parameters of risk model calculation
    4. Add/Remove factors from the template
    5. Add custom data

    """
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
        """Returns date list for which the risk model is built. The risk model should be in completed or success state. 

       Returns: list 
       -------
       List of dates YYYY-mm-dd
       """       
        if self.esvc is None:
            raise ValueError(self.no_request_error_msg)
        info = json.loads(self.esvc.get(""))
        return info['dates']

    def add_risk_factors(self, factors):
        """Add a list of factors to the risk model. The factor should either be in User data or one of the supported mnemonics in QES Library. Should be called prior to submitting the request. 

       Returns: list of str
       -------
       List of factors to add to the risk model
       """             
        self.req['add_factors'] = factors
        return self

    def remove_risk_factors(self, factors):
        """Removes factors from the risk model. Should be called prior to submitting the request. 

       Returns: list of str
       -------
       List of factors to remove. Note that if the factor is not in the template, it will ignore it. 
       """        
        self.req['remove_factors'] = factors
        return self
    
    def set_grouping(self, grouping_variable_name):
        """Sets the grouping (sector or industry) for the risk model. The factor should either be in User data or one of the supported mnemonics in QES Library. Should be called prior to submitting the request

       Returns: str
       -------
       Grouping Factor that will be used instead of default Industry Group.  
       """          
        self.req['grouping'] = grouping_variable_name
        return self

    def set_template(self, template):
        """Sets the template for the risk model. Templates are reusable parameters that can maintained independently. SHould be called prior to submitting the request. 

       Returns: list of str
       -------
       List of factors to remove. Note that if the factor is not in the template, it will ignore it. 
       """   
        self.req['template'] = template
        return self

    def get_data(self, dated):
        """Gets the data for the risk model. This will include the following:
        1. Exposure matrix 
        2. Meta data
        3. Factor Covariance Matrix
        4. Stock Specific Risk

        Parameters
        ----------
        dated: str YYYY-mm-dd
            Date for which the risk model data is needed. 


       Returns: str
       -------
       Dictionary of risk model data suite.  
       """          
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
        """Downloads all data to a local directory.
        1. Exposure matrix 
        2. Meta data
        3. Factor Covariance Matrix
        4. Stock Specific Risk

        Parameters
        ----------
        out_dir: str 
            Directory where the data should be saved. This should be a local directory. This should be called when the risk model is in Completed or Success state. 


       Returns: str
       -------
       Dictionary of risk model data suite.  
       """           
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
        """Submits a new Request for building risk model. This is an async all hence it will return immediate. The caller can poll for status to change to Completed or Success. 

        Parameters
        ----------
        universe: str
            Universe Id. Should be one of the supported universes in QES library. 
        template: str
            Name of the Template. Should be one of the templates saved prior to calling this. 
        startDate: str date YYYY-mm-dd
            Start date for the risk model
        endDate: str date YYYY-mm-dd
            End date for the risk model
        freq: str 1d,2d,..,1w, 2w,..1m,2m,..1q,2q,..1y,2y
            Frequency of when to re-evaluate the risk model. 

       Returns: self
       -------
       Instance of the same class
       """        
        request = self.req

        if request.get('user_data') is not None:
            print('Risk Model API: User data specified, will use dates/frequency from user data')
        
        request['universe'] = universe
        request['template'] = template
        request['startDate'] = startDate
        request['endDate'] = endDate
        request['freq'] = freq
        self.req = request
        return self.submit_new_request(request)

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
    
    def __init__(self, init_cash, output, data = None, version = 1):
        self.output = output
        self.init_cash = init_cash
        self.version = version
        if data is None:
            self.data = output.get_data()['result']
        else:
            self.data = data['result']
        
        if version == 2:
            dates = list(self.data['dates'].x)
        else:
            dates = list(self.data.keys())
            dates.sort()
        self.dates = dates
        self.include_interest = True
        self.include_shorting_fees = True
        
    
    def sym_mapping(self):
        return self.output.sym_mapping()


    def _v_(self,name):
        if self.version == 2:
            v = self.data[name]
        else:
            v = pd.concat([self.data[dt][name] for dt in self.dates])
            
        if type(v.index[1]) == str:
            v.index = [datetime.strptime(x,'%Y-%m-%d') for x in v.index]
        return v

    def _v2_(self,name):
        if self.version == 2:
            return self._v_(name)
        return pd.Series([self.data[dt][name].x.iloc[0] for dt in self.dates], index = self.dates)
    
    def _m_(self,name):
        if self.version == 2:
            return self.data[name] 
        else:
            return pd.concat([self.data[dt][name] for dt in self.dates],axis=1)
    
    def cash(self):
        return self._v_('cash')
    
    def earned_interest(self):
        return self._v_('earned_interest')
    
    def shorting_fees(self):
        return self._v_('shorting_fees')
    
    def shares_traded(self):
        return self._m_('shares_traded')
    
    def daily_pnl(self):
        return self._m_('daily_pnl')
    
    def shares(self):
        return self._m_('shares')
    
    def short_values(self):
        return self._v_('short_values')
    
    def long_values(self):
        return self._v_('long_values')
    
    def net_values(self):
        vals = self.values().add(self.cash())
        if self.include_interest:
            vals = vals.add(self.earned_interest())
        if self.include_shorting_fees:
            vals = vals.add(-self.shorting_fees())
        return vals
    
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
        self.req = {'options':{},'serialization_version':2}
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
    
    def set_funding_spread(self, spread: float):
        self.req['funding_spread'] = spread
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
        return PortSimulatorOutput(init_cash = self.cash,output = self.get_output(), 
                                   data = None,
                                   version = self.req['serialization_version'])


class AttributionResult:
    
    def __init__(self, output):
        self.output = output
    
    def sym_mapping(self):
        return self.output.sym_mapping()

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

class HedgeBuilder(Base):
    def __init__(self, conn):
        super().__init__(version = 2)
        self.set_conn(conn)
        self.req = {}
        self.endPoint = 'hedge' # TODO: Check if the syntax is hedge-builder
        self.typeid = TYPE_HEDGE
        self.cash = None
        self.no_request_error_msg = 'No Hedge request associated with the instance. Either run a new one or attach successful UUID' 

    def set_risk_model(self, risk_model: str):
        self.req['risk_model'] = risk_model
        return self
    
    def set_template_name(self, template_name: str):
        self.req['template'] = template_name
        return self

    def set_notional_value(self, notional_value):
        self.req['notional_value'] = notional_value
        return self

    def set_hedge_type(self, hedge_type):
        '''LONG_SHORT, LONG_ONLY, SHORT_ONLY, not case sensitive'''
        self.req['hedge_type'] = hedge_type
        return self

    def set_factor_to_hedge(self, factor_to_hedge):
        '''list of one or more SECTOR, STYLE, COUNTRY, SYSTEMATIC, or other fator name, case sensitive'''
        self.req['factor_to_hedge'] = factor_to_hedge
        return self

    def set_factor_to_neutralize(self, factor_to_neutralize):
        '''list of one or more SECTOR, STYLE, COUNTRY, SYSTEMATIC, or other fator name, case sensitive'''
        self.req['factor_to_neutralize'] = factor_to_neutralize
        return self

    def set_auto_neutralization(self, auto_neutralization: bool):
        '''default is True'''
        self.req['auto_neutralization'] = auto_neutralization
        return self

    def set_max_number_of_stocks(self, max_number_of_stocks):
        self.req['max_number_of_stocks'] = max_number_of_stocks
        return self

    def set_max_neutral_exposure(self, max_neutral_exposure):
        self.req['max_neutral_exposure'] = max_neutral_exposure
        return self

    def set_max_gross_exposure(self, max_gross_exposure):
        self.req['max_gross_exposure'] = max_gross_exposure
        return self

    def set_max_weight(self, max_weight):
        self.req['max_weight'] = max_weight
        return self

    def set_min_weight(self, min_weight):
        self.req['min_weight'] = min_weight
        return self

    def set_max_adv_usage(self, max_adv_usage):
        self.req['max_adv_usage'] = max_adv_usage
        return self

    def set_default_universe(self, default_univ):
        '''FMP_UNIV or CORE_FMP_UNIV, not case sensitive'''
        self.req['default_univ'] = default_univ
        return self

    def set_exclude_condition(
            self, 
            ma_target: bool, 
            hard_to_borrow : bool, 
            earning_release_names: bool,
            dual_listings: bool,
            portfolio_holdings: bool, 
            firmwide_restrictions: bool
        ):
        self.req['exclusions'] = {
            'ma_target': ma_target, 
            'hard_to_borrow': hard_to_borrow,
            'earning_release_names': earning_release_names, 
            'dual_listings': dual_listings,
            'portfolio_holdings': portfolio_holdings, 
            'firmwide_restrictions':firmwide_restrictions
        }
        return self
    
    def set_hedge_universe(self, universe_ids:list, 
                           include_gics:list = [], 
                           exclude_gics:list = [],
                           min_mktcap_usd:float = 0.0,
                           max_mktcap_usd:float = -1,
                           min_adv_usd:float = 0.0,
                           max_adv_usd:float = -1, 
                           exclude_tickers:list = []):
        """ Sets the Hedge Universe for building the portfolio. User can specify, 
        any of the supported Universe (e.g., US_1, CORE_FMP). Further filtering can be
        done based on Sector (GICS) and liquidity. See `micsvc.Hedgebuilder.set_exclude_condition` to further 
        constraint the portfolio. 

        Parameters
        ----------
        universe_ids : list
            Ids of the universes. Should be one of the supported ones, e.g., SP500
        include_gics : list, optional
            List of GICS to be included by default all
        exclude_gics : list, optional
            List of GICS to be excluded, by default none
        min_mktcap_usd : int, optional
            Minimum Market Cap in the portfolio by default 0
        max_mktcap_usd : int, optional
            Maximum Market Cap in the portfolio by default -1
        min_adv_usd : int, optional
            Minimum ADV (in USD) in the portfolio
        max_adv_usd : int, optional
            Maximum ADV (in USD) in the portfolio
        exclude_tickers : list, optional
            List of Tickers (exchange) to exclude

        Returns
        -------
        _type_
            _description_
        """
        self.req['hedge_univ'] = {
            'universe_ids' : universe_ids,
            'include_gics' : include_gics,
            'exclude_gics' : exclude_gics,
            'min_mktcap_usd' : min_mktcap_usd,
            'max_mktcap_usd' : max_mktcap_usd,
            'min_adv_usd' : min_adv_usd,
            'max_adv_usd' : max_adv_usd,
            'exclude_tickers': exclude_tickers
        }
        return self

    def set_scalars(self, scalars):
        '''list of float point'''
        self.req['scalars'] = scalars
        return self

    def set_hedge_ratio(self, hedge_ratio):
        '''RISK or EXP or VOLADJEXP'''
        self.req['hedge_ratio'] = hedge_ratio
        return self

    def add_factor_constraint(self, name, lb, ub, type_='Factor', constraint_type='Numerical', target='AfterHedge', include_target_factors=False):
        self.req['factor_constraints'].append({'name': name, 'lb': lb, 'ub': ub, 'type': type_, 'constraint_type': constraint_type, 'target': target, 'include_target_factors': include_target_factors})
        return self
    
    def get_results(self):
        return HedgeOutput(self.get_output())


class HedgeOutput:
    def __init__(self, output):
        self.output = output
    
    def __get__(self, f1, f2):
        return self.output.get_data('{}/{}'.format(f1, f2)).get(f1).get(f2)

    def get_basket_ids(self):
        fls = [x for x in self.output.files.Key if bool(re.search('^baskets\/D_(S[0-9]{4}).csv$',x))]
        basket_ids = [re.sub('^baskets\/D_(S[0-9]{4}).csv$','\\1',x) for x in fls]
        return basket_ids

    def get_baskets(self):
        return self.output.get_data('baskets').get('baskets')
    
    def get_basket(self, basket_name):
        return self.__get__('baskets', 'D_{}.csv'.format(basket_name))
    
    def get_standalone_summary(self):
        return self.__get__('summary', 'standalone_summary')

    def get_afterhedge_summary(self):
        return self.__get__('summary', 'afterhedge_summary')

    def get_standalone_attribution(self):
        return self.__get__('analysis', 'standalone_attr')

    def get_afterhedge_attribution(self):
        return self.__get__('analysis', 'afterhedge_attr')
        
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
