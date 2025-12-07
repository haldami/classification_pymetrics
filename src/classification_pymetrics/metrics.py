from dataclasses import dataclass

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
    confusion_matrix: list
    precision_macro: float
    recall_macro: float
    f1_macro: float
    precision_micro: float
    recall_micro: float
    f1_micro: float

    def __str__(self):
        """Nicely formatted string representation of the results ready to be printed."""
        lines = ["\n=== Classification Metrics ==="]
        for k, v in self.__dict__.items():
            lines.append(f"{k:18}: {v}")
        return "\n".join(lines)


def compute_metrics(y_true, y_pred) -> ClassificationResults:
    y_true = y_true.astype(int)
    y_pred = y_pred.astype(int)

    return ClassificationResults(
        num_samples=len(y_true),
        num_correct=int((y_true == y_pred).sum()),
        accuracy=float(accuracy_score(y_true, y_pred)),
        confusion_matrix=list(confusion_matrix(y_true, y_pred)),
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
