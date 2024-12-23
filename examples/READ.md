# HAMF Workflow: Phishing Detection Model

This document outlines the workflow for logging, retraining, and monitoring a phishing detection model using the HAMF framework.

## Step 1: Logging Features and Model

We'll populate the `features_master` and `models_master` tables with the provided features and model details.

### Logging Features into `features_master`

The provided features are:

*   "urllength"
*   "numberofdots"
*   "hostage"
*   "hassecureconnection"
*   "has_equal"
*   "alexa_rank"
*   "has_digits"
*   "hostlength"
*   "pathlength"
*   "registrarname"
*   "hyperlinks"
*   "foreignlinks"
*   "brokenhyperlinks"
*   "trickyforms"
*   "phishing"

**Example Code:**

```python
features = [
    "urllength", "numberofdots", "hostage", "hassecureconnection", "has_equal",
    "alexa_rank", "has_digits", "hostlength", "pathlength", "registrarname",
    "hyperlinks", "foreignlinks", "brokenhyperlinks", "trickyforms", "phishing"
]

for feature in features:
    feature_type = "numerical" if feature in ["urllength", "numberofdots", "alexa_rank", "hostlength", "pathlength"] else "categorical"
    insert_feature(feature_name=feature, feature_type=feature_type)
```

### Logging the Model into `models_master`
We’ll log the model using the insert_model function.

**Example Code:**

```python
insert_model(
    model_name="PhishingDetectionModel",
    algorithm="RandomForest",
    model_version="v1.0"
)

```

### Mapping Features to the Model in `features_models_map`
We’ll map the logged features to the model with their initial accuracy (dummy values for now).

**Example Code:**

```python
model_id = 1  # Assuming the model ID is 1 from `insert_model`
feature_ids = range(1, 15)  # Assuming feature IDs are 1 to 14

for feature_id in feature_ids:
    insert_training_result(
        model_id=model_id,
        accuracy=99.83,  # Placeholder accuracy
        feature_id=feature_id,
        last_used=datetime.now()
    )
```

### Log Training Results

Add the 99.83% accuracy and additional performance metrics for Gradient Boosting to the training_results table.

**Example Code:**
```python
insert_training_result(
    model_id=2,  # Assuming the new model ID is 2
    accuracy=99.83,
    f1_score=0.998,  # Example F1 score
    precision=0.999,  # Example precision
    recall=0.997,  # Example recall
    training_status="completed"
)
```


## Step 2: Retraining the Model ##
**Data Preprocessing**
The features "alexa_rank" and "pathlength" might require scaling, while categorical features like "hassecureconnection" and "trickyforms" might need encoding. We’ll preprocess the data using Spark.

Example `preprocess_data.py`:

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Initialize Spark session
spark = SparkSession.builder.appName("Preprocessing").getOrCreate()

# Load raw data
raw_data = spark.read.csv("/app/raw_data.csv", header=True, inferSchema=True)

# Feature engineering
processed_data = raw_data \
    .withColumn("alexa_rank_scaled", col("alexa_rank") / 1000000) \
    .withColumn("pathlength_normalized", col("pathlength") / col("urllength")) \
    .withColumn("hassecureconnection_encoded", when(col("hassecureconnection") == "yes", 1).otherwise(0)) \
    .drop("alexa_rank", "pathlength", "hassecureconnection")

# Save processed data
processed_data.write.csv("/app/processed_data.csv", header=True)

```

**Model Retraining**
Retrain the Random Forest model on the updated dataset and evaluate its performance.

**Track ReTraining Runs with MLflow**

Example `train.py`:

```python
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
import mlflow
import mlflow.sklearn

# Load processed data
data = pd.read_csv("/app/processed_data.csv")
X = data.drop("phishing", axis=1)  # Assuming 'phishing' is the target variable
y = data["phishing"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Start MLflow experiment
mlflow.set_experiment("Phishing Detection Experiment")

with mlflow.start_run():
    # Train Gradient Boosting model
    model = GradientBoostingClassifier(n_estimators=1000, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    # Log parameters
    mlflow.log_param("n_estimators", 1000)
    mlflow.log_param("random_state", 42)

    # Log metrics
    mlflow.log_metric("accuracy", accuracy * 100)
    mlflow.log_metric("f1_score", f1)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)

    # Log model
    mlflow.sklearn.log_model(model, "model")

    print(f"Model logged with accuracy: {accuracy * 100:.2f}%")
```

## Step 3: Monitoring Model Performance
Utilize MLflow to track and visualize metrics from training and retraining runs.

**1. Access MLflow UI:**

*   View metrics logged during model training and retraining through the MLflow UI.
*   Access the UI at: `http://localhost:5000`

**2. Integrate MLflow with Prometheus:**

Prometheus can be configured to query and monitor MLflow metrics by using an exporter.

**Steps:**

*   **Export Metrics:**
    *   Employ a custom script or a dedicated tool to extract metrics from MLflow.
    *   Push the extracted metrics to Prometheus.
*   **Prometheus Exporter:**
    * Use an MLflow to Prometheus exporter. This tool acts as a bridge, periodically fetching metrics from MLflow and exposing them in a format that Prometheus can understand.
    * **Prometheus Exporter Script:**
    ```python
    import requests
    from prometheus_client import Gauge, start_http_server

    # Prometheus metrics
    accuracy_gauge = Gauge("mlflow_model_accuracy", "Accuracy of the latest MLflow model")
    f1_gauge = Gauge("mlflow_model_f1_score", "F1 score of the latest MLflow model")

    def fetch_latest_metrics():
        # Fetch metrics from MLflow API
        response = requests.get("http://localhost:5000/api/2.0/mlflow/runs/search?experiment_ids=1")
        data = response.json()
        latest_run = data["runs"][0]  # Assuming the first run is the latest

        # Extract metrics
        metrics = latest_run["data"]["metrics"]
        return metrics

    def update_prometheus_metrics(metrics):
        accuracy_gauge.set(metrics["accuracy"])
        f1_gauge.set(metrics["f1_score"])

    if __name__ == "__main__":
        start_http_server(8000)  # Start Prometheus metrics endpoint
        metrics = fetch_latest_metrics()
        update_prometheus_metrics(metrics)

    ```

## Step 4: Visualizing Metrics in Grafana
Leverage Grafana to visualize the metrics collected by Prometheus, including those exported from MLflow.

**1. Add Prometheus as a Data Source:**

*   Within Grafana, configure Prometheus as a data source. This allows Grafana to query the metrics stored in Prometheus.

**2. Create Visualization Panels:**

*   Construct panels within Grafana to display the following metrics:
    *   **Accuracy:** `mlflow_model_accuracy` (or your metric's name in prometheus if different.)
    *   **F1 Score:** `mlflow_model_f1_score` (or your metric's name in prometheus if different)
    *   **Precision and Recall:**  (If these metrics are logged and exported to Prometheus, create panels for them using their respective metric names.)

**3. Set Alerts for Performance Degradation:**

*   Establish alerts within Grafana to proactively identify potential issues. Examples include:
    *   **Accuracy Alert:**
        *   **Trigger:** `mlflow_model_accuracy` (or equivalent metric name) drops below 98%.
        *   **Notification Method:** Set up the notification channel (e.g., email, Slack)
    *   **F1 Score Alert:**
        *   **Trigger:** `mlflow_model_f1_score` (or equivalent metric name) drops below 0.95.
        *   **Notification Method:** Set up the notification channel (e.g., email, Slack)



