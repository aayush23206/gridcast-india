import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import joblib
import os
import logging
import warnings

# Suppress convergence warnings for cleaner logs
warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArimaModel:
    def __init__(self, model_dir="backend/models/saved"):
        self.model_dir = model_dir
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)

    def train(self, df, region):
        """
        Trains a SARIMAX model for a specific region.
        df: DataFrame with 'ds' as index and 'y' column.
        """
        logger.info(f"Training ARIMA (SARIMAX) model for region: {region}")
        
        # Ensure 'ds' is the index and has a frequency
        if 'ds' in df.columns:
            df = df.set_index('ds')
        
        df = df.asfreq('H')
        df['y'] = df['y'].interpolate(method='linear')

        # SARIMA parameters (p,d,q) x (P,D,Q,s)
        # Simplified for speed; usually optimized via grid search
        # Note: Energy data has strong 24h seasonality
        order = (1, 1, 1)
        seasonal_order = (1, 0, 1, 24) 

        model = SARIMAX(df['y'], 
                        order=order, 
                        seasonal_order=seasonal_order,
                        enforce_stationarity=False,
                        enforce_invertibility=False)
        
        results = model.fit(disp=False)
        
        # Save the results object
        model_path = os.path.join(self.model_dir, f"arima_{region}.joblib")
        joblib.dump(results, model_path)
        logger.info(f"ARIMA model saved to {model_path}")
        return results

    def predict(self, region, horizon_days=7):
        """
        Generates forecast for a specified horizon.
        """
        model_path = os.path.join(self.model_dir, f"arima_{region}.joblib")
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"No trained model found for region: {region}")
        
        results = joblib.load(model_path)
        
        # Forecast
        steps = horizon_days * 24
        forecast_res = results.get_forecast(steps=steps)
        
        forecast_df = forecast_res.summary_frame()
        # Rename columns to match Prophet style for easy frontend consumption
        forecast_df = forecast_df.reset_index()
        forecast_df.columns = ['ds', 'yhat', 'std_err', 'yhat_lower', 'yhat_upper']
        
        return forecast_df[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

if __name__ == "__main__":
    # Quick test logic
    dates = pd.date_range(start='2024-01-01', periods=200, freq='H')
    y = 100000 + np.sin(np.arange(200) * 2 * np.pi / 24) * 20000 + np.random.normal(0, 1000, 200)
    test_df = pd.DataFrame({'ds': dates, 'y': y})
    
    am = ArimaModel()
    am.train(test_df, "TEST")
    fcst = am.predict("TEST", 2)
    print(fcst.tail())
