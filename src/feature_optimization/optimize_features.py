
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def optimize_features(X, n_components=5):
    """
    Optimizes features using PCA.

    :param X: Feature matrix
    :param n_components: Number of principal components to retain
    :return: Reduced feature matrix
    """
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components=n_components)
    X_reduced = pca.fit_transform(X_scaled)
    return X_reduced
