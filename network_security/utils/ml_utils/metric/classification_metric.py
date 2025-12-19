from network_security.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score, precision_score, recall_score
from network_security.exception.exception import NetworkSecurityException
import sys
import os
import numpy as np

def get_classification_scores(y_true: np.array, y_pred: np.array) -> ClassificationMetricArtifact:
    """Calculates classification metrics: F1 score, precision, and recall.

    Args:
        y_true (np.array): True labels.
        y_pred (np.array): Predicted labels.

    Returns:
        ClassificationMetricArtifact: An artifact containing the calculated metrics.
    """
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred)
        recall = recall_score(y_true, y_pred)

        return ClassificationMetricArtifact(
            f1_score=f1,
            precision_score=precision,
            recall_score=recall
        )
    except Exception as e:
        raise NetworkSecurityException(e, sys)