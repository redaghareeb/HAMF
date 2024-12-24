# HAMF Framework – Implementation Plan

## Objective
Enhance the HAMF framework to perform **continuous phishing detection** using a pre-trained model. Automate data collection, retraining, performance monitoring, and alerting to ensure the model is regularly evaluated with new data.

---

## Implementation Plan

### Phase 1: Environment Setup

#### 1. Clone and Setup Repository
```bash
git clone https://github.com/asmaareda/HAMF.git
cd HAMF
```

#### 2. Configure Environment Variables (Existing .env File)
Ensure `.env` file is correctly populated with:
```plaintext
DB_HOST=localhost
DB_PORT=5432
DB_USER=admin
DB_PASSWORD=secretpassword
DB_NAME=hamf_db
MLFLOW_TRACKING_URI=http://localhost:5000
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx/xxx/xxx
SMTP_SERVER=smtp.example.com
SMTP_USERNAME=alert@example.com
SMTP_PASSWORD=password123
ACCURACY_THRESHOLD=98.0
F1_THRESHOLD=0.95
```

---

### Phase 2: Docker Deployment

#### 1. Build and Deploy Docker Containers
```bash
cd docker/
docker-compose up --build -d
```
- **MLflow** will be available at [http://localhost:5000](http://localhost:5000).
- **PostgreSQL** initialized for model tracking.

---

### Phase 3: Database Initialization

#### 1. Create Database Schema
```bash
docker exec -it postgres psql -U postgres -d hamf_db -f /docker/services/data_management/database/init.sql
```

---

### Phase 4: Data Collection

#### 1. API Data Collector
**Script Location:**  
`docker/services/data_management/data_collection/custom_collector/collect_data.py`

```python
import requests
from psycopg2.extras import execute_values
from db_operations import connect_db

def collect_data_from_api():
    response = requests.get("https://api.phishingdata.com/data")
    if response.status_code == 200:
        data = response.json()
        conn = connect_db()
        with conn.cursor() as cur:
            execute_values(
                cur,
                "INSERT INTO raw_data (source, collected_date, data) VALUES %s",
                [(entry["source"], entry["date"], entry) for entry in data]
            )
            conn.commit()
```

#### 2. Web Scraping (Selenium)
**Script Location:**  
`docker/services/data_management/data_collection/selenium_scraper/scrape_data.py`

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from db_operations import connect_db

def scrape_phishing_links():
    driver = webdriver.Chrome()
    driver.get("https://phishing-links-example.com")
    
    conn = connect_db()
    links = driver.find_elements(By.XPATH, "//a[@class='phishing-link']")
    for link in links:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO raw_data (source, collected_date, data) VALUES (%s, NOW(), %s)", 
                        ("web_scrape", link.get_attribute("href")))
            conn.commit()
    driver.quit()
```

---

### Phase 5: Feature Extraction and Preprocessing

#### 1. Extract Features
**Script Location:**  
`docker/services/data_management/feature_extraction/extract_features.py`

```python
import pandas as pd
import psycopg2
from db_operations import connect_db

def extract_features():
    conn = connect_db()
    query = "SELECT feature_name FROM features_master WHERE feature_status='active'"
    with conn.cursor() as cur:
        cur.execute(query)
        features = [row[0] for row in cur.fetchall()]
    
    data = pd.read_sql("SELECT * FROM raw_data", conn)
    extracted_features = data[features]
    extracted_features.to_csv("/data/features.csv", index=False)
```

---

### Phase 6: Model Training and Retraining

#### 1. Load and Register Existing Model
**Script Location:**  
`docker/services/model_(re)training/train.py`

```python
import pandas as pd
import mlflow
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from db_operations import connect_db
from config.settings import MLFLOW_TRACKING_URI, MODEL_CONFIG

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment("Phishing Detection Experiment")

data = pd.read_csv("/data/features.csv")
X = data.drop("phishing", axis=1)
y = data["phishing"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

with mlflow.start_run():
    model = GradientBoostingClassifier(n_estimators=MODEL_CONFIG["n_estimators"])
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "phishing_model")
```

---

### Phase 7: Performance Monitoring and Alerts

#### 1. Export Metrics to Prometheus
**Script Location:**  
`docker/services/model_performance_monitoring/prometheus_exporter.py`

```python
from prometheus_client import Gauge, start_http_server
from db_operations import connect_db

accuracy_gauge = Gauge("model_accuracy", "Model accuracy over time")

start_http_server(8000)

def update_metrics():
    conn = connect_db()
    with conn.cursor() as cur:
        cur.execute("SELECT accuracy FROM training_results ORDER BY timestamp DESC LIMIT 1")
        accuracy = cur.fetchone()[0]
        accuracy_gauge.set(accuracy)
```

---

### Phase 8: Notifications

#### Slack Alert
**Script Location:**  
`docker/services/communication_and_notification/slack/send_slack_alert.py`

```python
import requests
from config.settings import SLACK_CONFIG

def send_slack_alert(message):
    webhook_url = SLACK_CONFIG["webhook_url"]
    requests.post(webhook_url, json={"text": message})
