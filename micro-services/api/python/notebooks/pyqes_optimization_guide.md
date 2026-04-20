# Optimization Service Documentation

## Overview

The pyqes Optimization Service provides a comprehensive Python API for portfolio optimization using the QES (Quantitative Equity Strategies) microservice platform. This service allows you to:

- Upload custom user data (alpha signals, constraints, benchmarks)
- Configure optimization parameters
- Run portfolio optimizations with various objective functions
- Retrieve and analyze optimization results

## Table of Contents

1. [Getting Started](#getting-started)
2. [Uploading User Data](#uploading-user-data)
3. [Setting Up Optimization Parameters](#setting-up-optimization-parameters)
4. [Running Optimization](#running-optimization)
5. [Retrieving Results](#retrieving-results)
6. [Complete Examples](#complete-examples)

---

## Getting Started

### Installation

The pyqes package can be installed directly from the GitHub repository:

```bash
pip install git+https://github.com/wolferesearch/docs.git#subdirectory=micro-services/api/python
```

#### Dependencies

The package requires the following dependencies (automatically installed):
- `requests` - for HTTP API calls
- `pandas` - for data manipulation
- `datetime` - for date/time handling

#### Alternative Installation

You can also clone the repository and install locally:

```bash
git clone https://github.com/wolferesearch/docs.git
cd docs/micro-services/api/python
pip install .
```

### Connection Setup

```python
from pyqes import micsvc

# Create a connection to the QES service
connection = micsvc.Connection(
    username='your_username',
    password='your_password'
)

# Get an optimizer instance
optimizer = connection.get_optimizer()
```

### Prerequisites

- Valid QES credentials
- A risk model (either custom or default template)
- User data in the correct format (CSV with `DATE`, an identifier column (`TICKER` or `SEDOL`), and metrics)

---

## Uploading User Data

User data contains your custom metrics such as alpha signals, benchmark weights, initial portfolios, and custom bounds. The data must be in a specific format for the optimizer to process it correctly.

### Data Format Requirements

Your data should be a pandas DataFrame with the following structure:

```
| DATE       | TICKER | Alpha    | Benchmark | InitPortfolio | LB    | UB    | ... |
|------------|--------|----------|-----------|---------------|-------|-------|-----|
| 2023-01-03 | AAPL   | 0.05     | 0.02      | 0.015         | -0.03 | 0.05  | ... |
| 2023-01-03 | MSFT   | 0.03     | 0.018     | 0.012         | -0.03 | 0.05  | ... |
| 2023-01-04 | AAPL   | 0.04     | 0.02      | 0.020         | -0.03 | 0.05  | ... |
| ...        | ...    | ...      | ...       | ...           | ...   | ...   | ... |
```

**Required Columns:**
- `DATE`: Date in YYYY-MM-DD format (uppercase)
- Identifier column: `TICKER` or `SEDOL` (uppercase — use a single identifier type consistently)

**Supported meta mnemonics** (per the service's OpenAPI spec — `swagger-generated/docs/MetaInput.md`):
- Identifiers: `TICKER`, `SEDOL`
- Meta/grouping factors: `CURRENCY`, `QES_GSECTOR`, `QES_GGROUP`, `QES_COUNTRY`

**Optional Columns** (depending on optimization type):
- `Alpha`: Alpha signal/forecast for the security
- `Benchmark`: Benchmark weight (for benchmark-relative optimization)
- `InitPortfolio`: Initial portfolio holdings
- `LB`, `UB`: Custom lower and upper bounds per security
- Any custom factors or grouping variables

### Method 1: Upload from DataFrame

```python
import pandas as pd

# Create or load your data
data = pd.DataFrame({
    'DATE': ['2023-01-03', '2023-01-03', '2023-01-04', '2023-01-04'],
    'TICKER': ['AAPL', 'MSFT', 'AAPL', 'MSFT'],
    'Alpha': [0.05, 0.03, 0.04, 0.035],
    'Benchmark': [0.02, 0.018, 0.02, 0.018],
    'MarketCap': [2500000, 2000000, 2520000, 2010000]
})

# Upload data directly from DataFrame
optimizer.set_user_data(
    name='my_alpha_data',
    data=data,
    overwrite=True  # Set to False to prevent overwriting existing data
)
```

### Method 2: Upload from CSV File

```python
# Using UserData class directly
user_data = connection.user_data()

# Upload from file path
user_data.upload_data(
    file_path_or_data='path/to/your/data.csv',
    name='my_alpha_data'
)
```

### Method 3: List and Manage Existing Data

```python
# Get UserData instance
user_data = connection.user_data()

# List all uploaded data
available_data = user_data.list_data()
print(available_data)

# Check if data exists
exists = user_data.exists('my_alpha_data')

# Delete data
user_data.delete_data('my_alpha_data')
```

### Important Notes on User Data

1. **Data Validation**: Ensure your data has no missing values for required columns
2. **Date Format**: Use YYYY-MM-DD format consistently
3. **Identifier Consistency**: Use the same identifier type throughout (e.g., all Tickers or all SEDOLs)
4. **Column Names**: Column names are case-sensitive and will be referenced in optimization parameters
5. **Encrypted Data**: If `LQUANT_MICSVC_ENCRYPTED=TRUE` environment variable is set, data will be encrypted using GPG

---

## Setting Up Optimization Parameters

The Optimizer class provides a fluent API with chainable setter methods for configuring optimization parameters.

### Essential Parameters

#### 1. Set Template (Optional but Recommended)

Templates provide default optimization configurations that can be customized.

```python
optimizer.set_template('default')
```

Available templates can be viewed via:
```python
templates = connection.optimization_templates()
print(templates)
```

#### 2. Set Objective Function

The optimizer supports three objective functions:

```python
# Mean-Variance Optimization (requires alpha and lambda)
optimizer.set_objective('MVO')

# Minimize Risk
optimizer.set_objective('minRisk')

# Maximize Alpha (requires alpha signal)
optimizer.set_objective('maxAlpha')
```

#### 3. Set Risk Model

Specify which risk model to use for covariance estimation:

```python
optimizer.set_risk_model('QES_US_AC_2')
```

**Common Risk Model Codes:**
- `QES_US_AC_2` - Default US equity risk model
- Contact your QES administrator for other available risk models

#### 4. Configure User Data Reference

After uploading user data, reference it in the optimizer:

```python
# This is done automatically by set_user_data() method
# But can be set manually as well
optimizer.req['user_data'] = {
    'format': 'csv',
    'name': 'my_alpha_data'
}
```

### Alpha and Signal Parameters

#### Set Alpha Signal

Specify which column in your user data contains the alpha forecast:

```python
optimizer.set_alpha('Alpha')  # Column name from your uploaded data
```

#### Set Lambda (Risk Aversion) for MVO

For Mean-Variance Optimization, lambda controls the trade-off between return and risk:

```python
optimizer.set_lambda(2.0)  # Higher values = more risk-averse
```

**Lambda Guidelines:**
- Typical range: 0.5 to 10
- Higher lambda = lower risk, lower expected return
- Lower lambda = higher risk, higher expected return

### Weight Bounds and Constraints

#### 1. Set Global Weight Bounds

```python
# Set bounds for all securities
optimizer.set_bounds(
    lb=-0.02,  # -2% minimum weight (short)
    ub=0.05    # 5% maximum weight (long)
)
```

#### 2. Set Relative Bounds (vs. Benchmark)

```python
# Set benchmark column
optimizer.set_benchmark('Benchmark')

# Set relative bounds
optimizer.set_relative_bounds(
    lb=-0.01,  # Max 1% underweight vs benchmark
    ub=0.01    # Max 1% overweight vs benchmark
)
```

#### 3. Stock-Specific Bounds from Data

Use custom bounds from uploaded data columns:

```python
optimizer.add_stock_bounds(
    lb='LB',        # Column name for lower bounds
    ub='UB',        # Column name for upper bounds
    benchmark=False # True if bounds are relative to benchmark
)
```

### Portfolio Constraints

#### Long/Short Exposure

```python
# Long side constraints
optimizer.set_min_long_weight(0.9)   # At least 90% long
optimizer.set_max_long_weight(1.1)   # At most 110% long

# Short side constraints
optimizer.set_min_short_weight(0.9)  # At least 90% short
optimizer.set_max_short_weight(1.1)  # At most 110% short
```

#### Turnover Constraints

```python
# Maximum turnover per rebalance (as fraction)
optimizer.set_max_turnover(0.5)  # 50% maximum turnover

# Soft turnover penalty (adds to objective)
optimizer.set_soft_turnover_penalty(0.1)
```

#### Number of Securities

```python
# Limit portfolio size
optimizer.set_max_number_securities(50)
optimizer.set_min_number_securities(20)
```

#### Minimum Holding Weight

Prevent very small positions:

```python
optimizer.set_min_holding(0.005)  # Minimum 0.5% (50 bps) per position
```

### Risk Constraints

#### Target Risk

```python
# Set maximum portfolio risk (annualized, in decimal)
optimizer.set_target_risk(0.15)  # 15% max risk
```

#### Use Absolute Risk vs Tracking Error

```python
# Use absolute risk instead of tracking error
optimizer.set_abs_risk()
```

### Factor Constraints

#### 1. Risk Factor Neutralization

Control exposure to risk model factors:

```python
optimizer.set_risk_neutralization_factors(
    neutralization_factors=['Size', 'Momentum', 'Value'],
    factor_min_exposure=-0.1,
    factor_max_exposure=0.1
)
```

#### 2. Absolute Factor Neutralization

```python
optimizer.set_risk_neutralization_factors_abs(
    neutralization_factors=['Size', 'Beta'],
    factor_max_exposure=0.05
)
```

#### 3. Custom Factor Neutralization Matrix

For more complex factor constraints with groupings:

```python
optimizer.add_neutralization_matrix(
    neutralization_factors=['CustomFactor1', 'CustomFactor2'],
    factor_min_exposure=-0.05,
    factor_max_exposure=0.05,
    grouping_matrix='Sector',  # Apply constraints per sector
    benchmark=True
)
```

### Group Constraints

Control exposure by sectors, industries, or custom groups:

```python
# GICS Sector constraints
optimizer.add_group_constraint(
    grouping_factor='GICS1',      # GICS Level 1 (Sector)
    min_exposure=-0.05,
    max_exposure=0.05,
    benchmark=True,               # Relative to benchmark
    transformation=None
)

# Market cap bucket constraints with transformation
optimizer.add_group_constraint(
    grouping_factor='MarketCap',
    min_exposure=0.0,
    max_exposure=0.4,
    benchmark=False,
    transformation={
        'transformer': 'binner',
        'bins': [0, 1000, 10000, 100000]  # Market cap bins in millions
    }
)
```

### ADV (Average Daily Volume) Constraints

Limit trading and holdings based on liquidity:

```python
# Enable ADV usage
optimizer.set_use_adv(True)

# Set ADV factor from QES library
optimizer.set_adv_factor('ADV_20D')

# Trading constraints
optimizer.set_max_ADV_trading_participation(0.10)    # Max 10% of ADV traded
optimizer.set_soft_ADV_trading_penalty(1000.0)       # Penalty for violation

# Holding constraints
optimizer.set_max_ADV_holding_participation(0.05)    # Max 5% of ADV held

# Set notional for ADV calculations
optimizer.set_notional(
    init_notional_value=10000000,    # $10M initial
    notional_value=10000000          # $10M target
)
```

### Transaction Costs

#### Fixed Transaction Cost

```python
# Fixed cost as fraction of turnover
optimizer.set_transaction_cost(0.0005)  # 5 basis points
```

#### Transaction Cost Model

Use a sophisticated transaction cost model:

```python
optimizer.set_use_tcm(True)
optimizer.set_transaction_cost_model('QES_TCM_V1')
```

### Initial Portfolio

Set the starting portfolio for rebalancing:

```python
optimizer.set_init_portfolio('InitPortfolio')  # Column name in user data
```

### Hard-to-Borrow (HTB) Threshold

Exclude securities that are difficult to short:

```python
# Threshold from 2-10 (higher = include harder-to-borrow)
optimizer.set_htb_threshold(7.0)
```

### Implied Alpha Mode

Use implied alpha from benchmark:

```python
optimizer.set_implied_alpha(True)
```

---

## Running Optimization

### Submit and Wait

After configuring all parameters, submit the optimization job:

```python
# Submit the optimization
optimizer.submit()

# Wait for completion (max 300 seconds)
info = optimizer.wait(max_wait_secs=300)

# Check status
status = optimizer.status()
print(f"Optimization status: {status}")

if status == 'SUCCESS':
    results = optimizer.get_results()
else:
    # Get logs to debug
    logs = optimizer.get_logs()
    print(logs)
```

### Check Job Status

```python
# Get detailed job info
info = optimizer.info()
print(info)

# List all completed optimizations
completed_jobs = optimizer.completed()

# List failed optimizations
failed_jobs = optimizer.failed()
```

### Attach to Existing Job

```python
# Set UUID of previously run optimization
optimizer.set_id('uuid-string-here')

# Or attach to most recent job
optimizer.set_latest(k=0)  # 0 = most recent, 1 = second most recent, etc.
```

---

## Retrieving Results

The `OptimizerResult` class provides methods to access optimization outputs:

```python
# Get results
results = optimizer.get_results()
```

### Available Result Methods

#### 1. Optimized Weights

```python
# Get optimized portfolio weights (matrix: securities × dates)
weights = results.get_weights()
print(weights)
```

#### 2. Portfolio Metrics

```python
# Ex-ante risk
risk = results.get_risk()

# Ex-ante alpha
alpha = results.get_alpha()

# Notional value
notional = results.get_notional_value()

# Tracking error (if benchmark is set)
tracking_error = results.get_tracking_error()
```

#### 3. Turnover Metrics

```python
# Realized turnover
turnover = results.get_turnover()

# Required turnover (minimum needed)
required_turnover = results.get_required_turnover()
```

#### 4. Old Portfolio Weights

```python
# Previous portfolio weights
old_weights = results.get_old_weights()
old_notional = results.get_old_notional_value()
```

#### 5. Optimization Status

```python
# Solver status for each date
opt_status = results.get_opt_status()
```

#### 6. Get Portfolio for Specific Date

Combine weights with user data for a specific date:

```python
portfolio = results.get_portfolio('2023-01-03')
print(portfolio)
# Returns DataFrame with user data + WEIGHT column
```

#### 7. Security Mapping

```python
# Get identifier mapping
mapping = results.sym_mapping()
```

---

## Complete Examples

### Example 1: Basic Mean-Variance Optimization

```python
import pandas as pd
from pyqes import micsvc

# Connect
conn = micsvc.Connection('username', 'password')
optimizer = conn.get_optimizer()

# Prepare data
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']  # use real identifiers the risk model recognizes
data = pd.DataFrame({
    'DATE': ['2023-01-03']*len(tickers) + ['2023-01-04']*len(tickers),
    'TICKER': tickers * 2,
    'Alpha': [0.01, 0.02, 0.015, 0.025, 0.018] * 2,
    'Benchmark': [1.0 / len(tickers)] * (2 * len(tickers)),
})

# Upload data and configure
optimizer.set_user_data('my_strategy', data, overwrite=True)
optimizer.set_template('default')
optimizer.set_objective('MVO')
optimizer.set_alpha('Alpha')
optimizer.set_lambda(2.5)
optimizer.set_risk_model('QES_US_AC_2')
optimizer.set_benchmark('Benchmark')
optimizer.set_bounds(lb=-0.03, ub=0.03)
optimizer.set_target_risk(0.12)
optimizer.set_max_turnover(0.4)

# Submit and wait
optimizer.submit()
optimizer.wait(max_wait_secs=300)

# Get results
if optimizer.status() == 'SUCCESS':
    results = optimizer.get_results()
    weights = results.get_weights()
    risk = results.get_risk()
    alpha = results.get_alpha()

    print("Optimized Weights:\n", weights)
    print("\nEx-ante Risk:", risk)
    print("Ex-ante Alpha:", alpha)
```

### Example 2: Minimize Risk with Sector Constraints

```python
# Configure optimizer
optimizer.set_user_data('risk_parity_data', data, overwrite=True)
optimizer.set_objective('minRisk')
optimizer.set_risk_model('QES_US_AC_2')
optimizer.set_bounds(lb=0, ub=0.1)  # Long-only

# Add sector constraints
optimizer.add_group_constraint(
    grouping_factor='GICS1',
    min_exposure=0.0,
    max_exposure=0.25,  # Max 25% per sector
    benchmark=False
)

# Neutralize style factors
optimizer.set_risk_neutralization_factors(
    neutralization_factors=['Size', 'Value', 'Momentum'],
    factor_min_exposure=-0.05,
    factor_max_exposure=0.05
)

optimizer.set_max_number_securities(40)
optimizer.set_min_holding(0.01)

# Run
optimizer.submit()
optimizer.wait(max_wait_secs=300)
results = optimizer.get_results()
```

### Example 3: ADV-Constrained Optimization with Transaction Costs

```python
# Configure with liquidity constraints
optimizer.set_user_data('large_portfolio', data, overwrite=True)
optimizer.set_objective('maxAlpha')
optimizer.set_alpha('Alpha')
optimizer.set_risk_model('QES_US_AC_2')

# ADV constraints
optimizer.set_use_adv(True)
optimizer.set_adv_factor('ADV_20D')
optimizer.set_max_ADV_trading_participation(0.15)
optimizer.set_max_ADV_holding_participation(0.10)
optimizer.set_notional(init_notional_value=50000000, notional_value=50000000)

# Transaction costs
optimizer.set_use_tcm(True)
optimizer.set_transaction_cost_model('QES_TCM_V1')

# Set initial portfolio
optimizer.set_init_portfolio('CurrentHoldings')

# Turnover limit
optimizer.set_max_turnover(0.3)

# Run
optimizer.submit()
optimizer.wait(max_wait_secs=300)
results = optimizer.get_results()
```

---

## API Reference Summary

### Optimizer Class Methods

**Configuration Methods:**
- `set_template(template)` - Set optimization template
- `set_objective(objective)` - Set objective: 'MVO', 'minRisk', 'maxAlpha'
- `set_risk_model(risk_model)` - Set risk model ID
- `set_alpha(alpha)` - Set alpha column name
- `set_lambda(_lambda)` - Set risk aversion parameter
- `set_benchmark(benchmark)` - Set benchmark column name

**Bounds and Constraints:**
- `set_bounds(lb, ub)` - Set global weight bounds
- `set_relative_bounds(lb, ub)` - Set benchmark-relative bounds
- `add_stock_bounds(lb, ub, benchmark)` - Set stock-specific bounds
- `set_min_holding(min_holding)` - Set minimum position size

**Exposure Constraints:**
- `set_min_long_weight(min_long)` - Set minimum long exposure
- `set_max_long_weight(max_long)` - Set maximum long exposure
- `set_min_short_weight(min_short)` - Set minimum short exposure
- `set_max_short_weight(max_short)` - Set maximum short exposure

**Group Constraints:**
- `add_group_constraint(grouping_factor, min_exposure, max_exposure, benchmark, transformation)` - Add sector/group constraints

**Factor Constraints:**
- `set_risk_neutralization_factors(factors, min, max)` - Neutralize risk factors
- `set_risk_neutralization_factors_abs(factors, max)` - Absolute factor neutralization
- `add_neutralization_matrix(factors, min, max, grouping, benchmark)` - Custom factor matrix

**Risk Constraints:**
- `set_target_risk(target_risk)` - Set maximum risk
- `set_abs_risk()` - Use absolute risk instead of tracking error

**Turnover Constraints:**
- `set_max_turnover(turnover)` - Set maximum turnover
- `set_soft_turnover_penalty(penalty)` - Add turnover penalty to objective

**Portfolio Size:**
- `set_max_number_securities(max_securities)` - Maximum number of positions
- `set_min_number_securities(min_securities)` - Minimum number of positions

**ADV Constraints:**
- `set_use_adv(use_adv)` - Enable ADV constraints
- `set_adv_factor(adv_factor)` - Set ADV factor name
- `set_max_ADV_trading_participation(max_part)` - Max trading vs ADV
- `set_max_ADV_holding_participation(max_part)` - Max holding vs ADV
- `set_notional(init_notional, notional)` - Set portfolio notional

**Transaction Costs:**
- `set_transaction_cost(cost)` - Set fixed transaction cost
- `set_use_tcm(use_tcm)` - Enable transaction cost model
- `set_transaction_cost_model(model)` - Set TCM model ID

**Other Parameters:**
- `set_init_portfolio(init_portfolio)` - Set initial portfolio column
- `set_htb_threshold(threshold)` - Set hard-to-borrow threshold
- `set_implied_alpha(implied_alpha)` - Use implied alpha

**Execution Methods:**
- `submit()` - Submit optimization job
- `wait(max_wait_secs)` - Wait for completion
- `status()` - Get job status
- `info()` - Get job information
- `get_logs()` - Get execution logs
- `get_results()` - Get OptimizerResult object

**Job Management:**
- `set_id(uuid)` - Attach to existing job by UUID
- `set_latest(k)` - Attach to k-th most recent job
- `completed()` - List completed jobs
- `failed()` - List failed jobs

### OptimizerResult Class Methods

- `get_weights()` - Get optimized weights matrix
- `get_risk()` - Get ex-ante risk time series
- `get_alpha()` - Get ex-ante alpha time series
- `get_tracking_error()` - Get tracking error (if benchmark set)
- `get_turnover()` - Get realized turnover
- `get_required_turnover()` - Get required turnover
- `get_notional_value()` - Get notional value
- `get_old_weights()` - Get previous weights
- `get_old_notional_value()` - Get previous notional
- `get_opt_status()` - Get optimization solver status
- `get_portfolio(dated)` - Get portfolio for specific date
- `sym_mapping()` - Get security identifier mapping

### UserData Class Methods

- `upload_data(file_path_or_data, name)` - Upload data from file or DataFrame
- `list_data()` - List all uploaded datasets
- `exists(name)` - Check if dataset exists
- `delete_data(name)` - Delete dataset

---

## Best Practices

1. **Start Simple**: Begin with basic constraints and gradually add complexity
2. **Validate Data**: Always check your uploaded data format before running optimization
3. **Monitor Logs**: If optimization fails, check logs with `optimizer.get_logs()`
4. **Test Parameters**: Use short date ranges first to validate your configuration
5. **Use Templates**: Leverage existing templates and modify them rather than starting from scratch
6. **Set Realistic Bounds**: Ensure your constraints are feasible (not too restrictive)
7. **Consider Liquidity**: Always include ADV constraints for realistic portfolios
8. **Transaction Costs**: Include transaction costs for more realistic optimization
9. **Save Configurations**: Once you have a working configuration, save it as a template

---

## Troubleshooting

### Common Issues

**Issue**: Optimization fails with "Infeasible problem"
- **Solution**: Check that your constraints are not contradictory. Relax bounds or turnover limits.

**Issue**: "User data not found"
- **Solution**: Ensure data is uploaded before referencing it. Check the name matches exactly.

**Issue**: "Column not found in user data"
- **Solution**: Verify column names in your uploaded data match the ones referenced in parameters.

**Issue**: Very long optimization time
- **Solution**: Reduce the number of securities, simplify constraints, or increase turnover limits.

**Issue**: Empty results
- **Solution**: Check that dates in user data match the rebalancing schedule.

---

## Support

For additional support or questions:
- Contact: luo.qes@wolferesearch.com
- Review the complete API code: `pyqes/micsvc.py`

---

**Document Version**: 1.0
**Last Updated**: 2025
**API Version**: pyqes.micsvc v2
