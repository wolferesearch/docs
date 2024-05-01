# swagger_client.CatalogApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_optimization_template**](CatalogApi.md#create_optimization_template) | **POST** /template/optimization | Creates new optimization template
[**create_portfolio**](CatalogApi.md#create_portfolio) | **POST** /portfolio | Creates / Updates Portoflio
[**create_risk_model_template**](CatalogApi.md#create_risk_model_template) | **POST** /template/risk-model | Creates / Updates Risk Model Template based on ...
[**get_factor_list**](CatalogApi.md#get_factor_list) | **GET** /factor | Gets the list of applicable factors
[**get_meta_list**](CatalogApi.md#get_meta_list) | **GET** /meta | Gets the list of applicable meta fields
[**get_portfolio_list**](CatalogApi.md#get_portfolio_list) | **GET** /portfolio | Gets the list of applicable portfolios
[**get_template_list**](CatalogApi.md#get_template_list) | **GET** /template | Gets the list of appicable templates
[**get_universe_list**](CatalogApi.md#get_universe_list) | **GET** /universe | Gets the list of applicable universes


# **create_optimization_template**
> create_optimization_template(body)

Creates new optimization template

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))
body = swagger_client.TemplateModel() # TemplateModel | Optimization Template

try:
    # Creates new optimization template
    api_instance.create_optimization_template(body)
except ApiException as e:
    print("Exception when calling CatalogApi->create_optimization_template: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TemplateModel**](TemplateModel.md)| Optimization Template | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_portfolio**
> create_portfolio(body)

Creates / Updates Portoflio

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))
body = swagger_client.RiskModelTemplate() # RiskModelTemplate | Risk Model Template

try:
    # Creates / Updates Portoflio
    api_instance.create_portfolio(body)
except ApiException as e:
    print("Exception when calling CatalogApi->create_portfolio: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RiskModelTemplate**](RiskModelTemplate.md)| Risk Model Template | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_risk_model_template**
> create_risk_model_template(body)

Creates / Updates Risk Model Template based on ...

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))
body = swagger_client.TemplateModel() # TemplateModel | Risk Model Template

try:
    # Creates / Updates Risk Model Template based on ...
    api_instance.create_risk_model_template(body)
except ApiException as e:
    print("Exception when calling CatalogApi->create_risk_model_template: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TemplateModel**](TemplateModel.md)| Risk Model Template | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_factor_list**
> list[FactorModel] get_factor_list()

Gets the list of applicable factors

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of applicable factors
    api_response = api_instance.get_factor_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogApi->get_factor_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[FactorModel]**](FactorModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_meta_list**
> list[MetaModel] get_meta_list()

Gets the list of applicable meta fields

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of applicable meta fields
    api_response = api_instance.get_meta_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogApi->get_meta_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[MetaModel]**](MetaModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_portfolio_list**
> list[PortfolioModel] get_portfolio_list()

Gets the list of applicable portfolios

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of applicable portfolios
    api_response = api_instance.get_portfolio_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogApi->get_portfolio_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[PortfolioModel]**](PortfolioModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_template_list**
> list[TemplateModel] get_template_list()

Gets the list of appicable templates

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of appicable templates
    api_response = api_instance.get_template_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogApi->get_template_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[TemplateModel]**](TemplateModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_universe_list**
> list[UniverseModel] get_universe_list()

Gets the list of applicable universes

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure HTTP basic authorization: basicAuth
configuration = swagger_client.Configuration()
configuration.username = 'YOUR_USERNAME'
configuration.password = 'YOUR_PASSWORD'

# create an instance of the API class
api_instance = swagger_client.CatalogApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of applicable universes
    api_response = api_instance.get_universe_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CatalogApi->get_universe_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[UniverseModel]**](UniverseModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

