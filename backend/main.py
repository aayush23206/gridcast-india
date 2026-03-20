import os
import logging
from datetime import datetime
from data.scraper import MeritScraper
from data.gov_api import GovApiFetcher
from data.cleaner import DataCleaner
from data.db import SupabaseManager
from models.prophet_model import ProphetModel
from models.arima_model import ArimaModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_pipeline(recalibrate=False):
    """
    Main orchestration function to scrape, clean, save, and optionally retrain.
    """
    logger.info("Starting GridCast India Data Pipeline...")
    
    db = SupabaseManager()
    scraper = MeritScraper()
    cleaner = DataCleaner()
    
    try:
        # 1. Scrape Live Data from MERIT
        logger.info("Scraping live data...")
        raw_data = scraper.fetch_all_regions()
        
        # 2. Clean and Format
        logger.info("Cleaning data...")
        cleaned_df = cleaner.process_merit_data(raw_data)
        
        # 3. Save to Supabase
        logger.info("Saving to Supabase...")
        db.upsert_demand_data(cleaned_df)
        
        # 4. Optional: Recalibrate Models
        if recalibrate:
            logger.info("Recalibrating models...")
            regions = ['NR', 'SR', 'ER', 'WR', 'NER']
            prophet_wrapper = ProphetModel()
            arima_wrapper = ArimaModel()
            
            for region in regions:
                # Fetch last 90 days for training
                train_df = db.get_regional_data(region, limit=90*24)
                if not train_df.empty:
                    prophet_wrapper.train(train_df, region)
                    arima_wrapper.train(train_df, region)
        
        logger.info("Pipeline completed successfully.")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    # If run directly, perform a standard update
    run_pipeline(recalibrate=False)
