
# OptimizationTemplate

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**targetRisk** | [**BigDecimal**](BigDecimal.md) | Annualized Risk Target for optimization |  [optional]
**bound** | [**List&lt;BigDecimal&gt;**](BigDecimal.md) | Minimum and Maximum weight bound |  [optional]
**maxADVParticipation** | [**BigDecimal**](BigDecimal.md) | ADV Participation Ceiling (5% &#x3D;&#x3D; 0.05) |  [optional]
**maxTuronver** | [**BigDecimal**](BigDecimal.md) | Maximum turnover allowed |  [optional]
**grossWeight** | [**BigDecimal**](BigDecimal.md) | Total notional weight of the optimized basket |  [optional]
**netWeight** | [**BigDecimal**](BigDecimal.md) | Net weight of the optimized basket. For Long/Short neutral the Net weight should be 0 |  [optional]
**objective** | [**ObjectiveEnum**](#ObjectiveEnum) |  |  [optional]
**lambda** | [**BigDecimal**](BigDecimal.md) | Risk aversion parameter, only used when objective is set as MVO |  [optional]


<a name="ObjectiveEnum"></a>
## Enum: ObjectiveEnum
Name | Value
---- | -----
MAXALPHA | &quot;maxAlpha&quot;
MINRISK | &quot;minRisk&quot;
MVO | &quot;MVO&quot;



