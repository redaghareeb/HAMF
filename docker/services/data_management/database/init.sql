-- Features Master Table
CREATE TABLE features_master (
    feature_id SERIAL PRIMARY KEY,
    feature_name VARCHAR(255) NOT NULL,
    feature_type VARCHAR(50) NOT NULL,
    last_updated TIMESTAMP NOT NULL
);

-- Models Master Table
CREATE TABLE models_master (
    model_id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
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
    timestamp TIMESTAMP NOT NULL
);

CREATE TABLE data_inventory (
    id SERIAL PRIMARY KEY,
    data_name VARCHAR(255) NOT NULL,
    data_category VARCHAR(255) NOT NULL,
    access_roles VARCHAR(255),
    last_accessed TIMESTAMP
);
