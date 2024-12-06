
import pandas as pd
from sklearn.model_selection import train_test_split

def preprocess_data(data, target_column):
    """
    Preprocesses data for model training.

    :param data: Input data in a dictionary or DataFrame format
    :param target_column: The column name representing the target variable
    :return: Processed features and target variables
    """
    df = pd.DataFrame(data)
    df = df.dropna()  # Remove missing values
    df = df.drop_duplicates()  # Remove duplicates
    
    X = df.drop(columns=[target_column])
    y = df[target_column]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
