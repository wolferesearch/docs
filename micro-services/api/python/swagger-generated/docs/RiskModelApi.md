# swagger_client.RiskModelApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_risk_model**](RiskModelApi.md#create_risk_model) | **POST** /risk-model | Creates New Risk Model
[**get_risk_model_date_files**](RiskModelApi.md#get_risk_model_date_files) | **GET** /risk-model/{uuid}/{date} | Gets risk model files listing
[**get_risk_model_date_list**](RiskModelApi.md#get_risk_model_date_list) | **GET** /risk-model/{uuid} | Gets risk model dates list
[**get_risk_model_file**](RiskModelApi.md#get_risk_model_file) | **GET** /risk-model/{uuid}/{date}/{file} | Download a risk model file
[**get_risk_model_list**](RiskModelApi.md#get_risk_model_list) | **GET** /risk-model | Gets the list of risk models historical and current


# **create_risk_model**
> str create_risk_model(body)

Creates New Risk Model

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
api_instance = swagger_client.RiskModelApi(swagger_client.ApiClient(configuration))
body = swagger_client.RiskModelRequest() # RiskModelRequest | Risk Model Parameters

try:
    # Creates New Risk Model
    api_response = api_instance.create_risk_model(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RiskModelApi->create_risk_model: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RiskModelRequest**](RiskModelRequest.md)| Risk Model Parameters | 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_risk_model_date_files**
> list[str] get_risk_model_date_files(uuid, _date)

Gets risk model files listing

Returns list of files available for risk model for a date

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
api_instance = swagger_client.RiskModelApi(swagger_client.ApiClient(configuration))
uuid = 'uuid_example' # str | ID of the risk model
_date = '_date_example' # str | date of the risk model (yyyymmdd)

try:
    # Gets risk model files listing
    api_response = api_instance.get_risk_model_date_files(uuid, _date)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RiskModelApi->get_risk_model_date_files: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**| ID of the risk model | 
 **_date** | **str**| date of the risk model (yyyymmdd) | 

### Return type

**list[str]**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_risk_model_date_list**
> list[str] get_risk_model_date_list(uuid)

Gets risk model dates list

Returns dates for which risk model is available

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
api_instance = swagger_client.RiskModelApi(swagger_client.ApiClient(configuration))
uuid = 'uuid_example' # str | ID of the risk model

try:
    # Gets risk model dates list
    api_response = api_instance.get_risk_model_date_list(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RiskModelApi->get_risk_model_date_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**| ID of the risk model | 

### Return type

**list[str]**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_risk_model_file**
> get_risk_model_file(uuid, _date, file)

Download a risk model file

Download risk model CSV File

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
api_instance = swagger_client.RiskModelApi(swagger_client.ApiClient(configuration))
uuid = 'uuid_example' # str | ID of the risk model
_date = '_date_example' # str | date of the risk model (yyyymmdd)
file = 'file_example' # str | Risk model file

try:
    # Download a risk model file
    api_instance.get_risk_model_file(uuid, _date, file)
except ApiException as e:
    print("Exception when calling RiskModelApi->get_risk_model_file: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**| ID of the risk model | 
 **_date** | **str**| date of the risk model (yyyymmdd) | 
 **file** | **str**| Risk model file | 

### Return type

void (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_risk_model_list**
> list[RiskModel] get_risk_model_list()

Gets the list of risk models historical and current

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
api_instance = swagger_client.RiskModelApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of risk models historical and current
    api_response = api_instance.get_risk_model_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RiskModelApi->get_risk_model_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[RiskModel]**](RiskModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

