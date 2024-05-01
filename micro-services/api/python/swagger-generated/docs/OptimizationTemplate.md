# OptimizationTemplate

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**target_risk** | **float** | Annualized Risk Target for optimization | [optional] 
**bound** | **list[float]** | Minimum and Maximum weight bound | [optional] 
**max_adv_participation** | **float** | ADV Participation Ceiling (5% &#x3D;&#x3D; 0.05) | [optional] 
**max_turonver** | **float** | Maximum turnover allowed | [optional] 
**gross_weight** | **float** | Total notional weight of the optimized basket | [optional] 
**net_weight** | **float** | Net weight of the optimized basket. For Long/Short neutral the Net weight should be 0 | [optional] 
**objective** | **str** |  | [optional] 
**_lambda** | **float** | Risk aversion parameter, only used when objective is set as MVO | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


