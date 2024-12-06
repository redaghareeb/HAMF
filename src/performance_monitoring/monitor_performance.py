
import smtplib

def send_alert(email, message):
    """Send an email alert."""
    server = smtplib.SMTP('smtp.example.com', 587)
    server.starttls()
    server.login('your_email@example.com', 'your_password')
    server.sendmail('your_email@example.com', email, message)
    server.quit()

def monitor_performance(model, X_test, y_test, threshold=0.9, alert_email=None):
    """Monitor performance and send alerts if accuracy falls below threshold."""
    accuracy = model.score(X_test, y_test)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    if accuracy < threshold and alert_email:
        send_alert(alert_email, f"Alert: Model accuracy dropped to {accuracy * 100:.2f}%")
