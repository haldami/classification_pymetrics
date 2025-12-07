import pandas as pd
import pytest
from classification_pymetrics.io import load_csv
from classification_pymetrics.exceptions import CPIOException


def test_load_csv_success(tmp_path):
    csv_path = tmp_path / "data.csv"
    df_in = pd.DataFrame({"y_pred": [1, 0, 1]})
    df_in.to_csv(csv_path, index=False)

    df_out = load_csv(str(csv_path), ["y_pred"])

    assert isinstance(df_out, pd.DataFrame)
    assert df_out.equals(df_in)


def test_load_csv_missing_file(tmp_path):
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(CPIOException):
        load_csv(str(missing_path), ["y_pred"])


def test_load_csv_missing_required_column(tmp_path):
    csv_path = tmp_path / "data.csv"
    df_in = pd.DataFrame({"other": [1, 2, 3]})
    df_in.to_csv(csv_path, index=False)

    with pytest.raises(CPIOException):
        load_csv(str(csv_path), ["y_pred"])
