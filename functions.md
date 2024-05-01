# Functions support in LQuant

LQuant allows you to create your own factors using existing functions. This can be achived by using the wq.define method in R API and LQuant.define method in lquantPy package. 


Following are the list of functions available


# In Line Regular Functions

|Function | Description | Example |
|--------|-------------| --------|
| abs    |Computes absolute value. For NA and NaN, this returns NaN | abs(PRCCD/EPSX12) | 
| pow    |Computes power function | pow(PRCCD/EPSX12,3) | 
| nvl    |Returns the first value (PRCHD) when not NA or NaN otherwise second (PRCCD)| nvl(PRCHD,PRCCD) | 
| ifelse |Logical operator taking 3 operands, first one boolean, when the first operand is true then second operand is returned, otherwise  third| ifelse(PRCCD<5.0,5.0,PRCCD) | 
| nullif |Logical operator taking 2 operands, first one boolean, when the first operand is true then it returns NaN otherwise second operand| nullif(EPSPX12<0.0,EPSPX12) | 
| isnull |Single operand operator, return true if the operand is null | isnull(EPSPX12) |
| days_between |Returns number of days between the operands | days_between(SALEQ.DATADATE,POINTDATE) |
| min | Returns minimum of 2 operands| min(PRCCD,100.0) |
| max | Returns maximum of 2 operands| max(PRCCD,100.0) |


# Timeseries Functions

Timeseries functions are operated on a single time series or expression. The timeseries functions are invoked by having "@" in front of the function name. The first operand of the function is the timeseries object or expression and second is the window period. The timeseries functions look back over the period (second operand).  

|Function| Description | Example|
|--------|-------------|--------|
|mcount|Rolling Count of data item over the period|@mcount(PRCCD,1m)|
|msum|Rolling Sum of numeric values over the period|@msum(PRCCD,1m)|
|mhigh|Rolling High of numeric values over the period|@mhigh(PRCCD,1m)|
|mlow|Rolling Low of numeric values over the period|@mlow(PRCCD,1m)|
|mavg|Rolling Average of numeric values over the period|@mavg(PRCCD,1m)|
|mexpavg|Rolling Exponential Average of numeric values over the period|@mexpavg(PRCCD,1m)|
|mstd|Rolling Standard Deviation of numeric values over the period|@mstd(PRCCD,1m)|
|mkurt|Rolling Kurtosis of numeric values over the period|@mkurt(PRCCD,1m)|
|mskew|Rolling Skew of numeric values over the period|@mskew(RTN1D,1m)|
|mgrowth|Growth (V - lag(V) over period)/lag(V) over period|@mgrowth(SALEQ,12m)|
|mzscore|ZScore (V - avg(V))/std(V)|@mzscore(PRCCD,1m)|
|mslope|Trend Slope(b) of V ~ aT^2+bT+c|@mslope(SALEQ,5y)|
|m2slope|Trend Acceleration(b)  of V ~ aT^2+bT+c|@m2slope(SALEQ,5y)|


##Window Periods Examples
|Period | Description |
|------ | ----------- |
| 1m    | 1 month look back |
| 1w    | 1 week look back |
| 1q    | 1 quarter look back |
| 1y    | 1 year look back |
| 2m    | 2 months look back |
| 2w    | 2 weeks look back |
| 2q    | 2 quarters look back |
| 2y    | 2 years look back |
| 20d   | 20 calendar days look back |






