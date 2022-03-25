# LQuant - Equity Financial Data Library


## Introduction

LQuant is a Java based library that intermediates as data broker for interacting with financial data. We have integrated several data source in our distributed cloud based databases. We have employed polyglot storage to store structured and unstructured data sets. 


## Infrastructure And Architecture



## Design

**LQuant** works with time series data. Broadly, the data within LQuant is organized in 3 main dimensions, entity, attribute and time. The relationship between them is as follows:

1. Entity has many Attributes
2. Each Entity/Attribute pair is a time series.  


A unique data point exist for the following set of dimensions:

* Entity
* Attribute
* Data Time
* Observed Time




## Infrastructure

We have utilized Amazon AWS to host the Quant Infrastructure. Infrastructure is highly scalable and flexible. 

![](https://s3.amazonaws.com/lquant-images/QuantDataPipeline.png)

## Stack


| Technology | Description |
| -----------| ----------- |
|![](https://s3.amazonaws.com/lquant-images/AWS2-162x125.png)| Amazon Web services has become a dominant cloud provider. We utilize AWS to host our entire infrastructure|
|![](https://s3.amazonaws.com/lquant-images/Oracle-Logos.png)| Oracle is the main database utilized to host raw data directly from Vendors|
|![](https://s3.amazonaws.com/lquant-images/AmazonRDS.png)| RDS is a Database as a Service (DaaS) offered by Amazon, RDS does auto back up, multi-az deployment |
|![](https://s3.amazonaws.com/lquant-images/RStudio-Ball.png)| RStudio is convenient interface to interact with a Remote R Session. We utilize co-location of computation server (RStudio) and Database to reduce network delays|
|![](https://s3.amazonaws.com/lquant-images/Java_logo.png) | Java is used for data virtualization of time series data. |


## Databases
| Database | Description |
| ------ | ----------- |
|Capital IQ | S&P Captial IQ contains myriad of data items. We source fundamental, pricing data for Global Securities. The data is provided and maintained by Xpressfeed Loader|
|Thomson Reuters QA Direct | Thomson Reuters Quantitative and Analytics Direct Data. We source fundamental data for non-US securities, I/B/E/S data, M&A Data and ownership data. The data is maintained by communicator process |
|Axioma | Axioma provides risk model and optimizer functionality |
|Ravenpack | Ravenpack provides News sentiment data |
|S&P BMI | S&P Broad Market Index 


## Data Virtualization (In Memory Timeseries database)

Data is brokered between the final Consumer (i.e., Research Analyst) and the Databases using a middle layer library written in Java. This library performs in memory point in time computation (PIT) to remove look ahead bias when providing the data. The library also provides uniform query language to access all timeseries database. Library can connect to several database and seamless join data.  


## Universe

Universe is a set of entities (e.g., Securities) that change over time. At any given time, a universe (e.g., S&P 500) contain a finite set of securities. In LQuant, research starts from *Universe* (e.g., S&P US BMI, S&P Global BMI, Russell 3K etc). 

## Entity

In LQuant, an Entity is a named concept that has factors associated it. It is identified by a unique id. For example, primary Issue of International Business Machine is identified by G006066_01. A country (e.g. US) or a currency (e.g., USD) can also be entity. 


## Factor / Attributes

The word "*Factor*" or "*Attribute*" is used interchangeably throughout this document and they mean exactly the same thing.    Factors are the backbone of LQuant infrastructure. Factors are identified by a unique id, e.g., CS_PRCCD is a factor that represent the close price of the entity. Combination of Entity and Factor provides a unique time series that can be projected on an array of observation dates (a.k.a point dates). Factor are classified as follows:

| Factor Type | Description |
| ----------- | ----------- | 
| Raw Vendor Factors | These factors are directly extracted from the data source., e.g., CS_PRCCD |
| Mapped Factor | These factors are merely aliases and point to a raw factor, e.g., PRCCD | 
| Interpreted Factor | These factors are interpreted based on their suffixes and prefixes, e.g., CS_SALEQ_LTM is interpreted as sum of last 4 quarterly items,  IN_SP500 is interpreted as a factor that returns 0 or 1 based on whether the entity is present in the universe SP500|
| Expression Factor | Mathematical Expression along with supported timeseries functions can be used to express a factor, e.g., RECTR + TXR + RECCO |
| Function Factor | Factor that have function associated with, e.g., CUM_CS_DIV cumulates all values from CS_DIV |


### Examples
|Factor Id | Factor Type | Description |
| ---------| ----------- | ----------- |
| CS_PRCCD | Raw Vendor Factor | This factor comes directly from Compustat. The prefix CS stands for Compustat. This item is available for US and Canadian securities | 
| PRCCD    | Mapped Factor | This factor maps to different raw vendor factor based on the security. If the security is classified as US security then it would map to CS_PRCCD that comes from Compustat sec_dprc table, otherwise it comes from CIQ_PRICECLOSE available in ciqEquityPrices. 







 



