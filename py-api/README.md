<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="heading">

<tbody>

<tr bgcolor="#7799ee">

<td valign="bottom">   
<font color="#ffffff" face="helvetica, arial">   
<big><big>**LQuant**</big></big></font></td>

<td align="right" valign="bottom"><font color="#ffffff" face="helvetica, arial">[index](.)  
[/home/ubuntu/projects/lquantPy/lquantPy/LQuant.py](file:/home/ubuntu/projects/lquantPy/lquantPy/LQuant.py)</font></td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#aa55cc">

<td colspan="3" valign="bottom">   
<font color="#ffffff" face="helvetica, arial"><big>**Modules**</big></font></td>

</tr>

<tr>

<td bgcolor="#aa55cc"></td>

<td> </td>

<td width="100%">

<table width="100%" summary="list">

<tbody>

<tr>

<td width="25%" valign="top">[csv](csv.html)  
[logging](logging.html)  
</td>

<td width="25%" valign="top">[numpy](numpy.html)  
[os](os.html)  
</td>

<td width="25%" valign="top">[pandas](pandas.html)  
[sys](sys.html)  
</td>

<td width="25%" valign="top">[tempfile](tempfile.html)  
</td>

</tr>

</tbody>

</table>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ee77aa">

<td colspan="3" valign="bottom">   
<font color="#ffffff" face="helvetica, arial"><big>**Classes**</big></font></td>

</tr>

<tr>

<td bgcolor="#ee77aa"></td>

<td> </td>

<td width="100%">

<dl>

