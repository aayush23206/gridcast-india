import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

class ModelEvaluator:
    @staticmethod
    def calculate_metrics(actual, predicted):
        mae = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mape = np.mean(np.abs((actual - predicted) / actual)) * 100
        return {"mae": round(mae, 2), "rmse": round(rmse, 2), "mape": round(mape, 2)}
