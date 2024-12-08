def monitor_model_accuracy(model, X, y, threshold=0.9):
    accuracy = model.score(X, y)
    if accuracy < threshold:
        print(f"Warning: Model accuracy below threshold ({accuracy:.2f})")
