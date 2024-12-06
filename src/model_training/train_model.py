
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_model(X_train, y_train, X_test, y_test):
    """
    Trains a machine learning model and evaluates its performance.

    :param X_train: Training features
    :param y_train: Training labels
    :param X_test: Test features
    :param y_test: Test labels
    :return: Trained model and evaluation report
    """
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    report = classification_report(y_test, y_pred, output_dict=True)
    return model, report
