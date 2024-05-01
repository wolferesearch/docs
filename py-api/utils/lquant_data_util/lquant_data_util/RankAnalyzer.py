from lquantPy import LQuant
import pandas as pd

def _R_to_num_list(v):
    return 'c(' + ','.join([str(x) for x in v]) + ')'
    
def _R_to_str_list(v):
    return 'c("' + '","'.join(v) + '")'

def _R_from_dict_to_list(dic):
    return "list(" + ",".join(['`' + k + '` = "' + v + '"'  for (k,v) in dic.items()]) + ")"

def _R_to_num_list_of_list(list_of_list):
    return 'list(' + ','.join([_R_to_num_list(x) for x in list_of_list]) + ')'
    
def rankdb_save_to_db(env, data, name, subindices = {}):
    env.run('source("/mnt/ebs1/data/common/R/rankdb.R")')
    env.run('rankdb.add(data = ' + data.name() + ', dbname = "' + name + '", subindices = ' + _R_from_dict_to_list(subindices) + ')')
    return True    

def quantdb_save_to_db(env, data, name, subindices = {}):
    env.run('source("/mnt/ebs1/data/common/R/rankdb.R")')
    env.run('quantdb.add(data = ' + data.name() + ', dbname = "' + name + '", subindices = ' + _R_from_dict_to_list(subindices) + ')')
    return True    
    
def _quote(v):
    if v is None:
        return 'NULL'
    else:
        return LQuant.LQEnv._quote(v)

class RankParams:
    def __init__(self, historic):
        self.historic = historic
        self.args = {}
        
    def bins(self, n):
        self.args['bins'] = n
        return self
    def index(self, _index):
        self.args['index'] = _quote(_index)
        return self
    def setid(self,_id):
        self.args['id'] = _quote(_id)
        return self
    def gics(self,gics):
        self.args['gics'] = _quote(gics)
        return self
    def factor(self,factor):
        self.args['factor'] = _quote(factor)
        return self
    def dated(self,dated):
        self.args['dated'] = _quote(dated)
        return self
    def desc(self):
        self.args['desc'] = 'T'
        return self
    def make_args(self):
        if self.historic and 'dated' in self.args.keys():
            self.args.pop('dated')
        if not self.historic and 'factor' in self.args.keys():
            self.args.pop('factor')
        return self.args


def make_rank_params(id, dated, index, gics, bins, desc):
    params = RankParams(False)
    params.setid(id).dated(dated).index(index).gics(gics).bins(bins)
    if (desc):
        params.desc()
    return params.make_args()

def make_history_rank_params(id, factor, index, gics, bins, desc):
    params = RankParams(True)
    params.setid(id).factor(factor).index(index).gics(gics).bins(bins)
    if (desc):
        params.desc()
    return params.make_args()


def rankdb_dynamic(env, data, subindices = {}):
    env.run('source("/mnt/ebs1/data/common/R/RankAnalyzer2.R")')
    env.run('source("/mnt/ebs1/data/common/R/rankdb.R")')
    v = env.get_temp_var().var
    env.set(v,'rankdb.build',data = data.name(), subindices = _R_from_dict_to_list(subindices))
    return RankAnalyzer(env = env, name = v, dynamic = True)
    
            
