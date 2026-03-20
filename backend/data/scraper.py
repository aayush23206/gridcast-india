import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import time

# Logging Configuration
logging.basicConfig(
    filename='scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class MeritIndiaScraper:
    BASE_URL = "https://merit.posoco.gov.in/Home/GraphData"
    
    REGIONS = {
        "NR": "Northern",
        "SR": "Southern",
        "ER": "Eastern",
        "WR": "Western",
        "NER": "North-Eastern"
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

    def fetch_data(self, region_code, start_date, end_date, retries=3):
        """
        Fetches hourly demand data for a given region and date range.
        Format of response is expected to be JSON/CSV from MERIT India.
        """
        if region_code not in self.REGIONS:
            logging.error(f"Invalid region code: {region_code}")
            return None

        params = {
            "region": region_code,
            "startDate": start_date,
            "endDate": end_date
        }

        for attempt in range(retries):
            try:
                logging.info(f"Fetching data for {region_code} from {start_date} to {end_date} (Attempt {attempt+1})")
                response = self.session.get(self.BASE_URL, params=params, timeout=15)
                response.raise_for_status()
                
                # MERIT India typically returns a list of dictionaries with 'datetime' and 'demand'
                data = response.json()
                if not data:
                    logging.warning(f"No data returned for {region_code}")
                    return None
                
                df = pd.DataFrame(data)
                
                # Standardizing columns
                # Note: Actual keys from MERIT might be 'time' or 'value', adjusting as per usual patterns
                df['region'] = region_code
                df.rename(columns={'time': 'datetime', 'value': 'demand_mw'}, inplace=True)
                
                logging.info(f"Successfully fetched {len(df)} records for {region_code}")
                return df
            
            except Exception as e:
                logging.error(f"Error fetching data for {region_code}: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return None

if __name__ == "__main__":
    scraper = MeritIndiaScraper()
    # Example call
    # res = scraper.fetch_data("NR", "2024-01-01", "2024-01-02")
    # if res is not None:
    #     print(res.head())
