
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

    def get_product_details(self, productid: str):
        """GET /qes/product/{productid} - Get details of a data package"""
        path = f"/qes/product/{productid}"
        return self.request("GET", path)

    def get_security_data(self, securityid: str, item: str, startdate: str, enddate: str):
        """
        GET /qes/data/ts/{securityid}/{item}/{startdate}/{enddate}
        Get time series data for a security
        """
        path = f"/qes/data/ts/{securityid}/{item}/{startdate}/{enddate}"
        return self.request("GET", path)

    def get_cross_sectional_data(self, productid: str, dated: str):
        """
        GET /qes/data/cs/{productid}/{dated}
        Get cross-sectional data for a data package on a specific date
        """
        path = f"/qes/data/cs/{productid}/{dated}"
        return self.request("GET", path)
