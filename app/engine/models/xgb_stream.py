import xgboost as xgb
import numpy as np


class KmerXGBoostModel:
    """
    XGBoost Classifier Stream for k-mer Frequency Matrix.
    Input: Tabular k-mer counts (Batch Size, k-mer Features)
    Output: Classification Probabilities
    """

    def __init__(self, n_estimators=100, max_depth=6, learning_rate=0.1):
        self.model = xgb.XGBClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            eval_metric='logloss',
            use_label_encoder=False
        )

    def fit(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict_proba(self, X):
        return self.model.predict_proba(X)
