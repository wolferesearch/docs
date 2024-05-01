# RiskModelApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createRiskModel**](RiskModelApi.md#createRiskModel) | **POST** /risk-model | Creates New Risk Model
[**getRiskModelDateFiles**](RiskModelApi.md#getRiskModelDateFiles) | **GET** /risk-model/{uuid}/{date} | Gets risk model files listing
[**getRiskModelDateList**](RiskModelApi.md#getRiskModelDateList) | **GET** /risk-model/{uuid} | Gets risk model dates list
[**getRiskModelFile**](RiskModelApi.md#getRiskModelFile) | **GET** /risk-model/{uuid}/{date}/{file} | Download a risk model file
[**getRiskModelList**](RiskModelApi.md#getRiskModelList) | **GET** /risk-model | Gets the list of risk models historical and current


<a name="createRiskModel"></a>
# **createRiskModel**
> String createRiskModel(body)

Creates New Risk Model

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RiskModelApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

RiskModelApi apiInstance = new RiskModelApi();
RiskModelRequest body = new RiskModelRequest(); // RiskModelRequest | Risk Model Parameters
try {
    String result = apiInstance.createRiskModel(body);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RiskModelApi#createRiskModel");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RiskModelRequest**](RiskModelRequest.md)| Risk Model Parameters |

### Return type

**String**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

<a name="getRiskModelDateFiles"></a>
# **getRiskModelDateFiles**
> List&lt;String&gt; getRiskModelDateFiles(uuid, date)

Gets risk model files listing

Returns list of files available for risk model for a date

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RiskModelApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

RiskModelApi apiInstance = new RiskModelApi();
String uuid = "uuid_example"; // String | ID of the risk model
String date = "date_example"; // String | date of the risk model (yyyymmdd)
try {
    List<String> result = apiInstance.getRiskModelDateFiles(uuid, date);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RiskModelApi#getRiskModelDateFiles");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **String**| ID of the risk model |
 **date** | **String**| date of the risk model (yyyymmdd) |

### Return type

**List&lt;String&gt;**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getRiskModelDateList"></a>
# **getRiskModelDateList**
> List&lt;String&gt; getRiskModelDateList(uuid)

Gets risk model dates list

Returns dates for which risk model is available

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RiskModelApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

RiskModelApi apiInstance = new RiskModelApi();
String uuid = "uuid_example"; // String | ID of the risk model
try {
    List<String> result = apiInstance.getRiskModelDateList(uuid);
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RiskModelApi#getRiskModelDateList");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **String**| ID of the risk model |

### Return type

**List&lt;String&gt;**

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getRiskModelFile"></a>
# **getRiskModelFile**
> getRiskModelFile(uuid, date, file)

Download a risk model file

Download risk model CSV File

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RiskModelApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

RiskModelApi apiInstance = new RiskModelApi();
String uuid = "uuid_example"; // String | ID of the risk model
String date = "date_example"; // String | date of the risk model (yyyymmdd)
String file = "file_example"; // String | Risk model file
try {
    apiInstance.getRiskModelFile(uuid, date, file);
} catch (ApiException e) {
    System.err.println("Exception when calling RiskModelApi#getRiskModelFile");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **uuid** | **String**| ID of the risk model |
 **date** | **String**| date of the risk model (yyyymmdd) |
 **file** | **String**| Risk model file |

### Return type

null (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

<a name="getRiskModelList"></a>
# **getRiskModelList**
> List&lt;RiskModel&gt; getRiskModelList()

Gets the list of risk models historical and current

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.RiskModelApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

RiskModelApi apiInstance = new RiskModelApi();
try {
    List<RiskModel> result = apiInstance.getRiskModelList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling RiskModelApi#getRiskModelList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;RiskModel&gt;**](RiskModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

