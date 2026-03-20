import requests
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class MeritScraper:
    def __init__(self):
        self.base_url = "https://merit.posoco.gov.in/api/order_delta" # Example endpoint

    def fetch_region_data(self, region_code):
        logger.info(f"Fetching merit order data for {region_code}")
        # Simplified: using mock data that follows the structure expected
        return {
            "region": region_code,
            "demand": 25000 + (pd.Timestamp.now().hour * 1000),
            "timestamp": datetime.now().isoformat()
        }

    def fetch_all_regions(self):
        regions = ['NR', 'SR', 'ER', 'WR', 'NER']
        results = []
        for r in regions:
            results.append(self.fetch_region_data(r))
        return results
