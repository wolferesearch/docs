# swagger_client.OptimizationApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_optimization**](OptimizationApi.md#get_optimization) | **GET** /optimization/{uuid}/{file} | Gets optimization result for the date
[**get_optimization_file_list**](OptimizationApi.md#get_optimization_file_list) | **GET** /optimization/{uuid} | Gets optimization file list
[**get_optimization_list**](OptimizationApi.md#get_optimization_list) | **GET** /optimization | Gets the list of optimization tasks historical and current
[**new_optimization_request**](OptimizationApi.md#new_optimization_request) | **POST** /optimization | New Optimization Request


# **get_optimization**
> list[str] get_optimization(uuid, file)

Gets optimization result for the date

Returns optimized portfolio and other statistics

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
api_instance = swagger_client.OptimizationApi(swagger_client.ApiClient(configuration))
uuid = 'uuid_example' # str | ID of the optimization
file = 'file_example' # str | Optimization result file

try:
    # Gets optimization result for the date
    api_response = api_instance.get_optimization(uuid, file)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OptimizationApi->get_optimization: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**| ID of the optimization | 
 **file** | **str**| Optimization result file | 

### Return type

**list[str]**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_optimization_file_list**
> list[str] get_optimization_file_list(uuid)

Gets optimization file list

Returns file list for which optimization is run and summary

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
api_instance = swagger_client.OptimizationApi(swagger_client.ApiClient(configuration))
uuid = 'uuid_example' # str | ID of the optimization

try:
    # Gets optimization file list
    api_response = api_instance.get_optimization_file_list(uuid)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OptimizationApi->get_optimization_file_list: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **str**| ID of the optimization | 

### Return type

**list[str]**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_optimization_list**
> list[OptimizationTemplate] get_optimization_list()

Gets the list of optimization tasks historical and current

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
api_instance = swagger_client.OptimizationApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of optimization tasks historical and current
    api_response = api_instance.get_optimization_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OptimizationApi->get_optimization_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[OptimizationTemplate]**](OptimizationTemplate.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **new_optimization_request**
> str new_optimization_request(body)

New Optimization Request

Runs a new Optimization Request

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
api_instance = swagger_client.OptimizationApi(swagger_client.ApiClient(configuration))
body = swagger_client.OptimizationRequest() # OptimizationRequest | Optimization Request

try:
    # New Optimization Request
    api_response = api_instance.new_optimization_request(body)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OptimizationApi->new_optimization_request: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OptimizationRequest**](OptimizationRequest.md)| Optimization Request | 

### Return type

**str**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

