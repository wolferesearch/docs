Update: Starting Aug 2018, Long Format is the default format for portfolio upload


# LQuant Portfolio Upload 

LQuant Portfolio Upload module allows you to upload custom portfolio into your database space. The custom porfolio (identified by a string id), once uploaded can be used for backtesting. In addition custom portfolio can be used to add custom attributes into the database. 

Below are a few use cases for this feature

1. Portfolio Tracking
2. Portfolio Rebalance
3. Portfolio Performance Summary
4. Interest List Tracking
5. Data Upload

Portfolio upload system seamlessly ties with the backtesting library to provide several performance metrics, such as Sharpe Ratio, Draw Down and several more. 

## Identifiers

*Following Identifiers can be used to upload the portfolio:*

1. TICKER (US Only)
   Ticker can be point in time or current known ticker. By default the ticker is assumed to be Point-in-Time. 
2. SEDOL 
   Sedol is the most robust identifier. System supports both point-in-time as well as last SEDOL for mapping. For US and CA companies, the SEDOL mapping only goes back to 2002
3. CUSIP (US and Canada Only)
   Cusip is a security level identifier that can be used. In case where we have more than one security per cusip, we map the US one if available, othewise we attempt to map to Canadian. The identifier can be specified as either point-in-time or most recent. 
4. BBTICKER
   Bloomberg Ticker is good recent updates. Our history for Bloomberg ticker only starts from May 2018. 
