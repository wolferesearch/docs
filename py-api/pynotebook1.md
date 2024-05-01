
# Python API


This examples illustrates the working of Python interface to LQuant&reg; data query library created by [Wolfe Research](https://www.wolferesearch.com). The API paralles the R API. 

## Architecture

![Quant Architecture](https://s3.amazonaws.com/lquant-images/QuantDataPipeline.png "Quant Architecture")






`lquantPy` is a python package available on servers hosted by Wolfe Research. The package provides access to the data query API. For Python, we use [`numpy`](http://www.numpy.org/) and [`pandas`](http://pandas.pydata.org/) as the data container. Here is an exampel of the API, attempting to retrieve Company Name (COMPANYNAME), Return on Equity (ROE), Close Price (PRCCD), and Cumulative Dividend Cash Flow (CUM_DIV) for S&P 500 (SP500) from Dec, 1995 to Mar, 2017. 

### Data Query API


```python


# LQuant is 
from lquantPy import LQuant
wq=LQuant.LQuant()

freq = '1me'
univ = 'SP500'

startDate = '1995-12-31'
endDate = '2017-03-31'

req = wq.newRequest().testMode().start(startDate).to(endDate).\
    runFor(univ).at(freq).a('COMPANYNAME').a('ROE').a('MA_15_36').a('PRCCD').a('CUM_DIV')
    
data = wq.getData(req)    

```

    2017-06-19 21:54:00,283 - lquantPy.LQuant - INFO - Initial LQuant. This may take some time...
    2017-06-19 21:54:00,283 - lquantPy.LQuant - INFO - Initial LQuant. This may take some time...
    2017-06-19 21:54:00,286 - lquantPy.LQuant - INFO - Initialized LQuant environment
    2017-06-19 21:54:00,286 - lquantPy.LQuant - INFO - Initialized LQuant environment
    2017-06-19 21:54:00,289 - lquantPy.LQuant - INFO - Fetching Data
    2017-06-19 21:54:00,289 - lquantPy.LQuant - INFO - Fetching Data
    2017-06-19 21:54:02,223 - lquantPy.LQuant - DEBUG - [WQUANT] Dates: 256
    2017-06-19 21:54:02,223 - lquantPy.LQuant - DEBUG - [WQUANT] Dates: 256
    2017-06-19 21:54:02,226 - lquantPy.LQuant - DEBUG - [WQUANT] Securities: 1064
    2017-06-19 21:54:02,226 - lquantPy.LQuant - DEBUG - [WQUANT] Securities: 1064
    2017-06-19 21:54:02,713 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,713 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,736 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,736 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,756 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,756 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,776 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,776 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,795 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]
    2017-06-19 21:54:02,795 - lquantPy.LQuant - DEBUG - Size of DataFrame:[ 1064 x 256]


The returned object `data` is the dictionary object, with keys as the name of the factor and values as pandas data frame. Each value in the dictionary is of the same dimension. In this example, the data frame that can be deferenced using the square bracket dictionary operator with the name (i.e., ROE) as the operand, has 1064 rows and 256 columns. There is one row per security and one column per date of the analysis. Since we have monthly data specified as the frequency, we have 256 months from Dec 95 to Mar 07. 

Below code illustrates the extracting ROE from the dictionary and prints out the head. You can utilize `roe.index` and `row.columns` to print out the row names and columns names of the pandas data frame.



```python
roe=data['ROE']
roe.head()

```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>1995-12-31</th>
      <th>1996-01-31</th>
      <th>1996-02-29</th>
      <th>1996-03-31</th>
      <th>1996-04-30</th>
      <th>1996-05-31</th>
      <th>1996-06-30</th>
      <th>1996-07-31</th>
      <th>1996-08-31</th>
      <th>1996-09-30</th>
      <th>...</th>
      <th>2016-06-30</th>
      <th>2016-07-31</th>
      <th>2016-08-31</th>
      <th>2016-09-30</th>
      <th>2016-10-31</th>
      <th>2016-11-30</th>
      <th>2016-12-31</th>
      <th>2017-01-31</th>
      <th>2017-02-28</th>
      <th>2017-03-31</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>001013.01</th>
      <td>18.802900</td>
      <td>14.958718</td>
      <td>15.737780</td>
      <td>15.737780</td>
      <td>15.737780</td>
      <td>15.737780</td>
      <td>17.567588</td>
      <td>17.567588</td>
      <td>17.567588</td>
      <td>17.567588</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>001045.01</th>
      <td>8.550000</td>
      <td>8.550000</td>
      <td>8.550000</td>
      <td>4.670559</td>
      <td>4.670559</td>
      <td>8.873239</td>
      <td>8.873239</td>
      <td>8.873239</td>
      <td>11.370780</td>
      <td>11.370780</td>
      <td>...</td>
      <td>192.737722</td>
      <td>177.254482</td>
      <td>177.254482</td>
      <td>177.254482</td>
      <td>142.627076</td>
      <td>142.627076</td>
      <td>142.627076</td>
      <td>65.644548</td>
      <td>65.644548</td>
      <td>65.644548</td>
    </tr>
    <tr>
      <th>001045.04</th>
      <td>8.550000</td>
      <td>8.550000</td>
      <td>8.550000</td>
      <td>4.670559</td>
      <td>4.670559</td>
      <td>8.873239</td>
      <td>8.873239</td>
      <td>8.873239</td>
      <td>11.370780</td>
      <td>11.370780</td>
      <td>...</td>
      <td>192.737722</td>
      <td>177.254482</td>
      <td>177.254482</td>
      <td>177.254482</td>
      <td>142.627076</td>
      <td>142.627076</td>
      <td>142.627076</td>
      <td>65.644548</td>
      <td>65.644548</td>
      <td>65.644548</td>
    </tr>
    <tr>
      <th>001075.01</th>
      <td>11.566896</td>
      <td>10.372870</td>
      <td>10.372870</td>
      <td>10.372870</td>
      <td>10.901949</td>
      <td>10.901949</td>
      <td>10.901949</td>
      <td>11.819788</td>
      <td>11.819788</td>
      <td>11.819788</td>
      <td>...</td>
      <td>9.628969</td>
      <td>9.628969</td>
      <td>9.543613</td>
      <td>9.543613</td>
      <td>9.543613</td>
      <td>9.721892</td>
      <td>9.721892</td>
      <td>9.721892</td>
      <td>9.434848</td>
      <td>9.434848</td>
    </tr>
    <tr>
      <th>001078.01</th>
      <td>40.642266</td>
      <td>41.014787</td>
      <td>41.014787</td>
      <td>41.014787</td>
      <td>41.475378</td>
      <td>41.475378</td>
      <td>41.475378</td>
      <td>41.352871</td>
      <td>41.352871</td>
      <td>41.352871</td>
      <td>...</td>
      <td>10.008146</td>
      <td>9.143124</td>
      <td>9.161802</td>
      <td>9.161802</td>
      <td>4.580952</td>
      <td>4.603720</td>
      <td>4.603720</td>
      <td>5.109818</td>
      <td>5.143061</td>
      <td>5.143061</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 256 columns</p>
</div>



### Search API

`lquantPy` has a search API to search through Universes, Attributes and Securities. They can be accessed via `searchUniverse`, `searchAttribute` and `searchSecurity` methods available in LQuant class. In the code below, we are looking for Portugal universe. 


```python
# Search for universes
# LQuant utilizes 
wq.searchUniverse('Portugal').head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>vendorId</th>
      <th>vendorIdDataType</th>
      <th>name</th>
      <th>description</th>
      <th>inceptionDate</th>
      <th>region</th>
      <th>source</th>
      <th>args</th>
      <th>importance</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>TQA_SPCBMICPTUSD</td>
      <td>175</td>
      <td>NUMERIC</td>
      <td>TQA BMI S&amp;P Portugal BMI (US Dollar)</td>
      <td>S&amp;P Portugal BMI (US Dollar)</td>
      <td>1980-01-01</td>
      <td>GLOBAL</td>
      <td>tqaBmiUniv</td>
      <td></td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>TQAMSCI_962000</td>
      <td>962000</td>
      <td>NUMERIC</td>
      <td>TQA MSCI PORTUGAL</td>
      <td>PORTUGAL</td>
      <td>1980-01-01</td>
      <td>GLOBAL</td>
      <td>msciIdx</td>
      <td></td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BMI_84316440</td>
      <td>84316440</td>
      <td>NUMERIC</td>
      <td>CAPIQ BMI S&amp;P Portugal BMI Index</td>
      <td>S&amp;P Portugal BMI Index</td>
      <td>2004-12-31</td>
      <td>GLOBAL</td>
      <td>ciqBmiUniv</td>
      <td></td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>TQA_SPCBMIVCPTUSD</td>
      <td>1249</td>
      <td>NUMERIC</td>
      <td>TQA BMI S&amp;P Portugal BMI Value (US Dollar)</td>
      <td>S&amp;P Portugal BMI Value (US Dollar)</td>
      <td>1980-01-01</td>
      <td>GLOBAL</td>
      <td>tqaBmiUniv</td>
      <td></td>
      <td>2</td>
    </tr>
    <tr>
      <th>4</th>
      <td>TQA_SPCBMIGCPTUSD</td>
      <td>967</td>
      <td>NUMERIC</td>
      <td>TQA BMI S&amp;P Portugal BMI Growth (US Dollar)</td>
      <td>S&amp;P Portugal BMI Growth (US Dollar)</td>
      <td>1980-01-01</td>
      <td>GLOBAL</td>
      <td>tqaBmiUniv</td>
      <td></td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>




```python
wq.searchSecurity('Apple').head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>ticker</th>
      <th>exchange</th>
      <th>name</th>
      <th>currency</th>
      <th>status</th>
      <th>descr</th>
      <th>source</th>
      <th>primflag</th>
      <th>sedol</th>
      <th>importance</th>
      <th>isoCurrency</th>
      <th>country</th>
      <th>region</th>
      <th>isoCountry</th>
      <th>cusip</th>
      <th>isin</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>001690.01</td>
      <td>AAPL</td>
      <td>NASDAQ</td>
      <td>Apple Inc-COM NPV</td>
      <td>US Dollar</td>
      <td>A</td>
      <td>Apple Inc. designs, manufactures, and markets ...</td>
      <td>NA</td>
      <td>Y</td>
      <td>2046251</td>
      <td>1</td>
      <td>USD</td>
      <td>United States</td>
      <td>United States and Canada</td>
      <td>US</td>
      <td>037833100</td>
      <td>US0378331005</td>
    </tr>
    <tr>
      <th>1</th>
      <td>304348005</td>
      <td></td>
      <td>SIX Swiss Exchange</td>
      <td>Apple Inc.- Common Stock</td>
      <td>Euro</td>
      <td>A</td>
      <td></td>
      <td>GLOBAL</td>
      <td>Y</td>
      <td></td>
      <td>2</td>
      <td>EUR</td>
      <td>Switzerland</td>
      <td>Europe</td>
      <td>CH</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>2</th>
      <td>2590360</td>
      <td>AAPL</td>
      <td>Nasdaq Global Select</td>
      <td>Apple Inc.-Common Stock</td>
      <td>US Dollar</td>
      <td>A</td>
      <td></td>
      <td>GLOBAL</td>
      <td>Y</td>
      <td>2046251</td>
      <td>2</td>
      <td>USD</td>
      <td>United States</td>
      <td>United States and Canada</td>
      <td>US</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>308716962</td>
      <td>AAPL</td>
      <td>Bolsa de Valores de Lima</td>
      <td>Apple Inc.-Common Stock</td>
      <td>US Dollar</td>
      <td>A</td>
      <td></td>
      <td>GLOBAL</td>
      <td>N</td>
      <td>BYS3934</td>
      <td>3</td>
      <td>USD</td>
      <td>Peru</td>
      <td>Latin America and Caribbean</td>
      <td>PE</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>260339402</td>
      <td>AAPL</td>
      <td>Wiener Boerse AG</td>
      <td>Apple Inc.-Common Stock</td>
      <td>Euro</td>
      <td>A</td>
      <td></td>
      <td>GLOBAL</td>
      <td>N</td>
      <td>BF1SS69</td>
      <td>3</td>
      <td>EUR</td>
      <td>Austria</td>
      <td>Europe</td>
      <td>AT</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>




```python
wq.searchAttribute('Price Close - Daily').head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Mnemonic</th>
      <th>Expression</th>
      <th>Function</th>
      <th>Args</th>
      <th>Description</th>
      <th>Unit</th>
      <th>Is Value</th>
      <th>Frequency</th>
      <th>Adjustment Type</th>
      <th>Fx Adjustment</th>
      <th>Staleness Threshold</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>CIQ_INDEX_PRICE_CLOSE</td>
      <td>112113</td>
      <td></td>
      <td>{"INDEXPROVIDERID":339}</td>
      <td>Local Price From Close File</td>
      <td>PER_SHARE</td>
      <td>Yes</td>
      <td>DAILY</td>
      <td>Per Share(V/Adjustment Factor)</td>
      <td>Values are adjusted at the spot fx rate of dat...</td>
      <td>21d</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CIQ_INDEX_MKTCAP_CLOSE</td>
      <td>112115</td>
      <td></td>
      <td>{"INDEXPROVIDERID":339}</td>
      <td>Market Cap From Close File</td>
      <td>WHOLE</td>
      <td>Yes</td>
      <td>DAILY</td>
      <td>None</td>
      <td>Values are adjusted at the spot fx rate of dat...</td>
      <td>21d</td>
    </tr>
    <tr>
      <th>2</th>
      <td>CIQ_INDEX_SHARES_CLOSE</td>
      <td>112114</td>
      <td></td>
      <td>{"INDEXPROVIDERID":339}</td>
      <td>Shares Outstanding From Close File</td>
      <td>SHARES</td>
      <td>Yes</td>
      <td>DAILY</td>
      <td>Shares (V*Adjustment Factor)</td>
      <td>Values are adjusted at the spot fx rate of dat...</td>
      <td>21d</td>
    </tr>
    <tr>
      <th>3</th>
      <td>DS2_SECLOW</td>
      <td>LOW</td>
      <td></td>
      <td></td>
      <td>Secondary listing price</td>
      <td>PER_SHARE</td>
      <td>Yes</td>
      <td>DAILY</td>
      <td>Per Share(V/Adjustment Factor)</td>
      <td>Values are adjusted at the spot fx rate of dat...</td>
      <td>20y</td>
    </tr>
    <tr>
      <th>4</th>
      <td>DS2_SECOPEN</td>
      <td>OPEN_</td>
      <td></td>
      <td></td>
      <td>Secondary listing price</td>
      <td>PER_SHARE</td>
      <td>Yes</td>
      <td>DAILY</td>
      <td>Per Share(V/Adjustment Factor)</td>
      <td>Values are adjusted at the spot fx rate of dat...</td>
      <td>20y</td>
    </tr>
  </tbody>
</table>
</div>



### Defining New Factors

You can dynamically create new factors using existing. Simple mathematical expression can be constructed. The expression support simple mathematical functions (e.g., abs, exp, pow, log) and operators (e.g., *,/,+,-). There are also timeseries functions that can be created. For more information on the timeseries function, please see the [documentation](https://github.com/wolferesearch/docs/blob/master/functions.md)


```python
# Define a new Factor

wq.define('CloseToHigh=PRCCD/PRCHD')
wq.factorDetail('CloseToHigh','COMPUSTAT')
```


<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Key</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Mnemonic</td>
      <td>CloseToHigh</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Expression</td>
      <td>PRCCD/PRCHD</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Function</td>
      <td></td>
    </tr>
    <tr>
      <th>3</th>
      <td>Args</td>
      <td></td>
    </tr>
    <tr>
      <th>4</th>
      <td>Description</td>
      <td>PRCCD/PRCHD</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Unit</td>
      <td>WHOLE</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Is Value</td>
      <td>No</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Frequency</td>
      <td></td>
    </tr>
    <tr>
      <th>8</th>
      <td>Adjustment Type</td>
      <td>None</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Fx Adjustment</td>
      <td>No Adjustment</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Staleness Threshold</td>
      <td></td>
    </tr>
  </tbody>
</table>
</div>



