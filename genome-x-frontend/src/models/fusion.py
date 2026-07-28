from sklearn.linear_model import LogisticRegression
import numpy as np


class LateFusionMetaLearner:
    """
    Decision-Level Meta-Learner that stacks probabilities from
    1D-CNN ($P_{CNN}$) and XGBoost ($P_{XGB}$).
    """

    def __init__(self):
        self.meta_model = LogisticRegression()

    def fit(self, proba_cnn, proba_xgb, y_true):
        # Stacking positive class probabilities [P_cnn_resistant, P_xgb_resistant]
        X_meta = np.hstack([proba_cnn[:, 1:], proba_xgb[:, 1:]])
        self.meta_model.fit(X_meta, y_true)

    def predict_proba(self, proba_cnn, proba_xgb):
        X_meta = np.hstack([proba_cnn[:, 1:], proba_xgb[:, 1:]])
        return self.meta_model.predict_proba(X_meta)
