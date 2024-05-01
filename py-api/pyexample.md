# Python API for LQuant data Query Engine


## Handle to the Data Query Engine
```python
from lquantPy import LQuant
lq=LQuant.LQuant()
```


## Setting the Data Query Parameters

### Set Universe
```python
univ='SP500'     # S&P 500
univ='US_1'      # Union of S&P 1500 and Russell 3000
univ='i:006066.01' # Single Stock 
```
### Frequency
```python
freq = '1d'   # Daily (Including Holidays)
freq = '1q'   # Quarterly
freq = '1me'  # Month End
freq = '1m'
```


### Start and End Date
```python
startDate = '1995-12-31'
endDate = '2017-02-28'
``` 

### Build the Request object
```python
req=lq.newRequest().start(startDate).to(endDate).runFor(univ).at(freq).a('PRCCD')
```

### Execute the data query request
```python
response=lq.execute(req)
```

### Check for error and print message
```python
if response.status().toString() == 'ERROR':
    print(response.message())
    sys.exit(-1)
```

### Check the type of response object
```python
type(response)
```

This should return a handle to java class  jnius.reflect.MetaJavaClass


### Print securities
```python
print(response.secs())
```

###Print Dates
```python
print(response.dates())
```

###Print all attributes
```python
print(response.attribs())
```


### Get raw array values
```python
response.values('006066.01','PRCCD')
```

