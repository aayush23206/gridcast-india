import pandas as pd
from prophet import Prophet
import joblib
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProphetModel:
    def __init__(self, model_dir="backend/models/saved"):
        self.model_dir = model_dir
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    def train(self, df, region):
        """
        Trains a Prophet model for a specific region.
        df: DataFrame with 'ds' (datetime) and 'y' (value) columns.
        """
        logger.info(f"Training Prophet model for region: {region}")
        
        # Initialize Prophet with specialized settings for energy data
        model = Prophet(
            yearly_seasonality=True,
            weekly_seasonality=True,
            daily_seasonality=True,
            changepoint_prior_scale=0.05,
            seasonality_mode='multiplicative'
        )
        
        # Add Indian holidays if possible (optional enhancement)
        # model.add_country_holidays(country_name='IN')
        
        model.fit(df)
        
        # Save the model
        model_path = os.path.join(self.model_dir, f"prophet_{region}.joblib")
        joblib.dump(model, model_path)
        logger.info(f"Model saved to {model_path}")
        return model

    def predict(self, region, horizon_days=7):
        """
        Generates forecast for a specified horizon.
        """
        model_path = os.path.join(self.model_dir, f"prophet_{region}.joblib")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No trained model found for region: {region}")
        
        model = joblib.load(model_path)
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=horizon_days * 24, freq='H')
        forecast = model.predict(future)
        
        # Return only the relevant columns and future dates
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

if __name__ == "__main__":
    # Quick test logic
    import numpy as np
    dates = pd.date_range(start='2024-01-01', periods=1000, freq='H')
    y = 100000 + np.sin(np.arange(1000) * 2 * np.pi / 24) * 20000 + np.random.normal(0, 1000, 1000)
    test_df = pd.DataFrame({'ds': dates, 'y': y})
    
    pm = ProphetModel()
    pm.train(test_df, "TEST")
    fcst = pm.predict("TEST", 7)
    print(fcst.tail())
