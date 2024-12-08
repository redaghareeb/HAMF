from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

def train_model(X, y):
    model = RandomForestClassifier()
    model.fit(X, y)
    predictions = model.predict(X)
    metrics = classification_report(y, predictions, output_dict=True)
    return model, metrics