class RankAnalyzer(LQuant.BaseWrap):
    
    def __init__(self, env, name, dynamic = False):
        LQuant.BaseWrap.__init__(self, env, env.get_temp_var().var)
        env.run('source("/mnt/ebs1/data/common/R/RankAnalyzer2.R")')
        if dynamic:
            self.env.set(self.handle, 'RankAnalyzer$new', dbname = name)
        else:
            self.env.set(self.handle, 'RankAnalyzer$new', dbname = LQuant.LQEnv._quote(name))
    
    def __call__(self, _method, name, **kwargs):
        tvar = self.env.get_temp_var()
        self._assign(tvar.var, _method, **kwargs)
        v = self.env.get(tvar.var)
        return pd.DataFrame(v.as_double_array(), index =v.names(), columns =[name])
        
    # def __quote__(self, vals):
    #     return [LQuant.LQEnv._quote(v) for v in vals]
    # 
    # def __run__(self, method, id1, id2, name):
    #     return self.__call__(method, name, *self.__quote__([id1,id2]))
        # tvar = self.env.get_temp_var()
        # self._assign(tvar.var,method,LQuant.LQEnv._quote(id1), LQuant.LQEnv._quote(id2))
        # v = self.env.get(tvar.var)
        #return pd.DataFrame(v.as_double_array(), index =v.names(), columns =[name])
    
    def __list__(self,f1):
        tvar = self.env.get_temp_var()
        self._assign(tvar.var,f1)
        v = self.env.get(tvar.var)
        s = v.as_string_array()
        return s
        
    def export_data(self, outdir):
        self.__call__(_method = "export_data", name = ".x", outdir = _quote(outdir))
        return True
        
    def get_filtered_data(self, starting_gics, start_date, end_date, min_mktcap, exclude_gics,
                                    method = 'z_normal', factors = ['all'], meta_factors = ['all']):
        tvar = self.env.get_temp_var()
        self._assign(tvar.var,'get_filtered_data',
                    starting_gics = starting_gics, start_date = _quote(start_date),
                    end_date = _quote(end_date), min_mktcap = min_mktcap, 
                    exclude_gics = _R_to_num_list(exclude_gics), method = _quote(method), 
                    factors = _R_to_str_list(factors), meta_factors = _R_to_str_list(meta_factors))
        v = self.env.get(tvar.var)
        x = v.__as_data_frame__()
        return x
        
    def get_ranks(self, id, dated = 'last', index = None, gics = None, bins = 10, desc = False):
        kwargs = make_rank_params(id, dated, index, gics, bins, desc)
        print(kwargs)
        return self.__call__(_method = 'main_sector_rank', name = 'Rank(1-' + str(bins) + ')', **kwargs)
            
    def get_rank_history(self, id, factor, index = None, gics = None, bins = 10, desc = False):
        kwargs = make_history_rank_params(id, factor, index, gics, bins, desc)
        return self.__call__(_method = 'main_sector_rank_history', name = 'Rank(1-' + str(bins) + ')', **kwargs)
        
    
    # def get_sector_ranks(self,id,dated):
    #     return self.__run__('get_sector_ranks',id,dated,'Sector Rank(1-10)')
    #     
    # def get_index_ranks(self,id,index,dated):
    #     return self.__call__('get_index_rank', index + ' Rank(1-100)', *self.__quote__([id,index,dated]))
    #     
    # def get_index_rank_history(self,id,index,f1):
    #     return self.__call__('get_index_rank_history', index + ' Rank(1-100)', *self.__quote__([id,index,f1]))
    # 
    # def get_rank_history(self,id,factor):
    #     return self.__run__('get_rank_history',id,factor,'Rank(1-100)')
    # 
    # def get_sector_rank_history(self,id,factor):
    #     return self.__run__('get_sector_rank_history',id,factor,'Sector Rank(1-10)' )
    
    def factors(self):
        return self.__list__('factors')

    def meta_factors(self):
        return self.__list__('meta_factors')

    def dates(self):
        return self.__list__('dates')
    
    def ids(self):
        return self.__list__('ids')
        
    def subindices(self):
        return self.__list__('subindices')
    
    def master(self, dated):
        tvar = self.env.get_temp_var()
        self._assign(tvar.var,'master',LQuant.LQEnv._quote(dated))
        v = self.env.get(tvar.var)
        x = v.__as_data_frame__()
        return x
    

class DataAnalyzer(LQuant.BaseWrap):
    
    def __init__(self, env, name):
        LQuant.BaseWrap.__init__(self, env, env.get_temp_var().var)
        env.run('source("/mnt/ebs1/data/common/R/RankAnalyzer2.R")')
        self.env.set(self.handle, 'DataAnalyzer$new', dbname = LQuant.LQEnv._quote(name))
        
    def get_neut_scores(self, dated):    
        tvar = self.env.get_temp_var()
        self._assign(tvar.var,'get_neut_scores',LQuant.LQEnv._quote(dated))
        v = self.env.get(tvar.var)
        x = v.as_matrix()
        return x

    def build_backtest_data(self, name, dates, list_of_weights):    
        
        self._assign(name,'build_backtest_data',LQuant.LQEnv._quote(name),
                    _R_to_str_list(dates), _R_to_num_list_of_list(list_of_weights))
        bdata = self.env.get(name)
        bdata.ref.xdata3(self.env.kernel)
        return bdata

    def get_binary_training_set(self, dated, lookback = 24, factors = [], bins = 3, nclusters = -1):
        tvar = self.env.get_temp_var()
        if len(factors) == 0:
            factors = 'NULL'
        else: 
            factors = 'c("' + '","'.join(factors) +'")'
        self._assign(tvar.var,'get_binary_training_set',LQuant.LQEnv._quote(dated), lookback, factors, bins, nclusters)
        v = self.env.get(tvar.var)
        X = v.element('X').as_matrix()
        Y = v.element('Y').as_double_array()
        C = v.element('C')
        if not C is None:
            C = pd.DataFrame({'Factor': C.names(), 'ID' : C.as_double_array()})
        return X,Y,C
        
    def get_neut_data(self, factors):
        tvar = self.env.get_temp_var()
        n1 = self.handle + "." + tvar.var
        ff = 'c("' + '","'.join(factors) + '")'
        self._assign(n1, 'get_neut_data',ff)
        v = self.env.get(n)
        return v
