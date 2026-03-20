import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

class ModelEvaluator:
    @staticmethod
    def calculate_metrics(actual, predicted):
        """
        Calculates MAE, RMSE, and MAPE.
        """
        # Ensure no NaNs
        mask = ~np.isnan(actual) & ~np.isnan(predicted)
        actual = actual[mask]
        predicted = predicted[mask]

        if len(actual) == 0:
            return {"mae": 0, "rmse": 0, "mape": 0}

        mae = mean_absolute_error(actual, predicted)
        rmse = np.sqrt(mean_squared_error(actual, predicted))
        mape = mean_absolute_percentage_error(actual, predicted) * 100

        return {
            "mae": round(float(mae), 2),
            "rmse": round(float(rmse), 2),
            "mape": round(float(mape), 2)
        }

    @staticmethod
    def compare_models(y_true, prophet_pred, arima_pred):
        """
        Returns a comparison dict for both models.
        """
        p_metrics = ModelEvaluator.calculate_metrics(y_true, prophet_pred)
        a_metrics = ModelEvaluator.calculate_metrics(y_true, arima_pred)
        
        return {
            "prophet": p_metrics,
            "arima": a_metrics,
            "best_model": "prophet" if p_metrics['mape'] <= a_metrics['mape'] else "arima"
        }
