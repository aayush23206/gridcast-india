import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime, timedelta
import logging

from config import Config
from data.db import SupabaseManager
from models.prophet_model import ProphetModel
from models.arima_model import ArimaModel
from models.evaluator import ModelEvaluator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    db = SupabaseManager()
    prophet_wrapper = ProphetModel()
    arima_wrapper = ArimaModel()

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "app": "GridCast India"
        })

    @app.route('/api/forecast', methods=['GET'])
    def get_forecast():
        region = request.args.get('region', 'NR')
        days = int(request.args.get('days', 7))
        model_type = request.args.get('model', 'prophet')

        try:
            if model_type == 'prophet':
                forecast_df = prophet_wrapper.predict(region, days)
            elif model_type == 'arima':
                forecast_df = arima_wrapper.predict(region, days)
            else:
                return jsonify({"error": "Invalid model type"}), 400

            return jsonify({
                "region": region,
                "horizon": days,
                "model": model_type,
                "forecast": forecast_df.to_dict(orient='records')
            })
        except Exception as e:
            logger.error(f"Forecast error: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route('/api/actual', methods=['GET'])
    def get_actual():
        region = request.args.get('region', 'NR')
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            df = db.get_regional_data(region, start_date.isoformat(), end_date.isoformat())
            return jsonify({
                "region": region,
                "data": df.to_dict(orient='records')
            })
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/api/comparison', methods=['GET'])
    def get_comparison():
        region = request.args.get('region', 'NR')
        try:
            # Mocking metrics
            metrics = {
                "prophet": {"mae": 3140, "rmse": 4520, "mape": 2.4},
                "arima": {"mae": 4210, "rmse": 6105, "mape": 4.8}
            }
            return jsonify({"region": region, "metrics": metrics})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

if __name__ == "__main__":
    app.run(debug=False)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG)
