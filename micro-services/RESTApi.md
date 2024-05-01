QES Quant Service API
=====================
QES Quant Service API provides easy access to Risk/Optimization API


**Version:** 0.0.2

**Terms of service:**  
http://wolferesearch.com

**Contact information:**  
luo.qes@wolferesearch.com  

**License:** [Restricted](http://wolferesearch.com)

[Find out more about Swagger](http://swagger.io)
### Security
---
**basicAuth**  

|basic|*Basic*|
|---|---|

### /job
---
##### ***GET***
**Summary:** Gets the list of applicable jobs

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [JobModel](#jobmodel) ] |

### /universe
---
##### ***GET***
**Summary:** Gets the list of applicable universes

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [UniverseModel](#universemodel) ] |

### /factor
---
##### ***GET***
**Summary:** Gets the list of applicable factors

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [FactorModel](#factormodel) ] |

### /meta
---
##### ***GET***
**Summary:** Gets the list of applicable meta fields

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [FactorModel](#factormodel) ] |

### /portfolio
---
##### ***GET***
**Summary:** Gets the list of applicable portfolios

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [PortfolioModel](#portfoliomodel) ] |

##### ***POST***
**Summary:** Creates / Updates Portoflio

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body | Risk Model Template | Yes | [RiskModelTemplate](#riskmodeltemplate) |

**Responses**

| Code | Description |
| ---- | ----------- |
| 405 | Invalid input |

### /template
---
##### ***GET***
**Summary:** Gets the list of appicable templates

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [TemplateModel](#templatemodel) ] |

### /risk-model
---
##### ***POST***
**Summary:** Creates New Risk Model

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body | Risk Model Parameters | Yes | [RiskModelRequest](#riskmodelrequest) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation return uuid | string |
| 403 | Not Authorized |  |
| 405 | Invalid input |  |

##### ***GET***
**Summary:** Gets the list of risk models historical and current

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [RiskModel](#riskmodel) ] |

### /risk-model/{uuid}
---
##### ***GET***
**Summary:** Gets risk model dates list

**Description:** Returns dates for which risk model is available

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| uuid | path | ID of the risk model | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | [ string ] |
| 400 | Invalid status value |  |

### /risk-model/{uuid}/{date}
---
##### ***GET***
**Summary:** Gets risk model files listing

**Description:** Returns list of files available for risk model for a date

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| uuid | path | ID of the risk model | Yes | string |
| date | path | date of the risk model (yyyymmdd) | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | [ string ] |
| 400 | Invalid status value |  |

### /risk-model/{uuid}/{date}/{file}
---
##### ***GET***
**Summary:** Download a risk model file

**Description:** Download risk model CSV File

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| uuid | path | ID of the risk model | Yes | string |
| date | path | date of the risk model (yyyymmdd) | Yes | string |
| file | path | Risk model file | Yes | string |

**Responses**

| Code | Description |
| ---- | ----------- |
| 200 | successful operation |
| 400 | Invalid status value |

### /optimization
---
##### ***POST***
**Summary:** New Optimization Request

**Description:** Runs a new Optimization Request

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body | Optimization Request | Yes | [OptimizationRequest](#optimizationrequest) |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation return uuid | string |
| 403 | Not Authorized |  |
| 405 | Invalid input |  |

##### ***GET***
**Summary:** Gets the list of optimization tasks historical and current

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | Successful operation | [ [OptimizationTemplate](#optimizationtemplate) ] |

### /optimization/{uuid}
---
##### ***GET***
**Summary:** Gets optimization file list

**Description:** Returns file list for which optimization is run and summary

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| uuid | path | ID of the optimization | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | [ string ] |
| 400 | Invalid status value |  |

### /optimization/{uuid}/{file}
---
##### ***GET***
**Summary:** Gets optimization result for the date

**Description:** Returns optimized portfolio and other statistics

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| uuid | path | ID of the optimization | Yes | string |
| file | path | Optimization result file | Yes | string |

**Responses**

| Code | Description | Schema |
| ---- | ----------- | ------ |
| 200 | successful operation | [ string ] |
| 400 | Invalid status value |  |

### /template/risk-model
---
##### ***POST***
**Summary:** Creates / Updates Risk Model Template based on ...

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body | Risk Model Template | Yes | [TemplateModel](#templatemodel) |

**Responses**

| Code | Description |
| ---- | ----------- |
| 405 | Invalid input |

### /template/optimization
---
##### ***POST***
**Summary:** Creates new optimization template

**Parameters**

| Name | Located in | Description | Required | Schema |
| ---- | ---------- | ----------- | -------- | ---- |
| body | body | Optimization Template | Yes | [TemplateModel](#templatemodel) |

**Responses**

| Code | Description |
| ---- | ----------- |
| 405 | Invalid input |

### Models
---

### OptimizationRequest  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| portfolio | string | Mnemonic of the portfolio to be optimized | No |
| template | string | One of the previously defined templates for risk | No |
| startDate | string | Start date (yyyy-mm-dd) | No |
| endDate | string | End date (yyyy-mm-dd) | No |
| freq | string | Frequency of risk model generation | No |
| benchmark | string | Benchmark for Tracking error optimization problem - Any of the standard universes and portfolios can be used - as benchmark. The caller should provide the benchmark - mnemonic, e.g., QES_EUROPE, QES_WORLD, SP500. System uses - the Float weighting as benchmark. | No |
| transaction_cost | number | Transaction cost  to consider in the optimization. - This is relevant for MVO optimization where transaction - cost is taken out from objective function. The transaction - cost is a quadratic function added based on value selected - For when the transaction_cost = 1, about 1 median spread - is estimated as the cost when 7% of ADV is participated, - for when transaction_cost = 5, 1 median spread cost is - estimated for when the participation is 3%. The per share - cost is linear and in objective function, the cost becomes - quadratic | No |

### RiskModelRequest  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| universe | string | Mnemonic for Risk Estimation universe | No |
| template | string | One of the previously defined templates for risk | No |
| startDate | string | Start date (yyyy-mm-dd) | No |
| endDate | string | End date (yyyy-mm-dd) | No |
| freq | string | Frequency of risk model generation | No |

### PortfolioModel  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| ID | string | Portfolio Name | No |
| UPLOADEDBY | string | Associated User | No |
| UPLOADEDTIME | string | Date on which portoflio file was uploaded | No |

### RiskModel  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| uuid | string | Unique id of the risk model | No |
| template | string | Template used for risk model | No |
| dateCreated | string | Date on which riks model was created | No |

### UniverseModel  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| ID | string | Unique Indentifier | No |
| NAME | string | Unique Name | No |
| SECTOR | string | Applicable Sector | No |
| COUNTRY | string | Applicable Country or Geographic Region | No |
| DESCRIPTION | string | Descriptive Text | No |

### FactorModel  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| ID | string | Unique Indentifier | No |
| CATEGORY | string | Unique Name | No |
| SUBCATEGORY | string | Applicable Sector | No |
| DESCRIPTION | string | Descriptive Text | No |

### MetaModel  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| ID | string | Unique Indentifier | No |
| NAME | string | Unique Name | No |
| DESCRIPTION | string | Descriptive Text | No |

### TemplateModel  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| TYPE | string | Applicable Process - Risk-Model, Optimization | No |
| OWNER | string | Template Creator | No |
| NAME | string | Unique Name | No |
| DESCRIPTION | string | Descriptive Text | No |
| MODIFIED_DATE | string | Timestamp of last modified | No |
| CONTENT | string | Template Content | No |

### JobModel  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| TYPEID | string | Unique id of the risk model | No |
| USER_ | string | Template used for risk model | No |
| UUID | string | Date on which riks model was created | No |
| STARTTIME | string | Date on which riks model was created | No |
| STATUS | string | Date on which riks model was created | No |
| ENDTIME | string | Date on which riks model was created | No |
| MESSAGE | string | Date on which riks model was created | No |

### RiskModelTemplate  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| factors | [ [FactorInput](#factorinput) ] | List of factor mnemonics inputs | No |
| meta | [ [MetaInput](#metainput) ] | List of meta data mnemonics inputs | No |
| options | [RiskModelOption](#riskmodeloption) |  | No |
| covArgs | [CovarianceMatrixOption](#covariancematrixoption) |  | No |

### FactorInput  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| name | string | Human readable name for the factor, should be unique across the list | No |
| mnemonic | string | Factor Mnemonic | No |

### MetaInput  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| name | string | Human readable name for the factor, should be unique across the list | No |
| mnemonic | string | Meta Mnemonic (SEDOL, TICKER, CURRENCY, QES_GSECTOR, QES_GGROUP, QES_COUNTRY) | No |

### RiskModelOption  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| spRisk | [RiskModelSpRiskOption](#riskmodelspriskoption) |  | No |

### RiskModelSpRiskOption  

Option to control the specific risk of the risk model

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| shrinkage | number | Shrinkage to control the specific risk | No |
| fn | string |  | No |

### CovarianceMatrixOption  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| interval | integer |  | No |
| cov.period | integer |  | No |
| var.period | integer |  | No |
| shirinkageIntensity | number |  | No |

### OptimizationTemplate  

| Name | Type | Description | Required |
| ---- | ---- | ----------- | -------- |
| target_risk | number | Annualized Risk Target for optimization | No |
| bound | [ number ] | Minimum and Maximum weight bound | No |
| max_ADV_participation | number | ADV Participation Ceiling (5% == 0.05) | No |
| max_turonver | number | Maximum turnover allowed | No |
| gross_weight | number | Total notional weight of the optimized basket | No |
| net_weight | number | Net weight of the optimized basket. For Long/Short neutral the Net weight should be 0 | No |
| objective | string |  | No |
| lambda | number | Risk aversion parameter, only used when objective is set as MVO | No |