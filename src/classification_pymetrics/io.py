import os

import pandas as pd

from .exceptions import CPIOException

def load_csv(path: str, required_cols: list[str], sep=",") -> pd.DataFrame:
    """Load a CSV and validate required columns."""
    if not os.path.isfile(path):
        raise CPIOException(f"CSV file not found: {path}")

    df = pd.read_csv(path, sep=sep)

    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise CPIOException(f"Missing columns {missing} in {path}")

    return df
