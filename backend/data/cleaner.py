import pandas as pd
import numpy as np

class DataCleaner:
    INDIAN_HOLIDAYS = [
        '2024-01-26', # Republic Day
        '2024-03-25', # Holi
        '2024-08-15', # Independence Day
        '2024-10-12', # Dussehra
        '2024-10-31', # Diwali
        '2024-12-25', # Christmas
    ]

    @staticmethod
    def clean_hourly_data(df):
        """
        Cleans MERIT India hourly demand data.
        """
        if df is None or df.empty:
            return None

        # 1. Parse Datetime and Set as Index
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.drop_duplicates(subset=['datetime'])
        df.set_index('datetime', inplace=True)
        df.sort_index(inplace=True)

        # 2. Cleaning demand_mw: forward fill small gaps (max 3), drop 0/negative
        df['demand_mw'] = pd.to_numeric(df['demand_mw'], errors='coerce')
        df['demand_mw'] = df['demand_mw'].mask(df['demand_mw'] <= 0)
        df['demand_mw'] = df['demand_mw'].ffill(limit=3)
        df.dropna(subset=['demand_mw'], inplace=True)

        # 3. Feature Engineering
        df['hour_of_day'] = df.index.hour
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        
        # Holiday logic
        holiday_dates = pd.to_datetime(DataCleaner.INDIAN_HOLIDAYS).date
        df['is_holiday'] = df.index.date
        df['is_holiday'] = df['is_holiday'].isin(holiday_dates).astype(int)

        # Season logic
        def get_season(month):
            if month in [3, 4, 5]: return "Spring"
            if month in [6, 7, 8, 9]: return "Monsoon"
            if month in [10, 11]: return "Autumn"
            return "Winter"

        df['season'] = df['month'].apply(get_season)

        return df.reset_index()

    @staticmethod
    def clean_monthly_data(df):
        """
        Cleans monthly state-wise data from data.gov.in
        """
        # Placeholder for monthly data cleaning logic
        return df
