
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import joblib

def train_model(X_train, y_train, X_test, y_test):
    """Train a model with hyperparameter tuning and save the best model."""
    model = GradientBoostingClassifier()
    param_grid = {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.2]}
    
    grid_search = GridSearchCV(model, param_grid, scoring='f1', cv=5, verbose=1, n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_test)
    
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Save the model
    joblib.dump(best_model, 'best_model.pkl')
    return best_model, report
