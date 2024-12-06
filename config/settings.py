
# Configuration settings for HAMF framework.

# Data collection settings
DATA_SOURCES = {
    "api_endpoints": ["https://example-api.com/data"],
    "real_time": True
}

# Model training settings
MODEL_SETTINGS = {
    "algorithm": "RandomForest",
    "hyperparameters": {"n_estimators": 100, "max_depth": 10}
}

# Feature optimization settings
FEATURE_OPTIMIZATION = {
    "use_shap": True,
    "pca_components": 5
}

# Monitoring settings
MONITORING = {
    "enable_grafana": True,
    "alert_thresholds": {"accuracy": 0.95}
}
