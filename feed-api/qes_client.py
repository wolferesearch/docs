
import requests
from urllib.parse import urljoin
import pandas as pd
import numpy as np

import urllib3
urllib3.disable_warnings()

class QesData:
    def __init__(self, data):
        self.data = data
        self.empty = len(data) == 0
        self.n_rows = len(data.get('$rows', []))
        self.df_data = {}

    def rows(self):
        return self.data.get('$rows')

    def _extract_section(self, section: dict):
        cols = section.get('$cols', [])
        vals = section.get('$vals', [])
        if not cols or not vals:
            return
        reshaped = np.array(vals).reshape(self.n_rows,len(cols))
        for i, col in enumerate(cols):
            self.df_data[col] = reshaped[:, i]

    def dates(self):
        return pd.to_datetime(self.rows())
        
    def as_time_series(self):
        if self.empty:
            return None

        num = self.data.get('$num')
        if num is None:
            return None
        
        # Create Series
        return pd.Series(data = num.get('$vals',[]), index = self.dates(), name = num.get('$cols')[0])
        
    def as_data_frame(self) -> pd.DataFrame:
        # Process numerical columns
        if '$num' in self.data:
            self._extract_section(self.data['$num'])

        # Process string columns
        if '$str' in self.data:
            self._extract_section(self.data['$str'])

        # Add date column
        df = pd.DataFrame(self.df_data)
        if '$rows' in self.data:
            df.insert(0, 'Id', self.rows())
        
        return df

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

    def get_security_data(self, productid: int,
                          item: str,
                          idtype: str, 
                          securityid: str,  
                          startdate: str, enddate: str):
        """
        GET /qes/product/{productid}/data/ts/{idtype}/{securityid}/{item}/{startdate}/{enddate}
        Get time series data for a security

        - idtype: Type of ID (e.g., 'QESID', 'CUSIP', 'SEDOL','TIC')
        - securityid: The ID of the security (e.g., 'AAPL US')
        - productid: The ID of the data package
        - item: The specific data item to retrieve (e.g., 'close', 'volume')
        - startdate: Start date for the data (format: YYYY-MM-DD)
        - enddate: End date for the data (format: YYYY-MM-DD)
        - Returns: JSON object with time series data for the security
        """
        path = f"/qes/product/{productid}/data/ts/{idtype}/{securityid}/{item}/{startdate}/{enddate}"
        return QesData(self.request("GET", path)).as_time_series()

        
    def get_cross_sectional_data(self, productid: int, dated: str):
        """
        GET /qes/data/cs/{productid}/{dated}
        Get cross-sectional data for a data package on a specific date.
            - productid: The ID of the data package
            - dated: The date for which to retrieve cross-sectional data (format: YYYY-MM-DD)
            - Returns: JSON object with cross-sectional data    
        """
        path = f"/qes/product/{productid}/data/cs/{dated}"
        return QesData(self.request("GET", path))
    
    def get_security_info(self, qesid: str):
        """
        GET /qes/security/{qesid}
        Get security information by QES ID
         - qesid: The QES ID of the security
         - Returns: JSON object with security information
        """
        path = f"/qes/security/{qesid}"
        return self.request("GET", path)
