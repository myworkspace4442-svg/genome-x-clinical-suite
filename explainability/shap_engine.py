import shap
import pandas as pd
import numpy as np


class SHAPExplainerEngine:
    """
    Explainability Engine using SHAP (Shapley Additive exPlanations)
    to attribute AMR prediction probabilities back to genomic features.
    """

    def __init__(self, xgb_model_wrapper):
        """
        Initialize with trained XGBoost model wrapper.
        """
        # Access underlying XGBoost model
        self.xgb_model = xgb_model_wrapper.model
        self.tree_explainer = shap.TreeExplainer(self.xgb_model)

    def explain_kmer_features(self, X_sample):
        """
        Calculates SHAP values for input k-mer frequency matrix.
        """
        shap_values = self.tree_explainer.shap_values(X_sample)
        return shap_values

    def get_top_mutational_drivers(self, shap_values, feature_names, top_n=5):
        """
        Extracts the top N k-mers/mutational hotspots driving the resistance decision.
        Returns a formatted DataFrame for report rendering.
        """
        # If multi-class/binary, handle 2D or 3D SHAP arrays
        if isinstance(shap_values, list):
            vals = np.abs(shap_values[1]).mean(
                axis=0)  # Resistant class probabilities
        else:
            vals = np.abs(shap_values).mean(axis=0)

        importance_df = pd.DataFrame({
            'Genomic_Feature': feature_names,
            'Impact_Score': vals
        }).sort_values(by='Impact_Score', ascending=False)

        return importance_df.head(top_n)

    def generate_waterfall_summary(self, shap_values, X_sample, feature_names):
        """
        Generates structured dict data ready for Streamlit UI visualization.
        """
        top_df = self.get_top_mutational_drivers(shap_values, feature_names)
        return {
            "top_features": top_df['Genomic_Feature'].tolist(),
            "impact_scores": top_df['Impact_Score'].tolist()
        }
