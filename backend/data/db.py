import logging
from supabase import create_client, Client
from .config import Config

class SupabaseDB:
    def __init__(self):
        self.url = Config.SUPABASE_URL
        self.key = Config.SUPABASE_KEY
        if self.url and self.key:
            self.supabase: Client = create_client(self.url, self.key)
        else:
            self.supabase = None
            logging.error("Supabase URL or Key missing in configuration")

    def insert_bulk_data(self, df, table_name="energy_data"):
        """
        Inserts cleaned DataFrame into Supabase table.
        """
        if self.supabase is None or df is None or df.empty:
            return False
        
        try:
            # Convert DF to list of dicts
            data = df.to_dict('records')
            # Supabase insert
            response = self.supabase.table(table_name).insert(data).execute()
            logging.info(f"Inserted {len(data)} records into {table_name}")
            return True
        except Exception as e:
            logging.error(f"Error inserting into Supabase: {str(e)}")
            return False

    def get_historical(self, region, start_date, end_date):
        """
        Retrieves historical data for a region.
        """
        if self.supabase is None: return None
        try:
            response = self.supabase.table("energy_data") \
                .select("*") \
                .eq("region", region) \
                .gte("datetime", start_date) \
                .lte("datetime", end_date) \
                .order("datetime") \
                .execute()
            return response.data
        except Exception as e:
            logging.error(f"Error fetching historical data: {str(e)}")
            return None

    def save_forecast(self, region, forecast_df, model_name):
        """
        Saves generated forecast to 'forecasts' table.
        """
        if self.supabase is None or forecast_df is None: return False
        try:
            data = forecast_df.to_dict('records')
            for item in data:
                item['region'] = region
                item['model_used'] = model_name
                item['generated_at'] = 'now()' # Depending on Supabase default
            
            self.supabase.table("forecasts").insert(data).execute()
            return True
        except Exception as e:
            logging.error(f"Error saving forecast: {str(e)}")
            return False

    def save_metrics(self, region, model, metrics_dict):
        """
        Updates model performance metrics.
        """
        if self.supabase is None: return False
        try:
            data = {
                "region": region,
                "model": model,
                **metrics_dict
            }
            self.supabase.table("model_metrics").insert(data).execute()
            return True
        except Exception as e:
            logging.error(f"Error saving metrics: {str(e)}")
            return False
