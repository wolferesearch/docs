# CatalogApi

All URIs are relative to *https://feed.luoquant.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**createOptimizationTemplate**](CatalogApi.md#createOptimizationTemplate) | **POST** /template/optimization | Creates new optimization template
[**createPortfolio**](CatalogApi.md#createPortfolio) | **POST** /portfolio | Creates / Updates Portoflio
[**createRiskModelTemplate**](CatalogApi.md#createRiskModelTemplate) | **POST** /template/risk-model | Creates / Updates Risk Model Template based on ...
[**getFactorList**](CatalogApi.md#getFactorList) | **GET** /factor | Gets the list of applicable factors
[**getMetaList**](CatalogApi.md#getMetaList) | **GET** /meta | Gets the list of applicable meta fields
[**getPortfolioList**](CatalogApi.md#getPortfolioList) | **GET** /portfolio | Gets the list of applicable portfolios
[**getTemplateList**](CatalogApi.md#getTemplateList) | **GET** /template | Gets the list of appicable templates
[**getUniverseList**](CatalogApi.md#getUniverseList) | **GET** /universe | Gets the list of applicable universes


<a name="createOptimizationTemplate"></a>
# **createOptimizationTemplate**
> createOptimizationTemplate(body)

Creates new optimization template

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
TemplateModel body = new TemplateModel(); // TemplateModel | Optimization Template
try {
    apiInstance.createOptimizationTemplate(body);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#createOptimizationTemplate");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TemplateModel**](TemplateModel.md)| Optimization Template |

### Return type

null (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createPortfolio"></a>
# **createPortfolio**
> createPortfolio(body)

Creates / Updates Portoflio

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
RiskModelTemplate body = new RiskModelTemplate(); // RiskModelTemplate | Risk Model Template
try {
    apiInstance.createPortfolio(body);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#createPortfolio");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**RiskModelTemplate**](RiskModelTemplate.md)| Risk Model Template |

### Return type

null (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="createRiskModelTemplate"></a>
# **createRiskModelTemplate**
> createRiskModelTemplate(body)

Creates / Updates Risk Model Template based on ...

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
TemplateModel body = new TemplateModel(); // TemplateModel | Risk Model Template
try {
    apiInstance.createRiskModelTemplate(body);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#createRiskModelTemplate");
    e.printStackTrace();
}
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **body** | [**TemplateModel**](TemplateModel.md)| Risk Model Template |

### Return type

null (empty response body)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

<a name="getFactorList"></a>
# **getFactorList**
> List&lt;FactorModel&gt; getFactorList()

Gets the list of applicable factors

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
try {
    List<FactorModel> result = apiInstance.getFactorList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#getFactorList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;FactorModel&gt;**](FactorModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="getMetaList"></a>
# **getMetaList**
> List&lt;MetaModel&gt; getMetaList()

Gets the list of applicable meta fields

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
try {
    List<MetaModel> result = apiInstance.getMetaList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#getMetaList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;MetaModel&gt;**](MetaModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="getPortfolioList"></a>
# **getPortfolioList**
> List&lt;PortfolioModel&gt; getPortfolioList()

Gets the list of applicable portfolios

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
try {
    List<PortfolioModel> result = apiInstance.getPortfolioList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#getPortfolioList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;PortfolioModel&gt;**](PortfolioModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="getTemplateList"></a>
# **getTemplateList**
> List&lt;TemplateModel&gt; getTemplateList()

Gets the list of appicable templates

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
try {
    List<TemplateModel> result = apiInstance.getTemplateList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#getTemplateList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;TemplateModel&gt;**](TemplateModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

<a name="getUniverseList"></a>
# **getUniverseList**
> List&lt;UniverseModel&gt; getUniverseList()

Gets the list of applicable universes

### Example
```java
// Import classes:
//import io.swagger.client.ApiClient;
//import io.swagger.client.ApiException;
//import io.swagger.client.Configuration;
//import io.swagger.client.auth.*;
//import io.swagger.client.api.CatalogApi;

ApiClient defaultClient = Configuration.getDefaultApiClient();

// Configure HTTP basic authorization: basicAuth
HttpBasicAuth basicAuth = (HttpBasicAuth) defaultClient.getAuthentication("basicAuth");
basicAuth.setUsername("YOUR USERNAME");
basicAuth.setPassword("YOUR PASSWORD");

CatalogApi apiInstance = new CatalogApi();
try {
    List<UniverseModel> result = apiInstance.getUniverseList();
    System.out.println(result);
} catch (ApiException e) {
    System.err.println("Exception when calling CatalogApi#getUniverseList");
    e.printStackTrace();
}
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**List&lt;UniverseModel&gt;**](UniverseModel.md)

### Authorization

[basicAuth](../README.md#basicAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

