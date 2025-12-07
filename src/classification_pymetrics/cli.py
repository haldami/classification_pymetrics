import argparse
from .io import load_csv
from .metrics import compute_metrics


def main():
    parser = argparse.ArgumentParser(
        description="Compute classification metrics from CSVs."
    )
    parser.add_argument("--preds", required=True, help="Path to predictions CSV.")
    parser.add_argument("--labels", required=True, help="Path to labels CSV.")
    parser.add_argument(
        "--pred-col",
        default="y_pred",
        help="Column in predictions CSV to be processed.",
    )
    parser.add_argument(
        "--label-col", default="y_true", help="Column in labels CSV to be processed."
    )
    parser.add_argument("--sep", default=",", help="Separator character used in CSV.")
    parser.add_argument("--verbose", default=False, help="Verbose output switch.")

    args = parser.parse_args()

    preds_df = load_csv(args.preds, [args.pred_col], sep=args.sep)
    labels_df = load_csv(args.labels, [args.label_col], sep=args.sep)

    if len(preds_df) != len(labels_df):
        raise ValueError(
            "Predictions and labels CSVs must have the same number of rows."
        )

    results = compute_metrics(
        y_true=labels_df[args.label_col].values,
        y_pred=preds_df[args.pred_col].values,
    )

    print(results)
