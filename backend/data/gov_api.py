import requests
import pandas as pd
import logging
from .config import Config

class GovApiFetcher:
    BASE_URL = "https://api.data.gov.in/resource/"
    # Resource ID for monthly state-wise power consumption (example ID, needs verification)
    RESOURCE_ID = "6fb45d2e-6887-434a-9a00-5c6210f0f46f" 

    def __init__(self):
        self.api_key = Config.GOV_API_KEY

    def fetch_monthly_data(self):
        """
        Fetches monthly state-wise power consumption from data.gov.in
        """
        if not self.api_key:
            logging.error("data.gov.in API Key not found in config")
            return None

        params = {
            "api-key": self.api_key,
            "format": "json",
            "resource_id": self.RESOURCE_ID,
            "limit": 1000
        }

        try:
            logging.info("Fetching monthly state-wise data from data.gov.in")
            response = requests.get(self.BASE_URL + self.RESOURCE_ID, params=params)
            response.raise_for_status()
            
            data = response.json()
            records = data.get('records', [])
            
            if not records:
                logging.warning("No records returned from data.gov.in")
                return None
                
            df = pd.DataFrame(records)
            # Standardizing columns - adjust based on actual API response schema
            logging.info(f"Successfully fetched {len(df)} monthly records")
            return df
            
        except Exception as e:
            logging.error(f"Error fetching data from data.gov.in: {str(e)}")
            return None
