
########## DEMO OF LQTOOL ############
##########   BY LUO'S QES ############


require(wquantR)
library(lqtool)

## Define Parameters

startDate<-'1994-12-31'
endDate<-'2017-03-31'
universeName<-'SP500'  
freq<-'1me'

### Some utility functions
source('/mnt/ebs1/data/demo/demoUtil.R')

##############  1.Download Factors Data and Visualize ##############

# Use a to concat all factor name we try to download
data<-getData(c('PRCCD','CUM_DIV','RTN_12M1M','ROE','MKTCAP','IN_SP500','GSUBIND'))

# This returns us factor data as a list of data matrices I (Items) X S (Securities) X T (Dates)

# Display all items in the list of data matrices
names(data)

# Show quantiles
plot.backtest.distribution(data$RTN_12M1M, "Momentum",title='Momentum',baskets = 5)
plot.backtest.density(data$RTN_12M1M, "Momentum",title='Momentum Density')

##############  2.Customized Factors ##############  
  
# Define a custom Earnings Yield 
wq.define('EarningsYield=0.5*EPSF12/PRCCD+0.50*CIQ_EST_EPS_MED_FY1/PRCCD')

# Get data from the query engine for the custom factor
data_cust <- getData('EarningsYield')
# Visualize Earnings Yield
plot.backtest.density3D(data_cust$EarningsYield, "Earnings Yield (%)",title='Earnings Yield Density')

##############  3.Get Sectors & Customize Universe ##############  

sector_mask <- getSectorMask(c('Energy','Utilities'),data)

#Mask the data
sectorData<-data_cust$EarningsYield
sectorData[!sector_mask]<-NA
mask <- rowSums(sector_mask) > 0

#show the sector coverage
colSums(!is.na(sectorData),na.rm=T)

#See the drop in First Quarter of 2016 when Oil prices crashed
plot.backtest.distribution(sectorData, "Earnings Yield (%)",title='Earnings Yield',baskets = 5)

##############  4.Normalize Factors ##############  

plot.backtest.distribution(data$MKTCAP, "Market Cap",title='Market Cap',baskets = 5)
norm_MKTCAP <- basic.neutralizeFactor(data$MKTCAP, method = 'z_score')
plot.backtest.distribution(norm_MKTCAP, "Market Cap (Normalized) ",title='Market Cap',baskets = 5)

# confirmation of normalization
mean(norm_MKTCAP[,'2015-01-31'], na.rm = T)
var(norm_MKTCAP[,'2015-01-31'], na.rm = T)

# We can also normalize them based on different sectors/country
norm_MKTCAP_by_sectors <- basic.neutralizeFactor(data$MKTCAP, method = 'z_score', classMatrix = sector_mask)
plot.backtest.distribution(norm_MKTCAP_by_sectors, "Market Cap (Normalized) ",title='Market Cap',baskets = 5)

# Check if normalized for Energy and Utilities sectors
mean(norm_MKTCAP_by_sectors[, 200], na.rm = T)
var(norm_MKTCAP_by_sectors[, 200], na.rm = T)
mean(norm_MKTCAP_by_sectors[, 200][sector_mask[,200]], na.rm = T)
var(norm_MKTCAP_by_sectors[, 200][sector_mask[,200]], na.rm = T)


#### ADV

#@mavg(CSHTRD,'3m')

#wq.define((CSHTRD_AV3M-CSHTRD_AV3M_L3M)/MKTCAP

##############  5.Run Linear Regression on Factors and Neutralize ##############  

# Get monthly return
RTN<-(data[['PRCCD']]+data[['CUM_DIV']]-wLag(data[['CUM_DIV']]))/wLag(data[['PRCCD']])-1

# Lag by -1 period to get forward return for backtesting later
FMRTN1M<-wLag(RTN,-1)

plot.backtest.distribution(RTN, "Total Return",title='Total Return',baskets = 5)

# Filter out all not-in-universe at point of time
idx<-data[[paste('IN_',universeName,sep='')]]>0
idx[is.na(idx)]<-FALSE
FMRTN1M[!idx]<-NA
data<-lapply(data,function(x){
  x[!idx]<-NA
  return(x)
})

# Create a new list with derived factors
factor_data<-list()
factor_data[['BETA']]<-basic.calculateBeta(RTN,idx,)
factor_data[['MKTCAP']]<-norm_MKTCAP

# Add momentum
momentum<-data[['RTN_12M1M']]
plot.backtest.density(momentum,"Momentum",title='Momentum')
plot.backtest.distribution(momentum, "Momentum",title='Momentum',baskets = 5)

# Equation of Regression (Momentum ~ Market Cap, Beta)
regressFactors<-basic.regressFactors(momentum,factor_data)
momentum_neutralized<-regressFactors[["residual"]]

coeff<-regressFactors[["coeff"]]
tstats<-regressFactors[["tstats"]]

plot.backtest.density(momentum_neutralized,"Factor score",title='NEUTRALIZED MOMENTUM')
plot.backtest.distribution(momentum_neutralized, "Factor score",title='NEUTRALIZED MOMENTUM',baskets = 5)

