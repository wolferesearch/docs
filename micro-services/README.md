# QES Luo as as Service (QLaaS)

## Introduction
QES team under the leadership of Yin Luo has built several tools over many years to help with the investment process. We have a built a convenient interface to consume this dataset using simple [RESTful Web API](https://en.wikipedia.org/wiki/Representational_state_transfer). This a completely cloud based service that allows clients to use the Risk Model and Optimization functionality without the need to install any infrastructure or library. Clients can use a simple web client from their favorite language to access these functionalities. 

## What we offer?

### Jan 2019
- Portfolio Upload and Management
  - Upload custom universes
  - Upload custom data series, e.g., alpha scores and other factors
- Customized Risk Model Generation with choice of factors/ risk models
  - Custom universe
  - Custom estimation universer
  - Custom set of factors including the ones uploaded using portfolio uploader
  - Control over risk horizon using half life parameters for variance and covariance relationship
  - Control over shrinkage of specific risk
- Portfolio Optimization
  - Long Only, Short Only or Long/Short Optimization
  - Support for Minimum Risk, Target Alpha and MVO
  - Transaction Cost, ADV Participation as constraints
  - Risk Targetting
  - 
  
## Who should use this?
The toolset is targeted to provide easy interface to risk and optimization analytics to incorporate in the investment process. The toolset can be used by desk quants and data science folks comfortable with programmable interface. 

## How to get started?
You can request for a username/password from you Wolfe QES Sales representative. The API credentials along with documentation will provide several use cases. We are actively adding new features and welcome feedback related to functionality and interface. 

## RESTful API
You can find the the API Documentation here. We have used Swagger API documentation tool that provides easy to use client interfaces for commonly used languages. In additional, we have added client interface for R. 
