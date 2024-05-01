from lquantPy.LQuant import BaseWrap
from lquantPy.LQuant import LQEnv

def rmutil_add_style_exposures(env, model, data, styles = None, prefix = None):
    env.run('source("/mnt/ebs1/data/common/R/risk-model-util.R")')
    if not styles:
        styles = 'NULL'
    else:
        styles = "c('" + "','".join(styles) + "')"
        
    if not prefix:
        prefix = model
    
    rmd_cmd = "{} <- rmutil.add_style_exposures({}, model = '{}', prefix = '{}', styles = {})".format(data.name(), 
        data.name(), model, prefix, styles)
    env.run(rmd_cmd)
    return None

def get_risk_model(env, model, dated):
    tempvar = env.get_temp_var()
    env.run('source("/mnt/ebs1/data/common/R/factor-awareness/risk-pkg.R")')
    rmd_cmd = "{} <- get_rmd('{}', dated = '{}')".format(tempvar.name(), model, dated)
    #print(rmd_cmd)
    env.run(rmd_cmd)
    return QESRiskModel(env, tempvar)

def get_risk_model_returns(env, model, factors, start_date, end_date):

    env.run('source("/mnt/ebs1/data/common/R/risk-model-return.R")')
    if len(factors) < 1:
        raise Exception("At least one factor should be provided")
        
    tempvar = env.get_temp_var()
    rmd_cmd = "{} <- get_risk_model_returns(model = '{}', factors = c('{}'), startDate = '{}', endDate = '{}')".format(
        tempvar.name(),model, "','".join(factors), start_date, end_date)
    #print(rmd_cmd)
    env.run(rmd_cmd)
    x = env.get(tempvar.name())
    return x.__as_data_frame__()
    
    
class RiskDecomposition(BaseWrap):
    def __init__(self, env, tempvar):
        """
        :param env: Computation (R) environment handle
        :param dlname: Base name of the object
        """
        self.tempvar = tempvar # Keep it in scope
        BaseWrap.__init__(self, env, tempvar.name())
        self.obj = env.get(tempvar.name())
    
    def get_risk_decom(self):
        return {
            'style_risk' : self.obj['portStyleRisk'].get_double(0),
            'sector_risk' : self.obj['portSectorRisk'].get_double(0),
            'idio_risk'  : self.obj['idioRisk'].get_double(0)
        }
    
    def get_summary(self):
        exp = self.obj['exposures']
        import pandas as pd
        return pd.DataFrame({
            'factor' : exp.names(),
            'exposure' : exp.as_double_array(),
            'volatility' : self.obj['factorVol'].as_double_array(),
            'risk_contribution' : self.obj['factorRisk'].as_double_array()
        })

class PortfolioRisk(BaseWrap):
    """
        Single Day Portfolio Risk Object
    """
    
    def __init__(self, env, tempvar):
        """
        :param env: Computation (R) environment handle
        :param dlname: Base name of the object
        """
        self.tempvar = tempvar # Keep it in scope
        BaseWrap.__init__(self, env, tempvar.name())
        
    def get_risk_decomposition(self):
        tempvar = self.env.get_temp_var()
        decom = self.handle + "_risk_decom"
        self._assign(tempvar.name(),'get_risk_decomposition')
        return RiskDecomposition(self.env, tempvar)
    
    
    
class QESRiskModel(BaseWrap):
    """
        Single Day Risk Model 
    """
    def __init__(self, env, tempvar):
        """
        :param env: Computation (R) environment handle
        :param dlname: Base name of the object
        """
        self.tempvar = tempvar
        BaseWrap.__init__(self, env, tempvar.name())
        
    def date(self):
        """
            Returns date of the risk model
        """
        return self._get('dated')
    
    def security_meta(self, max_rows = -1):
        """
            Returns meta data as 
            
            :param max_rows Maximum number of rows to fetch
        """
        x = self._get('get_security_meta({})'.format(max_rows))
        return x.__as_data_frame__()
    
    def factor_meta(self):
        """
            Returns factors meta data as pandas data frame
        """
        x = self._get('factorMeta')
        return x.__as_data_frame__()
        
    def sector_indices(self):
        """
            Index of sector in the meta data. Returns numeric array. 
        """
        x = self._get('ix.sector')
        return x.as_double_array()
    
    def style_indices(self):
        """
            Index of styles in the meta data. Returns numeric array.
        """
        x = self._get('ix.style')
        return x.as_double_array()
        
    def factor_covariance(self):
        """
            Returns factor covariance matrix.
        """
        x = self._get('factorCov')
        return x.as_matrix()
    
    def security_covariance_isc(self):
        """
            Returns Security (Issuer Specific) Covariance
        """
        x = self._get('securityCov')
        return x.__as_data_frame__()
    
    def model(self):
        """
            Returns the model name
        """
        return self._get('model')
    
    def exposures(self, max_rows = -1):
        """
            Gets the exposure matrix
            
            :param max_rows: maximum number of rows to fetch for preview
        """
        temp_var = self.env.get_temp_var()
        self._assign(temp_var.name(),'exposures',max_rows)
        x = self.env.get(temp_var.name())
        y = x.__as_data_frame__()
        temp_var.__del__()
        return y
    
    def get_security_exposures(self, ids):
        """
            Gets the exposure for securities
            
            :param ids: List of QES Ids
        """
        temp_var = self.env.get_temp_var()
        self._assign(temp_var.name(),'get_exposures',LQEnv._str_array(ids))
        x = self.env.get(temp_var.name())
        y = x.__as_data_frame__()
        temp_var.__del__()
        return y
    
    def get_cov_matrix(self, ids):
        """
            Builds the covariance matrix
            
            :param ids : List of QES Ids
            :weight: List of weights
        """
        temp_var = self.env.get_temp_var()
        self._assign(temp_var.name(),'get_cov_matrix',LQEnv._str_array(ids))
        x = self.env.get(temp_var.name())
        y = x.as_matrix()
        temp_var.__del__()
        return y
    
    def get_portfolio_risk(self, ids, weights):
        temp_var = self.env.get_temp_var()
        self._assign(temp_var.name(),'get_port_risk_object',LQEnv._str_array(ids), LQEnv._str_array(weights))
        return PortfolioRisk(self.env,temp_var)
        
