# swagger_client.JobApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_job_list**](JobApi.md#get_job_list) | **GET** /job | Gets the list of applicable jobs


# **get_job_list**
> list[JobModel] get_job_list()

Gets the list of applicable jobs

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
api_instance = swagger_client.JobApi(swagger_client.ApiClient(configuration))

try:
    # Gets the list of applicable jobs
    api_response = api_instance.get_job_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling JobApi->get_job_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**list[JobModel]**](JobModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

