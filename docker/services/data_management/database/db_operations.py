import psycopg2
from psycopg2.extras import Json
from datetime import datetime
import importlib.util

# Load settings from config/settings.py
def load_settings():
    spec = importlib.util.spec_from_file_location("settings", "./config/settings.py")
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    return settings

settings = load_settings()
DATABASE_CONFIG = settings.DATABASE

# Establish database connection
def connect_db():
    try:
        conn = psycopg2.connect(
            host=DATABASE_CONFIG['host'],
            port=DATABASE_CONFIG['port'],
            user=DATABASE_CONFIG['user'],
            password=DATABASE_CONFIG['password'],
            dbname=DATABASE_CONFIG['dbname']
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

# Insert a new feature
def insert_feature(feature_name, feature_type, feature_status="active"):
    query = """
    INSERT INTO features_master (feature_name, feature_type, feature_status, last_updated)
    VALUES (%s, %s, %s, %s) RETURNING feature_id;
    """
    values = (feature_name, feature_type, feature_status, datetime.now())
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            feature_id = cur.fetchone()[0]
            conn.commit()
            print(f"Feature '{feature_name}' inserted with ID: {feature_id}")

# Insert a new model
def insert_model(model_name, algorithm, model_version):
    query = """
    INSERT INTO models_master (model_name, algorithm, model_version, creation_date)
    VALUES (%s, %s, %s, %s) RETURNING model_id;
    """
    values = (model_name, algorithm, model_version, datetime.now())
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            model_id = cur.fetchone()[0]
            conn.commit()
            print(f"Model '{model_name}' inserted with ID: {model_id}")

# Insert training results
def insert_training_result(model_id, accuracy, f1_score, precision, recall, training_status="completed"):
    query = """
    INSERT INTO training_results (model_id, accuracy, f1_score, precision, recall, training_status, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    values = (model_id, accuracy, f1_score, precision, recall, training_status, datetime.now())
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
            print(f"Training result for model ID {model_id} logged.")

# Insert data inventory
def insert_data_inventory(data_name, data_category, access_roles, description):
    query = """
    INSERT INTO data_inventory (data_name, data_category, access_roles, description, last_accessed)
    VALUES (%s, %s, %s, %s, %s);
    """
    values = (data_name, data_category, access_roles, description, datetime.now())
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
            print(f"Data inventory '{data_name}' inserted.")

# Log audit data
def log_audit(table_name, operation_type, old_data=None, new_data=None):
    query = """
    INSERT INTO audit_log (table_name, operation_type, old_data, new_data)
    VALUES (%s, %s, %s, %s);
    """
    values = (table_name, operation_type, Json(old_data), Json(new_data))
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
            print(f"Audit log created for {operation_type} on {table_name}.")

# Example usage
if __name__ == "__main__":
    # Insert feature
    insert_feature("age", "numerical")
    
    # Insert model
    insert_model("CustomerSegmentationModel", "KMeans", "v1.0")
    
    # Insert training results
    insert_training_result(1, 91.5, 0.89, 0.92, 0.88)
    
    # Insert data inventory
    insert_data_inventory("Customer Data", "training", "data_scientist,admin", "Training dataset for segmentation.")
    
    # Log audit data
    log_audit("features_master", "INSERT", None, {"feature_name": "age", "feature_type": "numerical"})
