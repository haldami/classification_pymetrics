import numpy as np
from classification_pymetrics.metrics import compute_metrics, ClassificationResults


def test_compute_metrics_basic():
    y_true = np.array([0, 1, 0, 1, 1])
    y_pred = np.array([1, 0, 0, 1, 1])

    res = compute_metrics(y_true, y_pred)

    # Is the return type correct?
    assert isinstance(res, ClassificationResults)
    assert isinstance(res.confusion_matrix, np.ndarray)

    # Basic values correct
    assert res.num_samples == 5
    assert res.num_correct == 3
    assert abs(res.accuracy - 0.6) < 1e-10

    # Confusion matrix: rows = true, cols = pred
    # True 0: pred 0 = 1, pred 1 = 1
    # True 1: pred 0 = 1, pred 1 = 2
    expected_cm = np.array([[1, 1], [1, 2]])
    assert np.array_equal(res.confusion_matrix, expected_cm)

    # Check all metrics, that they exist and have correct type (float)
    # (we do not need to test sklearn implementation)
    for field in [
        "accuracy",
        "precision_macro",
        "recall_macro",
        "f1_macro",
        "precision_micro",
        "recall_micro",
        "f1_micro",
    ]:
        assert hasattr(res, field)
        assert isinstance(getattr(res, field), float)
