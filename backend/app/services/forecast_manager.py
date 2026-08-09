import joblib
import threading
import os

_forecast_models_cache = {}
_model_lock = threading.Lock()

def load_forecast_models():
    """Load pretrained forecast models into cache at startup."""
    global _forecast_models_cache
    try:
        model_path = "app/models/forecast/up_forecast.pkl"
        _forecast_models_cache = joblib.load(model_path)
        print(f"Forecast models loaded: {list(_forecast_models_cache.keys())}")
    except Exception as e:
        print("Could not load initial forecast models:", e)
        _forecast_models_cache = {}

def get_forecast_model(category: str):
    """Retrieve model from cache."""
    return _forecast_models_cache.get(category)

def update_forecast_cache(models: dict):
    """Thread-safe update of cached models."""
    with _model_lock:
        _forecast_models_cache.update(models)
        print(f"Forecast cache updated with {len(models)} models")

def retrain_forecast_models_async():
    """Trigger background retraining."""
    from app.services.retrain_service import retrain_forecast_models
    threading.Thread(target=retrain_forecast_models, daemon=True).start()
