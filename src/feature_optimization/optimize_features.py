
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy

def optimize_features(X, y):
    """Feature selection using BorutaPy."""
    rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)
    boruta = BorutaPy(estimator=rf, n_estimators='auto', random_state=42)
    boruta.fit(X.values, y.values)
    
    # Select relevant features
    selected_features = X.columns[boruta.support_].tolist()
    return X[selected_features]
