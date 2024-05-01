# OptimizationRequest

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**portfolio** | **str** | Mnemonic of the portfolio to be optimized | [optional] 
**template** | **str** | One of the previously defined templates for risk | [optional] 
**start_date** | **str** | Start date (yyyy-mm-dd) | [optional] 
**end_date** | **str** | End date (yyyy-mm-dd) | [optional] 
**freq** | **str** | Frequency of risk model generation | [optional] 
**benchmark** | **str** | Benchmark for Tracking error optimization problem - Any of the standard universes and portfolios can be used - as benchmark. The caller should provide the benchmark - mnemonic, e.g., QES_EUROPE, QES_WORLD, SP500. System uses - the Float weighting as benchmark. | [optional] 
**transaction_cost** | **float** | Transaction cost  to consider in the optimization. - This is relevant for MVO optimization where transaction - cost is taken out from objective function. The transaction - cost is a quadratic function added based on value selected - For when the transaction_cost &#x3D; 1, about 1 median spread - is estimated as the cost when 7% of ADV is participated, - for when transaction_cost &#x3D; 5, 1 median spread cost is - estimated for when the participation is 3%. The per share - cost is linear and in objective function, the cost becomes - quadratic | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


