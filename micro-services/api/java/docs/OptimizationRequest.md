
# OptimizationRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**portfolio** | **String** | Mnemonic of the portfolio to be optimized |  [optional]
**template** | **String** | One of the previously defined templates for risk |  [optional]
**startDate** | **String** | Start date (yyyy-mm-dd) |  [optional]
**endDate** | **String** | End date (yyyy-mm-dd) |  [optional]
**freq** | [**FreqEnum**](#FreqEnum) | Frequency of risk model generation |  [optional]
**benchmark** | [**BenchmarkEnum**](#BenchmarkEnum) | Benchmark for Tracking error optimization problem - Any of the standard universes and portfolios can be used - as benchmark. The caller should provide the benchmark - mnemonic, e.g., QES_EUROPE, QES_WORLD, SP500. System uses - the Float weighting as benchmark. |  [optional]
**transactionCost** | [**BigDecimal**](BigDecimal.md) | Transaction cost  to consider in the optimization. - This is relevant for MVO optimization where transaction - cost is taken out from objective function. The transaction - cost is a quadratic function added based on value selected - For when the transaction_cost &#x3D; 1, about 1 median spread - is estimated as the cost when 7% of ADV is participated, - for when transaction_cost &#x3D; 5, 1 median spread cost is - estimated for when the participation is 3%. The per share - cost is linear and in objective function, the cost becomes - quadratic |  [optional]


<a name="FreqEnum"></a>
## Enum: FreqEnum
Name | Value
---- | -----
_1ME | &quot;1me&quot;
_1M | &quot;1m&quot;
_1D | &quot;1d&quot;


<a name="BenchmarkEnum"></a>
## Enum: BenchmarkEnum
Name | Value
---- | -----
QES_EUROPE | &quot;QES_EUROPE&quot;
QES_WORLD | &quot;QES_WORLD&quot;
SP500 | &quot;SP500&quot;



