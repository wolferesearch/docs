# QES Security Data API Documentation

## Overview

This API provides endpoints to access time series and cross-sectional security data managed under QES products. It allows users to:

* List available data packages
* Get metadata for a specific data package
* Fetch time series data for a given security, item, and date range
* Fetch cross-sectional data for a given product on a specific date

## Base URL

```
http://localhost:8080/qes
```

---

## Endpoints

### 1. List Data Packages

**GET** `/product`

Returns a list of all available data packages.

**Response Example:**

```json
["macro_factor", "alpha_model", "industry_scores"]
```

---

### 2. Get Data Package Details

**GET** `/product/{productid}`

Retrieves metadata for the given product.

**Path Parameters:**

* `productid`: ID of the data product (e.g., `macro_factor`)

**Response Example:**

```json
{
  "productId": "macro_factor",
  "name": "Sample Package macro_factor",
  "description": "Dummy description for macro_factor"
}
```

---

### 3. Get Time Series Data

**GET** `/data/ts/{securityid}/{item}/{startdate}/{enddate}`

Fetches time series data for a specified security ID and item, between `startdate` and `enddate`.

**Path Parameters:**

* `securityid`: ID of the security (e.g., `AAPL`)
* `item`: Data item to retrieve (e.g., `price`, `return`)
* `startdate`: Start date (YYYY-MM-DD)
* `enddate`: End date (YYYY-MM-DD)

**Response Example:**

```json
[
  {"date": "2023-01-01", "value": 100.0},
  {"date": "2023-01-02", "value": 105.0}
]
```

---

### 4. Get Cross-Sectional Data

**GET** `/data/cs/{productid}/{dated}`

Retrieves cross-sectional data for a given product on a specific date.

**Path Parameters:**

* `productid`: ID of the product (e.g., `alpha_model`)
* `dated`: The date for the cross-section (YYYY-MM-DD)

**Response Example:**

```json
[
  {"securityId": "AAPL", "value": 0.67},
  {"securityId": "MSFT", "value": 0.72}
]
```

---

## Status Codes

* `200 OK`: Request succeeded
* `400 Bad Request`: Invalid input
* `404 Not Found`: Resource not found

## Notes

* Dates must be in ISO format `YYYY-MM-DD`
* This is a demo API with dummy data for testing

## Future Enhancements

* OAuth2 based authentication
* Swagger UI integration
* Real data connectivity via services or database

---

For questions or support, contact the QES API team.