<dt><font face="helvetica, arial">[builtins.object](builtins.html#object)</font></dt>

<dd>

<dl>

<dt><font face="helvetica, arial">[BaseWrap](LQuant.html#BaseWrap)</font></dt>

<dd>

<dl>

<dt><font face="helvetica, arial">[LQOptPortfolio](LQuant.html#LQOptPortfolio)</font></dt>

<dt><font face="helvetica, arial">[LQOptimizer](LQuant.html#LQOptimizer)</font></dt>

<dt><font face="helvetica, arial">[LQRiskModelBuilder](LQuant.html#LQRiskModelBuilder)</font></dt>

</dl>

</dd>

<dt><font face="helvetica, arial">[LQBacktestResult](LQuant.html#LQBacktestResult)</font></dt>

<dt><font face="helvetica, arial">[LQEnv](LQuant.html#LQEnv)</font></dt>

<dt><font face="helvetica, arial">[LQExportedData](LQuant.html#LQExportedData)</font></dt>

<dt><font face="helvetica, arial">[LQGenericData](LQuant.html#LQGenericData)</font></dt>

<dt><font face="helvetica, arial">[LQMultiFactorAnalytics](LQuant.html#LQMultiFactorAnalytics)</font></dt>

<dt><font face="helvetica, arial">[LQPort](LQuant.html#LQPort)</font></dt>

<dt><font face="helvetica, arial">[LQRiskModel](LQuant.html#LQRiskModel)</font></dt>

<dt><font face="helvetica, arial">[LQuant](LQuant.html#LQuant)</font></dt>

<dt><font face="helvetica, arial">[MultiFactorBacktest](LQuant.html#MultiFactorBacktest)</font></dt>

<dt><font face="helvetica, arial">[TempVar](LQuant.html#TempVar)</font></dt>

</dl>

</dd>

</dl>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="BaseWrap">class **BaseWrap**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr>

<td bgcolor="#ffc8d8"></td>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="BaseWrap-__init__">**__init__**</a>(self, env, handle)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="BaseWrap-name">**name**</a>(self)</dt>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQBacktestResult">class **LQBacktestResult**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Class is a thin wrapper on backtest results [object](builtins.html#object) exposing all items in the list [object](builtins.html#object)  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQBacktestResult-CAGR">**CAGR**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-IC_decay">**IC_decay**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-IC_stats">**IC_stats**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-__init__">**__init__**</a>(self, analytics, res)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQBacktestResult-__repr__">**__repr__**</a>(self)</dt>

<dd><tt>Return repr(self).</tt></dd>

</dl>

<dl>

<dt><a name="LQBacktestResult-__str__">**__str__**</a>(self)</dt>

<dd><tt>Return str(self).</tt></dd>

</dl>

<dl>

<dt><a name="LQBacktestResult-basket_returns">**basket_returns**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-coverage">**coverage**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-coverage_raw">**coverage_raw**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-cum_IC_decay">**cum_IC_decay**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-cum_hit_rate">**cum_hit_rate**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-get_dates">**get_dates**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-hit_rate">**hit_rate**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-maximum_draw_down">**maximum_draw_down**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_CAGR">**plot_CAGR**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_IC">**plot_IC**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_coverage">**plot_coverage**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_coverage_raw">**plot_coverage_raw**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_seasonal_IC">**plot_seasonal_IC**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_sharpe_ratio">**plot_sharpe_ratio**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_turnover">**plot_turnover**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_wealth">**plot_wealth**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-plot_wealthLS">**plot_wealthLS**</a>(self, title)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-serial_correlation">**serial_correlation**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-sharpe_ratio">**sharpe_ratio**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-turnover">**turnover**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-volatility">**volatility**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQBacktestResult-wealth">**wealth**</a>(self)</dt>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQEnv">class **LQEnv**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Class [LQEnv](#LQEnv): Direct handle to the analytics environment (R Kernel)  
This class should only be used for diagnostic purposes. A few things that  
can be done here  
- Lists down variable in the environment  
- Save variable to a file  
- Run a custom command  
- Import values into the environment (arrays and matrices)  
- Get an [object](builtins.html#object) from the environment  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQEnv-__init__">**__init__**</a>(self, context, kernel)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-get">**get**</a>(self, name)</dt>

<dd><tt>Gets handle to an [object](builtins.html#object) in the environment  
:param name: Name of the [object](builtins.html#object)  
:return: Handle to the [object](builtins.html#object)</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-import_double_array">**import_double_array**</a>(self, name, array, names)</dt>

<dd><tt>Imports a numeric array into the environment  
:param name: Name to assign  
:param array: Array or list of double values  
:param names: Optional names for the values  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-import_double_matrix">**import_double_matrix**</a>(self, name, matrix, rownames, colnames)</dt>

<dd><tt>Imports a numeric matrix into the environment  
:param name: Name to assign  
:param matrix: Data matrix (Pandas data frame)  
:param rownames: Not used  
:param colnames: Not used  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-import_string_array">**import_string_array**</a>(self, name, array, names)</dt>

<dd><tt>Imports a string array into the environment  
:param name: Name to assign  
:param array: Array or list of strings  
:param names: Optional names for the values  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-import_string_matrix">**import_string_matrix**</a>(self, name, matrix, rownames, colnames)</dt>

<dd><tt>Imports a string matrix into the environment  
:param name: Name of the  
:param matrix: Pandas data frame containing string values  
:param rownames: Not used  
:param colnames: Not used  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-list">**list**</a>(self)</dt>

<dd><tt>List down all variables in the environment  
:return: Array containing list of variable names</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-run">**run**</a>(self, cmd)</dt>

<dd><tt>Runs a custom command  
:param cmd: String command  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQEnv-save">**save**</a>(self, v, file)</dt>

<dd><tt>Saves [object](builtins.html#object) to a file  
:param v: Name of the [object](builtins.html#object) to save  
:param file: Name of the file  
:return:</tt></dd>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQExportedData">class **LQExportedData**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr>

<td bgcolor="#ffc8d8"></td>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQExportedData-__init__">**__init__**</a>(self, dirpath)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQExportedData-asNP">**asNP**</a>(self, attrib)</dt>

</dl>

<dl>

<dt><a name="LQExportedData-attribs">**attribs**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQExportedData-dates">**dates**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQExportedData-exportAsNP">**exportAsNP**</a>(self, savedir)</dt>

</dl>

<dl>

<dt><a name="LQExportedData-load">**load**</a>(self, attrib)</dt>

</dl>

<dl>

<dt><a name="LQExportedData-loadAll">**loadAll**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQExportedData-secs">**secs**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQExportedData-values">**values**</a>(self, sec, attrib)</dt>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQGenericData">class **LQGenericData**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>An instance of this class is returned by all interfaces of [LQuant](#LQuant). The class allows  
 navigating through the data item and also opens up analytics functions  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQGenericData-__as_data_frame__">**__as_data_frame__**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-__del__">**__del__**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-__getitem__">**__getitem__**</a>(self, key)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-__init__">**__init__**</a>(self, context, ref, deleteOnExit=False)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQGenericData-__repr__">**__repr__**</a>(self)</dt>

<dd><tt>Return repr(self).</tt></dd>

</dl>

<dl>

<dt><a name="LQGenericData-__str__">**__str__**</a>(self)</dt>

<dd><tt>Return str(self).</tt></dd>

</dl>

<dl>

<dt><a name="LQGenericData-append_double_matrix">**append_double_matrix**</a>(self, name, matrix)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-append_string_matrix">**append_string_matrix**</a>(self, name, matrix)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-as_double">**as_double**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-as_double_array">**as_double_array**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-as_large_data_frame">**as_large_data_frame**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-as_matrix">**as_matrix**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-as_string">**as_string**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-as_string_array">**as_string_array**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-columns">**columns**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-data_type">**data_type**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-element">**element**</a>(self, indx)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-get_double">**get_double**</a>(self, i)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-get_string">**get_string**</a>(self, i)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-is_array">**is_array**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-is_data_frame">**is_data_frame**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-is_list">**is_list**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-is_matrix">**is_matrix**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-is_primitive">**is_primitive**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-length">**length**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-name">**name**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-names">**names**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-num_cols">**num_cols**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-num_rows">**num_rows**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-rows">**rows**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQGenericData-structure">**structure**</a>(self)</dt>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQMultiFactorAnalytics">class **LQMultiFactorAnalytics**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Wrapper Class that provides access to multi-factor analytics. Class provides access to:  
 1. Neutralization and Inversion of factors  
 2. Compute Risk Parity based factor weights  
 3. Compute Factor score using different weighting scheme  
 4. Compute Factor score for sector-by-sector factor weighting  

 The class is designed to append to existing data [object](builtins.html#object) in the R Kernel environment. API caller  
 can choose  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQMultiFactorAnalytics-__init__">**__init__**</a>(self, wq, env, data, inflag)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-backtest">**backtest**</a>(self, factors, bins, align=True)</dt>

<dd><tt>Performs simple backtest for multiple factors  
:param factors: List of factors to backtest  
:param bins: Number of bins  
:param align:  
:return: Multi-backtest [object](builtins.html#object)</tt></dd>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-basic_neutralize_factor">**basic_neutralize_factor**</a>(self, varname, factor, method, class_matrix=None)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-generate_excel">**generate_excel**</a>(self, results)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-get_ic_alpha">**get_ic_alpha**</a>(self, varname, factors, period=60)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-get_risk_parity_weights">**get_risk_parity_weights**</a>(self, varname, factors, alpha=None)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-get_risk_parity_weights_using_ic">**get_risk_parity_weights_using_ic**</a>(self, varname, factors, period=60, alpha=None)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-get_sector_risk_parity_weights">**get_sector_risk_parity_weights**</a>(self, varname, factors, class_flag='QES_GSECTOR', alpha=None)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-get_sector_risk_parity_weights_ic">**get_sector_risk_parity_weights_ic**</a>(self, varname, factors, class_flag='QES_GSECTOR', alpha=None, period=60)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-get_vol_weights">**get_vol_weights**</a>(self, varname, factors)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-invert_factors">**invert_factors**</a>(self, factors)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-mask_factors">**mask_factors**</a>(self, factors)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-merge_factor_values">**merge_factor_values**</a>(self, factor, from_value, to_value)</dt>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-multi_factor_sector_score">**multi_factor_sector_score**</a>(self, varname, factors, class_flag, weights)</dt>

<dd><tt>Computes multi-factor score using the weighting of factors by sector  
:param varname: Name of the Score to assign to the data container  
:param factors: List of factors  
:param class_flag: Name of the classification (sector) flag, e.g., QES_GSECTOR  
:param weights: Weights List. This should be a list of matrices with each element containing matrix with  
time series weights  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQMultiFactorAnalytics-multi_factor_weighting">**multi_factor_weighting**</a>(self, varname, factors, weights)</dt>

<dd><tt>Computes multi-factor score using the weighting of the factor  
:param varname: Name of the Weighting to assign to the data container  
:param factors: List of factors  
:param weights: Weight matrix  
:return:</tt></dd>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQOptPortfolio">class **LQOptPortfolio**</a>([BaseWrap](LQuant.html#BaseWrap))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Wrapper for Optimized Portfolio. Provides basic information about optimized portfolio  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">

<dl>

<dt>Method resolution order:</dt>

<dd>[LQOptPortfolio](LQuant.html#LQOptPortfolio)</dd>

<dd>[BaseWrap](LQuant.html#BaseWrap)</dd>

<dd>[builtins.object](builtins.html#object)</dd>

</dl>

* * *

Methods defined here:  

<dl>

<dt><a name="LQOptPortfolio-__init__">**__init__**</a>(self, env, handle)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQOptPortfolio-alpha">**alpha**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQOptPortfolio-status">**status**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQOptPortfolio-txn_cost">**txn_cost**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQOptPortfolio-variance">**variance**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQOptPortfolio-weights">**weights**</a>(self)</dt>

</dl>

* * *

Methods inherited from [BaseWrap](LQuant.html#BaseWrap):  

<dl>

<dt><a name="LQOptPortfolio-name">**name**</a>(self)</dt>

</dl>

* * *

Data descriptors inherited from [BaseWrap](LQuant.html#BaseWrap):  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQOptimizer">class **LQOptimizer**</a>([BaseWrap](LQuant.html#BaseWrap))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Optimizer Class. Uses Risk Model Builder, Risk Model , Date and Notional Value  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">

<dl>

<dt>Method resolution order:</dt>

<dd>[LQOptimizer](LQuant.html#LQOptimizer)</dd>

<dd>[BaseWrap](LQuant.html#BaseWrap)</dd>

<dd>[builtins.object](builtins.html#object)</dd>

</dl>

* * *

Methods defined here:  

<dl>

<dt><a name="LQOptimizer-__init__">**__init__**</a>(self, env, risk_model_builder, risk_model, date, notional_value)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQOptimizer-build_maximize_alpha_portfolio">**build_maximize_alpha_portfolio**</a>(self, alpha)</dt>

</dl>

<dl>

<dt><a name="LQOptimizer-build_minimum_risk_portfolio">**build_minimum_risk_portfolio**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQOptimizer-limit_risk_to">**limit_risk_to**</a>(self, risk_target)</dt>

</dl>

<dl>

<dt><a name="LQOptimizer-max_long_stock_weight">**max_long_stock_weight**</a>(self, max_weight)</dt>

</dl>

<dl>

<dt><a name="LQOptimizer-max_short_stock_weight">**max_short_stock_weight**</a>(self, max_weight)</dt>

</dl>

<dl>

<dt><a name="LQOptimizer-with_long_short_weights">**with_long_short_weights**</a>(self, net_weight, gross_weight)</dt>

</dl>

<dl>

<dt><a name="LQOptimizer-with_max_adv">**with_max_adv**</a>(self, max_adv)</dt>

</dl>

* * *

Methods inherited from [BaseWrap](LQuant.html#BaseWrap):  

<dl>

<dt><a name="LQOptimizer-name">**name**</a>(self)</dt>

</dl>

* * *

Data descriptors inherited from [BaseWrap](LQuant.html#BaseWrap):  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQPort">class **LQPort**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Class [LQPort](#LQPort). Provides access to user uploaded portfolio. It allows the caller to do the following  
- List down constituents  
- Look at summary  
- Look for unmapped  
- Query factors associated with Portfolio  
- Delete portfolio  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQPort-__init__">**__init__**</a>(self, port)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQPort-attributes">**attributes**</a>(self)</dt>

<dd><tt>Lists set of factors associated with the portfolio/data  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQPort-delete">**delete**</a>(self)</dt>

<dd><tt>Deletes the portfolio, should be the owner of the portfolio  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQPort-exists">**exists**</a>(self)</dt>

<dd><tt>Checks if the portfolio exists  
:return: Return True if the portfolio exists otherwise false</tt></dd>

</dl>

<dl>

<dt><a name="LQPort-id">**id**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQPort-internal_id">**internal_id**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQPort-owner">**owner**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQPort-summary">**summary**</a>(self)</dt>

<dd><tt>Returns a simple summary of the portfolio/data  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQPort-unmapped">**unmapped**</a>(self)</dt>

<dd><tt>Returns data frame with list of unmapped securities  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQPort-upload_attributes">**upload_attributes**</a>(self)</dt>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQRiskModel">class **LQRiskModel**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Risk Model Data Class.  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQRiskModel-__init__">**__init__**</a>(self, rmd)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQRiskModel-cov">**cov**</a>(self)</dt>

<dd><tt>Returns factor covariance matrix  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQRiskModel-exp">**exp**</a>(self)</dt>

<dd><tt>Returns exposures (Beta) of the stocks  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQRiskModel-idm">**idm**</a>(self)</dt>

<dd><tt>Returns identity data frame for reference  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQRiskModel-rsk">**rsk**</a>(self)</dt>

<dd><tt>Returns stock idio risk vector  
:return:</tt></dd>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQRiskModelBuilder">class **LQRiskModelBuilder**</a>([BaseWrap](LQuant.html#BaseWrap))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>Multi-period Risk Model Builder Class. Generates Risk model on the fly  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">

<dl>

<dt>Method resolution order:</dt>

<dd>[LQRiskModelBuilder](LQuant.html#LQRiskModelBuilder)</dd>

<dd>[BaseWrap](LQuant.html#BaseWrap)</dd>

<dd>[builtins.object](builtins.html#object)</dd>

</dl>

* * *

Methods defined here:  

<dl>

<dt><a name="LQRiskModelBuilder-__init__">**__init__**</a>(self, env, dlname, idxFlag)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQRiskModelBuilder-dates">**dates**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQRiskModelBuilder-get_risk_model">**get_risk_model**</a>(self, date)</dt>

</dl>

<dl>

<dt><a name="LQRiskModelBuilder-setup_data">**setup_data**</a>(self)</dt>

</dl>

* * *

Methods inherited from [BaseWrap](LQuant.html#BaseWrap):  

<dl>

<dt><a name="LQRiskModelBuilder-name">**name**</a>(self)</dt>

</dl>

* * *

Data descriptors inherited from [BaseWrap](LQuant.html#BaseWrap):  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="LQuant">class **LQuant**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr bgcolor="#ffc8d8">

<td rowspan="2"></td>

<td colspan="2"><tt>[LQuant](#LQuant) Gateway Class  
Primary purpose of this class is to interact with the [LQuant](#LQuant) application. It provides the following functionalities:  
1. Access to Factor data  
2. Access to Universe  
3. Access to R Analytical environment  
4. Access to Risk Model Generator  
5. Access to Optimization  
6. Access to Multi-factor Analytics Class  
7. Access to portfolio uploader  
8. Access to Backtester  
 </tt></td>

</tr>

<tr>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="LQuant-__init__">**__init__**</a>(self)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-__js__">**__js__**</a>(self, s)</dt>

</dl>

<dl>

<dt><a name="LQuant-basic_backtest">**basic_backtest**</a>(self, data, req)</dt>

</dl>

<dl>

<dt><a name="LQuant-define">**define**</a>(self, expression)</dt>

<dd><tt>Creates a new factor based on expression  
:param expression: Expression (e.g., AV_PRICE=@mavg(PRCCD,1m))  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-env">**env**</a>(self)</dt>

</dl>

<dl>

<dt><a name="LQuant-execute">**execute**</a>(self, req)</dt>

<dd><tt>Executes a request. The request [object](builtins.html#object) have several mandatory and optional directive.  
For a complete list of directives, refer to documentation  
:param req: Request [object](builtins.html#object) constructed using the new_request call  
:return: Instance of Java Handle to the data</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-factor_detail">**factor_detail**</a>(self, attr, source='COMPUSTAT')</dt>

<dd><tt>:param attr: Name of the factor  
:param source: Source of the factor (e.g., COMPUSTAT,CIQ)  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-factor_graph">**factor_graph**</a>(self, attr, source='COMPUSTAT')</dt>

<dd><tt>:param attr: Name of the factor (e.g., ROE)  
:return: Image png file path with the graphical representation of the execution</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-get_data">**get_data**</a>(self, req)</dt>

<dd><tt>Executes a request. The request [object](builtins.html#object) have several mandatory and optional directive.  
For a complete list of directives, refer to documentation  
:param req: Request [object](builtins.html#object) constructed using the new_request call  
:return: Instance of [LQGenericData](#LQGenericData) class that can be converted to Pandas data frame</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-get_factors">**get_factors**</a>(self)</dt>

<dd><tt>Lists down available factors  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-get_port">**get_port**</a>(self, _id)</dt>

<dd><tt>Returns handle to the portfolio  
:param _id: Id of the portfolio  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-get_user_resource">**get_user_resource**</a>(self, username, type)</dt>

<dd><tt>:param username: Username for which to run the query  
:param type: Type of query (universe,factor,meta)  
:return: Data frame containing the resource information</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-load_csv_data">**load_csv_data**</a>(self, filename, varname, idCol, dateCol)</dt>

</dl>

<dl>

<dt><a name="LQuant-multi_factor_analysis">**multi_factor_analysis**</a>(self, data, inflag)</dt>

<dd><tt>    Provides handle to analytics class that allows multi factor analysis  
:param data: Data [object](builtins.html#object) fetched previously using get_data call  
:param inflag: String in flag (e.g., IN_SP500)  
:return: Handle to the Analytics class</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-new_request">**new_request**</a>(self)</dt>

<dd><tt>Builds an empty request [object](builtins.html#object). The [object](builtins.html#object) exposes a fluent API to add parameters to request  
:return: Data Query Request Object  
    from(yyyy-mm-dd) start date  
    to(yyyy-mm-dd) end date  
    runFor(universeId) universe specification  
    at(frequency) frequency specification  
    a(attribute) attribute. This method can be called multiple times for multiple attributes  
    forDates(dates array yyyy-mm-dd) List of dates. Should not be combined with from/to/at directives</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-new_risk_model_builder">**new_risk_model_builder**</a>(self, data, idxFlagName)</dt>

<dd><tt>Provides instance of a new risk model builder  
:param data: Data [object](builtins.html#object) returned from get_data call  
:param idxFlagName:  Name of the index flag  
:return: Handle to Risk Model Builder</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-optimizer">**optimizer**</a>(self, risk_model_builder, risk_model, date, notional_value)</dt>

<dd><tt>Provides instance of a new optimization runner  
:param risk_model_builder: Handle to risk model builder  
:param risk_model: Handle to risk model data  
:param date: Date of optimization  
:param notional_value: Notional value of the portfolio to optimize  
:return:</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-plan_tree">**plan_tree**</a>(self, attr, source='COMPUSTAT')</dt>

<dd><tt>Return the complete execution tree detail for the factor  
:param attr: Name of the factor (e.g., ROE)  
:param source: Source of the factor (e.g., COMPUSTAT, CIQ)  
:return: String with details of execution</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-port_list">**port_list**</a>(self, username, current_user_only=False)</dt>

</dl>

<dl>

<dt><a name="LQuant-port_list_by_user">**port_list_by_user**</a>(self, user, current_user_only=True)</dt>

</dl>

<dl>

<dt><a name="LQuant-port_upload">**port_upload**</a>(self, _id, header, data, _global=False, pit_id=False, short_format=False, user=None)</dt>

<dd><tt>Uploads data matrix into lquant  
:param id: Unique identifier  
:param header: columns of the data  
:param data: data frame containing data  
:param _global: Boolean flag to indicate if this is Global  
:param pit_id: Boolean flag to indicate if the id is point-in-time  
:param short_format: Boolean flag to indicate if the data is in short format (From-To)  
:return: Handle to portfolio</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-port_upload_data">**port_upload_data**</a>(self, _id, header, data, _global=False, pit_id=False, short_format=False, user=None)</dt>

</dl>

<dl>

<dt><a name="LQuant-port_upload_data_file">**port_upload_data_file**</a>(self, _id, filename, _global=False, pit_id=False, short_format=False, user=None)</dt>

<dd><tt>Uploads raw data into Lquant  
:param _id: Unique identifier for the portfolio  
:param filename: Full path of the file containing constituents  
:param _global: Boolean flag indicating if this to be mapped to US/Canada or Global securities  
:param pit_id:  Boolean flag to indicate if the Identifier Point in TIme (Default is False)  
:param short_format: Boolean flag to indicate if the format of the file is long/short format, see documentation  
                    for details  
:param user: Name of the user for which to upload  
:return: Returns a portfolio handle</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-port_upload_file">**port_upload_file**</a>(self, _id, filename, _global=False, pit_id=False, short_format=False, user=None)</dt>

<dd><tt>Uploads portfolio and corresponding data into Lquant  
:param _id: Unique identifier for the portfolio  
:param filename: Full path of the file containing constituents  
:param _global: Boolean flag indicating if this to be mapped to US/Canada or Global securities  
:param pit_id:  Boolean flag to indicate if the Identifier Point in TIme (Default is False)  
:param short_format: Boolean flag to indicate if the format of the file is long/short format, see documentation  
                    for details  
:return: Returns a portfolio handle</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-quantdb_query">**quantdb_query**</a>(self, name, query)</dt>

</dl>

<dl>

<dt><a name="LQuant-quantdb_user_query">**quantdb_user_query**</a>(self, username, name, query)</dt>

</dl>

<dl>

<dt><a name="LQuant-search">**search**</a>(self, type, query)</dt>

<dd><tt>:param type: Type of entity (UNIVERSE, ATTRIBUTE, SECURITY)  
:param query: Free format search query  
:return: List of entities matching the</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-search_attribute">**search_attribute**</a>(self, query)</dt>

<dd><tt>Searches factors (attributes) based on the string query  
:param query: String query (e.g., Earnings)  
:return: Data frame with hits</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-search_security">**search_security**</a>(self, query)</dt>

<dd><tt>Searches securities based on the string query  
:param query: String query (e.g., Apple)  
:return: Data frame with hits</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-search_universe">**search_universe**</a>(self, query)</dt>

<dd><tt>Searches universe based on the string query  
:param query: String query (e.g., Korea)  
:return: Data frame with hits</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-valuation_spread">**valuation_spread**</a>(self, data, req)</dt>

</dl>

* * *

Static methods defined here:  

<dl>

<dt><a name="LQuant-new_backtest_request">**new_backtest_request**</a>()</dt>

<dd><tt>Creates a new backtest request  
:return: Handle to backtest request</tt></dd>

</dl>

<dl>

<dt><a name="LQuant-new_valspread_request">**new_valspread_request**</a>()</dt>

<dd><tt>Creates a new Valuation Spread Request  
:return: Handle to valuation spread request</tt></dd>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="MultiFactorBacktest">class **MultiFactorBacktest**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr>

<td bgcolor="#ffc8d8"></td>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="MultiFactorBacktest-__init__">**__init__**</a>(self, env, backtest_results, factors)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="MultiFactorBacktest-factor_name">**factor_name**</a>(self, i)</dt>

</dl>

<dl>

<dt><a name="MultiFactorBacktest-generate_excel">**generate_excel**</a>(self, univName, baskets)</dt>

</dl>

<dl>

<dt><a name="MultiFactorBacktest-generate_pdf">**generate_pdf**</a>(self, filename, title, i)</dt>

</dl>

<dl>

<dt><a name="MultiFactorBacktest-get">**get**</a>(self, i)</dt>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

<table width="100%" cellspacing="0" cellpadding="2" border="0" summary="section">

<tbody>

<tr bgcolor="#ffc8d8">

<td colspan="3" valign="bottom">   
<font color="#000000" face="helvetica, arial"><a name="TempVar">class **TempVar**</a>([builtins.object](builtins.html#object))</font></td>

</tr>

<tr>

<td bgcolor="#ffc8d8"></td>

<td> </td>

<td width="100%">Methods defined here:  

<dl>

<dt><a name="TempVar-__del__">**__del__**</a>(self)</dt>

</dl>

<dl>

<dt><a name="TempVar-__init__">**__init__**</a>(self, env)</dt>

<dd><tt>Initialize self.  See help(type(self)) for accurate signature.</tt></dd>

</dl>

<dl>

<dt><a name="TempVar-name">**name**</a>(self)</dt>

</dl>

* * *

Data descriptors defined here:  

<dl>

<dt>**__dict__**</dt>

<dd><tt>dictionary for instance variables (if defined)</tt></dd>

</dl>

<dl>

<dt>**__weakref__**</dt>

<dd><tt>list of weak references to the object (if defined)</tt></dd>

</dl>

</td>

</tr>

</tbody>

</table>

</td>

</tr>

</tbody>

</table>