5. QESID (This is internal 
   This is QES internal idenfier

## Format

Following keywords in the file or data frame header are looked for:

1. DATED: Indicates date of Rebalance
2. TICKER/BBTICKER/CUSIP/CUSIP8/SEDOL/SEDOL6/QESID: Indicates Identifier
3. WEIGHT 
4. ..

Any number of additional properties can be added to the portfolio. All properties will become accessible for further processing using lquant library. 

In this example, the porfolio is specified at monthly frequency. For the first month, we had MSFT, APPL and IBM, and for the second month IBM is dropped and GOOG is added. The  format allows you to add addition attributes that are uploaded as factor in the LQuant database, e.g., you can choose to add weights 

|TICKER|DATED|WEIGHT|
|------|-----|------|
|MSFT|30-Apr-2010|0.3|
|AAPL|30-Apr-2010|0.4|
|IBM|30-Apr-2010|0.3|
|MSFT|31-May-2010|0.2|
|AAPL|31-May-2010|0.5|
|GOOG|31-May-2010|0.3|

Click [here](https://raw.githubusercontent.com/wolferesearch/docs/master/sample/LongFormatPort.csv) to download a sample Long Format File. 

After uploading LQuant will make the universe constituents available to the user and also provide WEIGHT as a factor. 


# API (Python & R)

## 1. Uploading Portfolio

### A. Using a CSV File

Portfolio can be uploading using either R or python API. 


#### *RCode*
```R
myport<-wq.port.uploadFile('XXX','LongPort.csv',global=FALSE,pitId=FALSE,shortFormat=FALSE)
```

#### *Python Code*
```python
myPort = wq.port_upload_file('XXX','LongPort.csv',global=FALSE,pitId=FALSE,shortFormat=FALSE)
```


*myport* is and R6 class that provides handle to the uploaded object. You can use this handle to query properties of the porfolio. There are several methods available under this that provide access/mutation operation on the portfolio. By default, the portfolio uploaded is visible to other users within your space, however, if you want to make it private, that can be done by changing the security properties of the portfolio. Portfolio can be mutated by the user. 

*Below are the arguments used by upload File API:*

|Arg|Description|Default|
|---|----|---|
|id| Unique Id for the portfolio | None |
|file | Location of the file | None|
|global| Boolean indicator to restrict universe mapping to US, when set to false, the portfolio is assumed US/CA|TRUE|
|pitId|Boolean indicator, True indicates that provided identifiers are point in time |TRUE|
|shortFormat| Boolean indicator indicates if the file provided is short format|FALSE|



### B. Using a Data Frame
#### *RCode*
```R
df<-read.csv('LongPort.csv',stringsAsFactors=FALSE)
myport<-wq.port.upload('XXX',header=colnames(df),data=df,global=FALSE,pitId=FALSE,shortFormat=FALSE)
```

*Internally the upload File API calls the upload data*

*Below are the arguments used by upload File API:*

|Arg|Description|Default|
|---|----|---|
|id| Unique Id for the portfolio | None |
|header | Location of the file | None|
|data | Data Frame  | None|
|global| Boolean indicator to restrict universe mapping to US, when set to false, the portfolio is assumed US/CA|TRUE|
|pitId|Boolean indicator, True indicates that provided identifiers are point in time |TRUE|
|shortFormat| Boolean indicator indicates if the file provided is short format|FALSE|


### C. Using Lquant Matrix

Lquant matrices generated using prior calls to lquant code can be used to save portfolio. At minimum, the API requires 2 matrices, (1) In Flag Matrix, and (2) Weight Matrix. 

#### *RCode*
```R

# Pull a factor from lquant
req<-wq.newRequest()$runFor('SP500')$from('2004-01-03')$to('2018-07-03')$at('1m')$a('QES_LEAP_1_SCORE')$addInFlag()
req$forFactor('QES_LEAP_1_SCORE')$mask()$znormal()
s1<-basic.quantileMatrix(wq.getdata(req)[[1]],qnum=10)
weight <- backtest.quantileMatrixToWeight(s1,qnum=10,longBinIndex = 10,shortBinIndex = 1)
dimnames(weight) <- dimnames(s1)


# Upload portfolio constructed from factor
p1<-wq.port.uploadMatrix('QESTEST',list(IN=ifelse(!is.na(weight) & weight != 0, TRUE, FALSE), WEIGHT=weight),'IN')
p1$uploadAttributes()
```

*Below are the arguments used by upload Matrix API:*

|Arg|Description|Default|
|---|----|---|
|id| Unique Id for the portfolio | None |
|header | Location of the file | None|
|dataMatrics | List of data matrices containing in flag  | None|
|idxFlag| Mnemonic for the membership flag in the dataMatrices |TRUE|



## 2. Access API

### List of Portfolios

You can get the list of portfolios previously uploaded using the list API

#### *R Code*
```R
wq.port.list(currUserOnly = TRUE)
```
#### *Python Code*
```python
wq.port_list(currUserOnly = TRUE)
```


### Get Portfolio Handle

Previously saved portfolio can be pulled by using the name of the portfolio. 
#### *R Code*
```R
myPort <- wq.port.get('XXX')
```
#### *Python Code*
```python
myPort = wq.get_port('XXX')
```

Portfolio uploaded by other users can also be inspected using the handle. 



### A. Summary

Provides a succinct summary of the portfolio, i.e., Start Date, End Date, Number of Securities, Mapped Securities. The output comes back a simple data frame. Below are code snippets from R and python languages

#### *R Code*
```R
myPort$summary()
```
#### *Python Code*
```python
myPort.summary()
```
|Univ Id | Property | Value |
|--------|---------|-------|
|1|Mapping Type|US/Canada|
|1|Total Securities|5|
|1|Start Date|30-APR-10|
|1|End Date|31-MAY-10|
|1|Mapped Securities|4|


### B. Mapping

The identifiers in the portfolio file are mapped to LQuant internal identifier (QESID). In some cases, when the system is unable to map them based on the criteria. In such a scenario, the unmapped securities can be accessed

#### *R Code*
```R
myPort$unmapped()
```
#### *Python Code*
```python
myPort.unmapped()
```

|UNIV_ID|ID|IDTYPE|FIRST_DATE|LAST_DATE|
|-------|-|-------|----------|---------|
|1|XXX|3|2010-05-31T00:00:00.000Z|2010-05-31T00:00:00.000Z|

### C. Attributes

Additional columns in the uploaded file (or data frame) is exposed as lquant attributes (prefixed with universe id). List of attributes can be accessed via a simple function. Below is the code to access the list

#### *R Code*
```R
myPort$attributes()
```
#### *Python Code*
```python
myPort.attributes()
```

|Mnemonic|Expression|Function|Args|Description|Unit|Is Value|Frequency|Adjustment Type|Fx Adjustment|Staleness Threshold|
|--|--|--|--|--|--|--|--|--|--|-|
|XX1_WEIGHT|2||{\"UNIV_ID\":1041}|Custom Attribute -- WEIGHT -- created for universe XX1|WHOLE|No||None|No Adjustment|m|

### D. Owner

The owner (username) can be accessed via owner function

#### *R Code*
```R
myPort$owner()
```
#### *Python Code*
```python
myPort.owner()
```

### E. Dates

Rebalance dates can be accessed via dates function

#### *R Code*
```R
myPort$dates()
```
#### *Python Code*
```python
myPort.dates()
```

|Date|
|---|
|2010-04-30|
|2010-05-31|

### F. Constituents

__For one Date__

#### *R Code*
```R
myPort$constituents('2010-04-30')
```
#### *Python Code*
```python
myPort.constituents('2010-04-30')
```
|ID|WEIGHT|
|--|-----|
|012141.01|.2|
|160329.01|.2|
|001690.01|.5|

### G. Portfolio Data

Lquant uses list of matrices as the main data structure for analyzing. Portfolio data can be pulled from database using a simple API.  

#### *R Code*
```R
myPort$asLquantMatrix()
```
#### *Python Code*
```python
myPort.asLquantMatrix()
```


#### WEIGHT

||2010-04-30|2010-05-31|
|---|---|---|
|012141.01|0.3|0.2|
|001690.01|0.4|0.5|
|006066.01|0.3|NA|
|160329.01|NA|0.2|

There are optional arguments that can be used to restrict the data. 

|Arg| Description|Default|
|---| -----------|----|
|dates|Dates array for which data to be pulled, should align with rebalance | NULL, all dates are pulled|
|factor_ids|Array of factor names, without universe prefix | NULL, all factors are pulled |


## 3. Compute Returns

API allows easy computation of returns and turnover. 

#### *R Code*
```R
myPort$computeReturns()
```
#### *Python Code*
```python
myPort.compute_returns()
```

Returns are computed at the daily frequency, whereas turnover if applicable is computed 

#### $return
|2010-04-30|2010-05-03|2010-05-04|
|----------|----------|----------|
|0.00000000|0.0126469| -0.0220854|

#### $turnover
|2010-04-30|2010-05-31|
|--------|--------|
|0.50|0.35|


## 4. Mutation API 

*The feature is protected, this is only accessible by the owner of the portfolio. For all other users, any mutation attempt will result in error*

### A. Append to Existing Portfolio

Additional rebalance dates can be added to the portfolio using the append API. 

```R
wq.port.append('XX1',header=c('QESID','DATE','WEIGHT'),data=matrix(c('006066.01','2010-06-30',0.5,'012141.01','2010-06-30','0.5'),nrow=2,byrow = TRUE),
                pitId=TRUE)
```

|Arg|Description|Default|
|---|----|---|
|id| Unique Id for the portfolio | None |
|header | Header of the data | None|
|data| Data Frame containing the update portfolio| None |
|pitId|Boolean indicator, True indicates that provided identifiers are point in time |TRUE|


### B. Add Returns/Turnover to the Database

Computed returns can be persisted in the database by using addReturn and addTurnover call. 

#### *R Code*
```R
ret <- myPort.computeReturns()
myPort$addReturns(ret$return)
myPort$addTurnover(ret$turnover)

```

#### *Python Code*
```python
ret <- myPort.compute_returns()
myPort.add_returns(ret.return)
myPort.add_turnover(ret.turnover)

```

A few things to note about adding returns
- Returns for a date can be only added once
- If a return for a date is added again, it would result in an error


### C. Deleting Returns/Turnover


Returns in the database can be deleted using a simple Delete API

#### *R Code*
```R
# Delete return for one date
myPort$deleteReturns(date = '2010-07-30')  

# Delete all returns
myPort$deleteAllReturns
```

#### *Python Code*
```python

myPort.deleteReturns(date = '2010-07-30')  

# Delete all returns
myPort.deleteAllReturns()

```

Deleting turnover has a similar API. 

### C. Add String Parameters 

Custom string parameters can be added 

#### *R Code*
```R
myPort$setParam('Benchmark','SP500')
```

#### *Python Code*
```python
myPort.set_param('Benchmark','SP500')
```

### D. Deleting Parameters
#### *R Code*
```R
# Delete one parameter
myPort$deleteParam('Benchmark')

# Delete all parameters
myPort$deleteAllParams()
```

#### *Python Code*
```python

# Delete one parameter
myPort.delete_param('Benchmark')

# Delete all parameters
myPort.delete_all_params()
```

## 4. Accessing Retursn/Return Statistics/Parameters

### A. Accessing pre-computed returns
#### *R Code*
```R
myPort$returns()
```

#### *Python Code*
```python
myPort.returns()
```

### B. Accessing returns statistics
#### *R Code*
```R
myPort$returnStats()
```

#### *Python Code*
```python
myPort.return_stats()
```


### C. Accessing String params
```R
myPort$param('Benchmark')
```

#### *Python Code*
```python
myPort.param('Benchmark')
```
