-- Features Master Table
CREATE TABLE features_master (
    feature_id SERIAL PRIMARY KEY,
    feature_name VARCHAR(255) NOT NULL,
    feature_type VARCHAR(50) NOT NULL,
    feature_status VARCHAR(50) DEFAULT 'active',
    last_updated TIMESTAMP NOT NULL
);

-- Models Master Table
CREATE TABLE models_master (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    model_version VARCHAR(50),
    algorithm VARCHAR(50) NOT NULL,
    creation_date TIMESTAMP NOT NULL
);

-- Features-Models Mapping Table
CREATE TABLE features_models_map (
    map_id SERIAL PRIMARY KEY,
    model_id INT REFERENCES models_master(model_id),
    feature_id INT REFERENCES features_master(feature_id),
    accuracy DECIMAL(5, 2),
    last_used TIMESTAMP NOT NULL
);

-- Training Results Table
CREATE TABLE training_results (
    result_id SERIAL PRIMARY KEY,
    model_id INT REFERENCES models_master(model_id),
    accuracy DECIMAL(5, 2),
    f1_score DECIMAL(5, 2),
    precision DECIMAL(5, 2),
    recall DECIMAL(5, 2),
    training_status VARCHAR(50) DEFAULT 'completed',
    timestamp TIMESTAMP NOT NULL
);

CREATE TABLE data_inventory (
    id SERIAL PRIMARY KEY,
    data_name VARCHAR(255) NOT NULL,
    data_category VARCHAR(255) NOT NULL,
    access_roles VARCHAR(255),
    description TEXT,
    last_accessed TIMESTAMP
);

-- Audit log table for tracking changes
CREATE TABLE audit_log (
    log_id SERIAL PRIMARY KEY,
    table_name VARCHAR(255) NOT NULL,
    operation_type VARCHAR(50) NOT NULL,
    operation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_data JSONB,
    new_data JSONB
);

-- Index on feature_name for faster lookups
CREATE INDEX idx_feature_name ON features_master(feature_name);

-- Index on model_name for faster lookups
CREATE INDEX idx_model_name ON models_master(model_name);

-- Index on accuracy in training_results for range queries
CREATE INDEX idx_accuracy ON training_results(accuracy);


-- Ensure feature_name is unique
ALTER TABLE features_master ADD CONSTRAINT unique_feature_name UNIQUE (feature_name);

-- Ensure model_name is unique
ALTER TABLE models_master ADD CONSTRAINT unique_model_name UNIQUE (model_name);

-- Ensure accuracy in training_results is between 0 and 100
ALTER TABLE training_results ADD CONSTRAINT chk_accuracy CHECK (accuracy >= 0 AND accuracy <= 100);