##############  6.Random Forest ##############  

# Get Additional Data
factor_data[['ROE']]<-data[['ROE']]
addData<-getData(c('OP_MARGIN','ES_TP_R3M','PE_LTM_B','GR_FY1_DPS'))

factor_data[['OP_MARGIN']]<-addData[['OP_MARGIN']]
factor_data[['ES_TP_R3M']]<-addData[['ES_TP_R3M']]
factor_data[['PE_LTM_B']]<-addData[['PE_LTM_B']]
factor_data[['GR_FY1_DPS']]<-addData[['GR_FY1_DPS']]

trainingPeriod<-c('2014-12-31','2015-12-31')
testDate<-"2016-12-31"

### learn random forest
model_RF<-learnRF(FMRTN1M,factor_data,trainingPeriod)

## get score for random forest
score_RF<-getScoreRF(factor_data,testDate,model_RF)

### regression
coeffs<-linearCoeffs(FMRTN1M,factor_data,trainingPeriod)
### get score
score_Linear<-getScoreLinear(factor_data,testDate,coeffs)
cor(score_RF,score_Linear,use="complete.obs")

##############  7.Run Backtesting ##############  

baskets <- 5
outBacktest<-backtest.Basic(momentum_neutralized,FMRTN1M,qnum=baskets)
names(outBacktest)

# Plot:
factorName <- 'Momentum (Neutrized for Size and Beta)'
plot.backtest.barline(outBacktest$coverage,"Coverage",isPercent = FALSE,stats=FALSE,title=factorName)
plot.backtest.wealth(outBacktest$wealth,"Cumulative Performance",title=factorName)
plot.backtest.wealthLS(outBacktest$wealth["LS",],"Cumulative Performance long/short",title=factorName)
plot.backtest.bar(outBacktest$IR,"Sharpe Ratio",isPercent=FALSE,title=factorName)
plot.backtest.bar(outBacktest$CAGR,"Average Annual Return (%)",isPercent=TRUE,title=factorName)
plot.backtest.barline(outBacktest$turnover["LS",],"Monthly one-way turnover",isPercent = TRUE,stats=FALSE,title=factorName)
plot.backtest.barline(outBacktest$ICs,"Rank IC (%)",isPercent = TRUE,stats=TRUE,period = 12,title=factorName)
plot.backtest.seasonality(outBacktest$ICs,"Rank IC (%)",isPercent = TRUE,title=factorName)


# Paralelly Testing:

momentumList <- list(momentum_neutralized = momentum_neutralized, momentum = momentum)
backtestResultList<-mclapply(momentumList,mc.cores=2,function(oneFactor){
  tryCatch({
    outBacktest<-backtest.Basic(oneFactor,FMRTN1M,qnum=baskets)
    return(outBacktest)
  },
  error = function(e) NULL)
})
names(backtestResultList)
factorName <- 'Momentum'
plot.backtest.wealth(backtestResultList$momentum$wealth,"Cumulative Performance",title=factorName)
plot.backtest.wealthLS(backtestResultList$momentum$wealth["LS",],"Cumulative Performance long/short",title=factorName)
plot.backtest.bar(backtestResultList$momentum$IR,"Sharpe Ratio",isPercent=FALSE,title=factorName)
plot.backtest.barline(backtestResultList$momentum$ICs,"Rank IC (%)",isPercent = TRUE,stats=TRUE,period = 12,title=factorName)


##############  8. RSMetrics ##############  
# Change Config for RSMetrics:
startDate<-'2010-12-31'
endDate<-'2017-03-31'
universeName<-'RSMETRIC_1'  
freq<-'1me'

# Get the raw fill rate based on the cars/space
rsmetricsData<-getData(c('RSMETRIC_FILLRATE', 'RSMETRIC_FILLRATE_YOY_CHG', 'COMPANYNAME', ))
fillrate <- rsmetricsData$RSMETRIC_FILLRATE
plot.backtest.distribution(fillrate,yLabel = 'Fill Rate',title = 'Satellite Image Parking Lot Fill Rate',baskets = 5)

# Get the balanced growth in fill rate for companies
yoy_chg<-rsmetricsData$RSMETRIC_FILLRATE_YOY_CHG
plot.backtest.distribution(fillrate,yLabel = 'Fill Rate',title = 'Satellite Image Parking Lot Growth Rate',baskets = 5)

meltTable <- getMeltTable(yoy_chg, rsmetricsData$COMPANYNAME)
companyConcerned <- c('Best.Buy.Co.Inc', 'Target.Corp', 'Wal.Mart.Stores.Inc', 'Starbucks.Corp', 'Whole.Foods.Market.Inc')
dataConcerned <- meltTable[meltTable$CompanyName %in% companyConcerned,]
gg <- ggplot(dataConcerned, aes(x = date,y=rate,group = CompanyName, fill=CompanyName)) + 
  geom_bar(stat='identity') +
  scale_x_date(breaks = pretty_breaks(25),labels = date_format("%b-%y")) 
gg + facet_grid(CompanyName ~ .)
