## Author: Kartik Arora
## Date : 13-Feb-2018
## 
## File shows simple example of using Risk Model/Optimization API

## Source the API file
source('micsvc.R')

# Setup a connection object 
conn1 <- qes.microsvc.Conn$new(username = 'hjain', password = 'hjain123')
conn1 <- qes.microsvc.Conn$new(username = 'limmant', password = 'UM5KBYzX')


# Get instance of risk model builder
risk_model_builder <- conn1$get_risk_model_builder()

# Submit a new risk model builder request
risk_model_builder$new_request(universe = 'QES_EUROPE',
                              template = 'euro-ext',
                              startDate = '2019-10-21',
                              endDate = '2019-10-24',
                              freq = '1d')
# Wait for it to finish
risk_model_builder$wait(max_wait_secs = 600)

dates <- risk_model_builder$dates()
alld <- lapply(dates,risk_model_builder$get_data)
names(alld) <- dates

xx <- do.call(rbind,
              lapply(dates,function(dt) {
                x <- alld[[dt]]
                ix <- which(endsWith(names(x),'exp'))
                subset(x[[ix]],ID == '9K6257DOY9')
              }))

# Download all data to a directory
risk_model_builder$download_all('QES-Risk-Model-Data')


# Uploading the Portfolio

conn1$upload_portfolio(id = 'Custom_Port1', filename = 'sample-port.csv')

# See the uploaded portfolio
catalog <- conn1$get_catalog()

portfolios <- catalog$get_portfolios()

View(portfolios)

# See the new factor

factors <- catalog$get_factors()

factors[which(startsWith(factors$ID,'Custom_Port1')),]


View(factors)





