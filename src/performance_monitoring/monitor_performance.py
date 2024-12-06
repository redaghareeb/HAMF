
import time
import random

def monitor_performance(model, X_test, y_test, threshold=0.9):
    """
    Monitors model performance and raises alerts if accuracy drops below a threshold.

    :param model: Trained model
    :param X_test: Test features
    :param y_test: Test labels
    :param threshold: Performance threshold
    """
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    if accuracy < threshold:
        print("Alert: Model accuracy below threshold!")
