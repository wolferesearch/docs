
import requests
from urllib.parse import urljoin

class APIClient:
    def __init__(self, url, username, password):
        self.auth = (username, password)
        self.base_url = url  # Replace with actual base URL if different
        self.session = requests.Session()
        self.session.auth = self.auth
        self.session.verify = False  # Disable SSL verification

    def request(self, method, path, **kwargs):
        url = urljoin(self.base_url, path)
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

class QESClient(APIClient):
    def get_products(self):
        """GET /qes/product - List all data packages"""
        return self.request("GET", "/qes/product")

    def get_product_details(self, productid: int):
        """GET /qes/product/{productid} - Get details of a data package"""
        path = f"/qes/product/{productid}"
        return self.request("GET", path)

    def get_security_data(self, idtype: str, 
                          securityid: str, 
                          productid: int, 
                          item: str, startdate: str, enddate: str):
        """
        GET /qes/data/ts/{securityid}/{item}/{startdate}/{enddate}
        Get time series data for a security

        - idtype: Type of ID (e.g., 'QESID', 'CUSIP', 'SEDOL','TIC')
        - securityid: The ID of the security (e.g., 'AAPL US')
        - productid: The ID of the data package
        - item: The specific data item to retrieve (e.g., 'close', 'volume')
        - startdate: Start date for the data (format: YYYY-MM-DD)
        - enddate: End date for the data (format: YYYY-MM-DD)
        - Returns: JSON object with time series data for the security
        """
        path = f"/qes/data/ts/{idtype}/{securityid}/{productid}/{item}/{startdate}/{enddate}"
        return self.request("GET", path)

    def get_cross_sectional_data(self, productid: int, dated: str):
        """
        GET /qes/data/cs/{productid}/{dated}
        Get cross-sectional data for a data package on a specific date.
            - productid: The ID of the data package
            - dated: The date for which to retrieve cross-sectional data (format: YYYY-MM-DD)
            - Returns: JSON object with cross-sectional data    
        """
        path = f"/qes/data/cs/{productid}/{dated}"
        return self.request("GET", path)
    
    def get_security_info(self, qesid: str):
        """
        GET /qes/security/{qesid}
        Get security information by QES ID
         - qesid: The QES ID of the security
         - Returns: JSON object with security information
        """
        path = f"/qes/security/{qesid}"
        return self.request("GET", path)
