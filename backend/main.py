import os
import logging
from datetime import datetime
from data.scraper import MeritScraper
# If needed: from data.gov_api import GovApiFetcher
from data.cleaner import DataCleaner
from data.db import SupabaseManager
from models.prophet_model import ProphetModel
from models.arima_model import ArimaModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_pipeline(recalibrate=False):
    logger.info("Starting GridCast India Data Pipeline...")
    db = SupabaseManager()
    scraper = MeritScraper()
    cleaner = DataCleaner()
    
    try:
        raw_data = scraper.fetch_all_regions()
        cleaned_df = cleaner.process_merit_data(raw_data)
        db.upsert_demand_data(cleaned_df)
        
        if recalibrate:
            regions = ['NR', 'SR', 'ER', 'WR', 'NER']
            prophet_wrapper = ProphetModel()
            arima_wrapper = ArimaModel()
            for region in regions:
                train_df = db.get_regional_data(region, limit=90*24)
                if not train_df.empty:
                    prophet_wrapper.train(train_df, region)
                    arima_wrapper.train(train_df, region)
        logger.info("Pipeline completed successfully.")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run_pipeline(recalibrate=False)
