# OptimizationApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getOptimization**](OptimizationApi.md#getOptimization) | **GET** /optimization/{uuid}/{file} | Gets optimization result for the date
[**getOptimizationFileList**](OptimizationApi.md#getOptimizationFileList) | **GET** /optimization/{uuid} | Gets optimization file list
[**getOptimizationList**](OptimizationApi.md#getOptimizationList) | **GET** /optimization | Gets the list of optimization tasks historical and current
[**newOptimizationRequest**](OptimizationApi.md#newOptimizationRequest) | **POST** /optimization | New Optimization Request


<a name="getOptimization"></a>
# **getOptimization**
> List&lt;String&gt; getOptimization(uuid, file)

Gets optimization result for the date

Returns optimized portfolio and other statistics

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OptimizationApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

OptimizationApi apiInstance = new OptimizationApi();
String uuid = "uuid_example"; // String | ID of the optimization
String file = "file_example"; // String | Optimization result file
try {
    List<String> result = apiInstance.getOptimization(uuid, file);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OptimizationApi#getOptimization");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **String**| ID of the optimization |
 **file** | **String**| Optimization result file |

### Return type

**List&lt;String&gt;**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getOptimizationFileList"></a>
# **getOptimizationFileList**
> List&lt;String&gt; getOptimizationFileList(uuid)

Gets optimization file list

Returns file list for which optimization is run and summary

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OptimizationApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

OptimizationApi apiInstance = new OptimizationApi();
String uuid = "uuid_example"; // String | ID of the optimization
try {
    List<String> result = apiInstance.getOptimizationFileList(uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OptimizationApi#getOptimizationFileList");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **String**| ID of the optimization |

### Return type

**List&lt;String&gt;**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getOptimizationList"></a>
# **getOptimizationList**
> List&lt;OptimizationTemplate&gt; getOptimizationList()

Gets the list of optimization tasks historical and current

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OptimizationApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

OptimizationApi apiInstance = new OptimizationApi();
try {
    List<OptimizationTemplate> result = apiInstance.getOptimizationList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OptimizationApi#getOptimizationList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;OptimizationTemplate&gt;**](OptimizationTemplate.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="newOptimizationRequest"></a>
# **newOptimizationRequest**
> String newOptimizationRequest(body)

New Optimization Request

Runs a new Optimization Request

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.OptimizationApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

OptimizationApi apiInstance = new OptimizationApi();
OptimizationRequest body = new OptimizationRequest(); // OptimizationRequest | Optimization Request
try {
    String result = apiInstance.newOptimizationRequest(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling OptimizationApi#newOptimizationRequest");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**OptimizationRequest**](OptimizationRequest.md)| Optimization Request |

### Return type

**String**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

