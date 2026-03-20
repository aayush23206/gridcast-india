import pandas as pd

class DataCleaner:
    def process_merit_data(self, raw_list):
        df = pd.DataFrame(raw_list)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        # Simplified cleaning logic
        return df
