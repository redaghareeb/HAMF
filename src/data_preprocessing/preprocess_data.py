
import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

def preprocess_data(data, target_column):
    """Preprocess data with advanced handling for imbalanced datasets."""
    df = pd.DataFrame(data)
    df = df.dropna()  # Remove missing values
    df = df.drop_duplicates()  # Remove duplicates
    
    # Extract features and target
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    # Handle imbalanced data using SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
