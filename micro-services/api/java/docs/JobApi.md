# JobApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**getJobList**](JobApi.md#getJobList) | **GET** /job | Gets the list of applicable jobs


<a name="getJobList"></a>
# **getJobList**
> List&lt;JobModel&gt; getJobList()

Gets the list of applicable jobs

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.JobApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

JobApi apiInstance = new JobApi();
try {
    List<JobModel> result = apiInstance.getJobList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling JobApi#getJobList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;JobModel&gt;**](JobModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

