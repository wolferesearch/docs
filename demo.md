

![Wolfe Research Image](https://s3.amazonaws.com/lquant-images/wolfe_luo.jpg)
# Wolfe Research Quant Data API (R)


Luo's Quant Data and Analytics API provides a comprehensive research platform. The platform is designed by a sell-side Quant team that has been top ranked  in Institutional Investors survey for 7 years in a row. The platform is built on top of following core components:

* Relational Database
* Security Mapping
* Custom in-memory time series database
* Java library to orchestrate the join
* R/Python API as the User Interface
* Modeling/Backtesting functions





## Getting Started

Full Script is available [here](https://github.com/wolferesearch/docs/blob/master/code/demo/demo.R)

### Source the libraries (wquantR and lqtool)

There two core R packages provided that offers a rich set of functions to retrieve and analyze data. The first step is to source these libraries in the R Session.

Documentation for these packages can be found within your RStudio install. You can find direct link to the document here 

* [Data Query Engine](<https://github.com/wolferesearch/docs/blob/master/r-api/wquantR.pdf>)
* [Analytics Library](https://github.com/wolferesearch/docs/blob/master/r-api/lqtool.pdf)

```R
library(wquantR)
library(lqtool)
```



### Define Parameters

Although the API offers a way to pass these functions with each call. It is recommended that you define these parameters as global variable. This way the getdata function would return consistent data using the global parameters. 

```R
startDate<-'1994-12-31'
endDate<-'2017-03-31'
universeName<-'SP500'  
freq<-'1me'
```

### Source Commmon Utility Functions
```R
source('/mnt/ebs1/data/util/util.R')
```

A simple function can be created to reduce the verbosity of code downstream. This function utilizes globally defined parameters. It only takes set of factors as argument. 

```R
getData<-function(factors){
  wq.getdata(wq.newRequest()$runFor(universeName)$from(startDate)$to(endDate)$at(freq)$attr(.jarray(factors)))
}

```

###  Download Factors Data and Visualize

Provide a list of factor mnemonics to download. This is the workhorse method and does most of the heavy lifting. 

```R
data<-getData(c('PRCCD','CUM_DIV','RTN_12M1M','ROE','MKTCAP','IN_SP500','GSUBIND'))
```

*Note that getData function is small wrapper that utilizes the global variables to run the data request* 

This returns us factor data as a list of data matrices *I* (Items) X *S* (Securities) X *T* (Dates)


On successful execution of the get data call, you can print out the names of  
```R
names(data)
```

### Visualize data using custom functions
```R
plot.backtest.distribution(data$RTN_12M1M, "Momentum",title='Momentum',baskets = 5)
plot.backtest.density(data$RTN_12M1M, "Momentum",title='Momentum Density')
```
The above functions utilizes ggplot.


### Universe Flag

Universe flag IN_SP500 returns a simple TRUE and FALSE matrix based on whether a given security is present or not in the universe at a given point in time. 
```R
idx<-data[[paste('IN_SP500',sep='')]]>0
idx[is.na(idx)]<-FALSE
```

Flag should be used to take out securities in the data matrices that are not present in the universe. Note that this does not change the dimensions of the matrices. 

In this example, we are making all matrix data points NA when the security is not in the universe. This is done for all downloaded factors

```R
data<-lapply(data,function(x){ x[!idx]<-NA; return(x)})
```

### Forward Returns

Returns can be computed using the adjusted prices (PRCCD) and Adjusted Cumulative Cash flow series. 

```R
RTN<-(data[['PRCCD']]+data[['CUM_DIV']]-wLag(data[['CUM_DIV']]))/wLag(data[['PRCCD']])-1
```

*Note that this is different from total returns that uses the immediate reinvestment of dividend back into the stock*


The computed factor RTN is backward looking. In order to get a forward looking return, we can utilize wLag function. 

```R
FMRTN1M<-wLag(RTN,-1)
FMRTN1M[!idx]<-NA
```
*Note that the code in previous block is merely a shift operation on matrix. Each column in the matrix is shifted to left.* 

Most of our analytics function require data to be aligned. It is for this reason, the return is shifted, so that we use factors to predict future return.

### Beta
There is a convenient method exposed to compute beta.

Beta can be computed by just providing the returns matrix. The beta is computed using the universe flag (idx). It constructs a equi-weighted index of securities. The function has other parameters that can be used to customize the beta calculation. The returned matrix is of the same size as all other factors 

```R
BETA<-basic.calculateBeta(RTN,idx)
```


### Idiosynchratic Volatility

```R
idioVolDaily = basic.idioVol(universeName,startDate,endDate)
```

Idiosynchratic volatility computation is memory and computational intensive. It provides volatility at daily frequency, you can project it to desired dates by getting the date/security projection projection vector. 

```
cname<-colnames(idioVolDaily)
idioVol<-idioVolDaily[rownames(idx),sapply(colnames(idx), function(d) min(which(d<=cname)))]
```



---
## Custom Factors 

Using existing factor mnemonic, higher level factor can be created using mathematical expressions involving existing mnemonic. System internally translates the mnemonics in the expression on each date and evaulates the derived factor.  
  
**Define a custom Earnings Yield**

In this example, we are defining a custom earning yield that weights backward yield and forward yield equally. 

```R
wq.define('EarningsYield=0.5*EPSF12/PRCCD+0.50*CIQ_EST_EPS_MED_FY1/PRCCD')
```


Get data from the query engine for the custom factor

```R
data_cust <- getData('EarningsYield')
```

*Visualize Earnings Yield*
```R
plot.backtest.density3D(data_cust$EarningsYield, "Earnings Yield (%)",title='Earnings Yield Density')
```

---

## Sectors & Custom Universes  

Sector mask is basically a boolean matrix that indicates if a security is present or not at the time 

```R
sector_mask <- getSectorMask(c('Energy','Utilities'),data)
```

The *sector_mask* matrix can be used to "mask" the data matrices. In this example, the previously computed earningsYield can be masked to have values only for securities in Energy and Utility industries. This is basic R data manipulation 

```R
sectorData<-data_cust$EarningsYield
sectorData[!sector_mask]<-NA
mask <- rowSums(sector_mask) > 0
```

You can see the coverage of the stocks in the 2 sectors.

```R
colSums(!is.na(sectorData),na.rm=T)
```

Here is the plot of sector filtered values
```R
plot.backtest.distribution(sectorData, "Earnings Yield (%)",title='Earnings Yield',baskets = 5)
```
*Notice the drop in First Quarter of 2016 when Oil prices crashed*


---

## Factor Normalization and Neutralization  

We have packaged normalization and neutralization in a single function. Here is a sample code that converts the Market Cap (previously downloaded) to it z score

```R
plot.backtest.distribution(data$MKTCAP, "Market Cap",title='Market Cap',baskets = 5)
norm_MKTCAP <- basic.neutralizeFactor(data$MKTCAP, method = 'z_score')
plot.backtest.distribution(norm_MKTCAP, "Market Cap (Normalized) ",title='Market Cap',baskets = 5)
```

This creates a new matrix norm_MKTCAP that is normalized and is 100% correlated with MKTCAP.  

```R
mean(norm_MKTCAP[,'2015-01-31'], na.rm = T)
var(norm_MKTCAP[,'2015-01-31'], na.rm = T)
```

Normalization can also be done by subsetting the universe. Here, we are adding the sector mask a matrix to subset the data. Hence data would be partitioned into two sets:
  1. Securities that in Energy and Utility industries, 
  2. Securities that are not. You can also utilize actual 2 digit sector codes to partition data into individual sectors. The normalization is done within each subset. 
  
  
  
  
```R
norm_MKTCAP_by_sectors <- basic.neutralizeFactor(data$MKTCAP, method = 'z_score', classMatrix = sector_mask)
```

Check if normalized for Energy and Utilities sectors. Here we are only looking at the mean and variance on one date. 

```R
mean(norm_MKTCAP_by_sectors[, 200], na.rm = T)
var(norm_MKTCAP_by_sectors[, 200], na.rm = T)
mean(norm_MKTCAP_by_sectors[, 200][sector_mask[,200]], na.rm = T)
var(norm_MKTCAP_by_sectors[, 200][sector_mask[,200]], na.rm = T)
```

---

## Neutralization using Regression 

In this example, we take the earnings yield and perform a regression on beta and  


**(Momentum ~ Market Cap, Beta)**

```R
regressFactors<-basic.regressFactors(data[['RTN_12M1M']],list(BETA=BETA,MKTCAP=norm_MKTCAP))
momentum_neutralized<-regressFactors[["residual"]]
coeff<-regressFactors[["coeff"]]
tstats<-regressFactors[["tstats"]]
```

Regress Factor is custom function that uses the matrix format to regress the dependent variable (*RTN_12M1M*) against the independent variables (*BETA* and *norm_MKTCAP*). The returned object returns the coefficients, tstats. The regression is performed for each column in the matrix. 

 
---

## Random Forest Modeling of Forward Return using market cap and beta


**Train the model using one year training period**
```R
factor_data    = list(BETA=BETA,MKTCAP=norm_MKTCAP)

model_RF<-ltool.randomforest.learnRF(FMRTN1M,
  factor_data    = factor_data,
  trainingPeriod = c('2014-12-31','2015-12-31'))
```

*learnRF is a custom function in LQuant Tool to run Random forest algo using the matrix data format*

*model_RF* is a custom object that keeps the coefficients for classification tree.  

**Predict for random forest**

```R
score_RF<-ltool.randomforest.getScoreRF(factor_data,testDate,model_RF)
```

**How does it compare with Linear Regression model** 


```R
coeffs<-ltool.regression.linearCoeffs(FMRTN1M,factor_data,trainingPeriod)
score_Linear<-ltool.regression.getScoreLinear(factor_data,testDate,coeffs)
cor(score_RF,score_Linear,use="complete.obs")
```


---

## Backtesting   

This demonstrates a simple factor backtesting. The *backtest.Basic* provides a suite of functions to see the efficacy of a single factor. It computes the following metrics for a factor driven portfolio

* Number of Stocks with Valid Values over Time
* Wealth Curve (Cumulative Return) for Long/Short basket based on factor value
* Information Ratio over time
* Average Annual Return
* Performance of individual bins
* Period over period Turnover


The example below illustrates a backtesting using the neutralized momentum. For long/short basket, the backester will be going long and short on top and bottom 20% of securities based on momentum respectively.  
```R
baskets <- 5
outBacktest<-backtest.Basic(momentum_neutralized,FMRTN1M,qnum=baskets)
names(outBacktest)
```

Convenient set of functions are provided to visualize the results of backtesting. 

```R
factorName <- 'Momentum (Neutrized for Size and Beta)'
plot.backtest.barline(outBacktest$coverage,"Coverage",isPercent = FALSE,stats=FALSE,title=factorName)
plot.backtest.wealth(outBacktest$wealth,"Cumulative Performance",title=factorName)
plot.backtest.wealthLS(outBacktest$wealth["LS",],"Cumulative Performance long/short",title=factorName)
plot.backtest.bar(outBacktest$IR,"Sharpe Ratio",isPercent=FALSE,title=factorName)
plot.backtest.bar(outBacktest$CAGR,"Average Annual Return (%)",isPercent=TRUE,title=factorName)
plot.backtest.barline(outBacktest$turnover["LS",],"Monthly one-way turnover",isPercent = TRUE,stats=FALSE,title=factorName)
plot.backtest.barline(outBacktest$ICs,"Rank IC (%)",isPercent = TRUE,stats=TRUE,period = 12,title=factorName)
plot.backtest.seasonality(outBacktest$ICs,"Rank IC (%)",isPercent = TRUE,title=factorName)
```


## Making it Faster (Parallelization) 

Since our data retrieval engine and analytics library is hosted on RStudio on Linux, we can utilize the multi-core apply function to essentially scale calculation across multiple cores on the server. For example, you can use the mclapply function to run many factors in parallel. 


```R
backtestResultList<-mclapply(list(momentum_neutralized = momentum_neutralized, momentum = momentum)
    ,mc.cores=2,
    function(oneFactor) backtest.Basic(oneFactor,FMRTN1M,qnum=baskets)
)
 
```

*One has to be careful with apply mclapply to ensure that individual apply job are robust, it is mostly recommended that you enclose the individual command in tryCatch 


```R
backtestResultList<-mclapply(list(momentum_neutralized = momentum_neutralized, momentum = momentum)
    ,mc.cores=2,
    function(oneFactor){
      tryCatch(return(backtest.Basic(oneFactor,FMRTN1M,qnum=baskets),)error=function(e){ return(NA) })
    }
  )
 
```


---

## Integrating Custom Data

Here as an example, we have integrated a custom data from a provider of Satellite image data. The data is available for past 8 year, hence we limit our analysis to those period. We have also defined a custom universe that has securities covered by the provider. 

```R
startDate<-'2010-12-31'
endDate<-'2017-03-31'
universeName<-'RSMETRIC_1'  
freq<-'1me'
```

There are custom factors created for this

```R
rsmetricsData<-getData(c('RSMETRIC_FILLRATE', 'RSMETRIC_FILLRATE_YOY_CHG', 'COMPANYNAME', ))
fillrate <- rsmetricsData$RSMETRIC_FILLRATE
plot.backtest.distribution(fillrate,yLabel = 'Fill Rate',title = 'Satellite Image Parking Lot Fill Rate',baskets = 5)
```


**Visualize security by security data**

The following code uses ggplot, melt to display the raw data for each company
```R
yoy_chg<-rsmetricsData$RSMETRIC_FILLRATE_YOY_CHG
plot.backtest.distribution(fillrate,yLabel = 'Fill Rate',title = 'Satellite Image Parking Lot Growth Rate',baskets = 5)

meltTable <- getMeltTable(yoy_chg, rsmetricsData$COMPANYNAME)
companyConcerned <- c('Best.Buy.Co.Inc', 'Target.Corp', 'Wal.Mart.Stores.Inc', 'Starbucks.Corp', 'Whole.Foods.Market.Inc')
dataConcerned <- meltTable[meltTable$CompanyName %in% companyConcerned,]
gg <- ggplot(dataConcerned, aes(x = date,y=rate,group = CompanyName, fill=CompanyName)) + 
  geom_bar(stat='identity') +
  scale_x_date(breaks = pretty_breaks(25),labels = date_format("%b-%y")) 
gg + facet_grid(CompanyName ~ .)
```


## Backtesting weighted portfolio for multiperiod

Here is an example of the portfolio of 3 stocks in the S&P 500, rebalanced on 2017-01-02 and 2017-02-02, and calculate the performance to 2017-03-24

Set the basic parameters

```R
startDate<-'2016-12-31'
endDate<-'2017-03-31'
universeName<-'SP500'  
freq<-'1d'
getData<-function(factors){
  wq.getdata(wq.newRequest()$runFor(universeName)$from(startDate)$to(endDate)$at(freq)$attr(.jarray(factors)))
}
```

Fetch Data
```R
data<-getData(c('PRCCD','CUM_DIV','SEDOL'))
```

Create a portfolio with custom weights. We create named list with weight vector
```R
weightList<-list()
weight<-c(0.5,0.2,0.3)
names(weight)<-c("2005973", "B7341C6", "2190385")
weightList[['2017-01-02']]<-weight

weight<-c(0.2,0.3,0.5)
names(weight)<-c("2005973", "B7341C6", "2190385")
weightList[['2017-02-02']]<-weight
```

Get Prices and Dividend
```R
identifier<-data[['SEDOL']]
dailyPrice<-data[['PRCCD']]
dailyCumDiv<-data[['CUM_DIV']]
```
Run backtest
```R
rtn<-backtest.getDailyReturns(weightList, identifier, dailyPrice, dailyCumDiv, endDate='2017-03-24')
```

Get Stats
```R
wealth<- backtest.getWealth (rtn)
Vol<- backtest.getVol(rtn)
CAGR<- backtest.getCAGR(rtn)
Sharpe<- backtest.getIR(rtn)
maxDD<-backtest.getMaxDD(rtn)
```


