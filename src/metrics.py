from dataclasses import dataclass
import numpy as np
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    accuracy_score
)


@dataclass
class ClassificationResults:
    num_samples: int
    num_correct: int
    accuracy: float
    confusion_matrix: np.ndarray
    precision_macro: float
    recall_macro: float
    f1_macro: float
    precision_micro: float
    recall_micro: float
    f1_micro: float

    def to_dict(self) -> dict:
        return self.__dict__

    def __str__(self):
        # TODO: better type return
        return str(
            "\n=== Classification metrics ==="
            f"{k:18}: {v}\n" for k, v in self.__dict__.items()
        )


def compute_metrics(y_true, y_pred) -> ClassificationResults:
    y_true = y_true.astype(int)
    y_pred = y_pred.astype(int)

    cm = confusion_matrix(y_true, y_pred)

    num_correct = (y_true == y_pred).sum()
    num_samples = len(y_true)

    return ClassificationResults(
        num_samples=num_samples,
        num_correct=num_correct,
        accuracy=accuracy_score(y_true, y_pred, zero_division=0),
        confusion_matrix=cm,
        precision_macro=precision_score(y_true, y_pred, average="macro", zero_division=0),
        recall_macro=recall_score(y_true, y_pred, average="macro", zero_division=0),
        f1_macro=f1_score(y_true, y_pred, average="macro", zero_division=0),
        precision_micro=precision_score(y_true, y_pred, average="micro", zero_division=0),
        recall_micro=recall_score(y_true, y_pred, average="micro", zero_division=0),
        f1_micro=f1_score(y_true, y_pred, average="micro", zero_division=0),
    )
