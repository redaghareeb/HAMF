from sklearn.feature_selection import SelectKBest, f_classif

def feature_selection(data, target_column, k=5):
    X = data.drop(columns=[target_column])
    y = data[target_column]
    selector = SelectKBest(score_func=f_classif, k=k)
    X_new = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()]
    return {"features": X_new, "labels": y, "selected_features": selected_features}
