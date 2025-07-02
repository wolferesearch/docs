from qes_client import QESClient

client = QESClient("qes_url","your_username", "your_password")

# List all data packages
products = client.get_products()

# Get details for a specific product
details = client.get_product_details(196)

# Get time series data for a security
ts_data = client.get_security_data("AAPL US", "TRAP", "2023-01-01", "2023-12-31")

# Get cross-sectional data for a product on a specific date
cs_data = client.get_cross_sectional_data("TRAP", "2023-12-31")

