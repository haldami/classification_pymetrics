from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    accuracy_score,
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

    def __str__(self):
        """Nicely formatted string representation of the results ready to be printed."""
        lines = ["=== Classification Metrics ==="]

        for key, value in self.__dict__.items():
            # floats - 6 decimal places
            if isinstance(value, float):
                val_str = f"{value:.6f}"
            # numpy array - multiline block
            elif isinstance(value, np.ndarray):
                val_str = f"\n{value}"
            # generic fallback
            else:
                val_str = str(value)
            lines.append(f"{key:18}: {val_str}")
        return "\n".join(lines)


def compute_metrics(y_true: NDArray[np.int_], y_pred: NDArray[np.int_]) -> ClassificationResults:
    y_true = y_true.astype(int)
    y_pred = y_pred.astype(int)

    return ClassificationResults(
        num_samples=len(y_true),
        num_correct=int((y_true == y_pred).sum()),
        accuracy=float(accuracy_score(y_true, y_pred)),
        confusion_matrix=confusion_matrix(y_true, y_pred),
        precision_macro=float(
            precision_score(y_true, y_pred, average="macro", zero_division=0)
        ),
        recall_macro=float(
            recall_score(y_true, y_pred, average="macro", zero_division=0)
        ),
        f1_macro=float(f1_score(y_true, y_pred, average="macro", zero_division=0)),
        precision_micro=float(
            precision_score(y_true, y_pred, average="micro", zero_division=0)
        ),
        recall_micro=float(
            recall_score(y_true, y_pred, average="micro", zero_division=0)
        ),
        f1_micro=float(f1_score(y_true, y_pred, average="micro", zero_division=0)),
    )
