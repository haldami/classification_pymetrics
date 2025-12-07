import argparse
from concurrent.futures import ThreadPoolExecutor

from .io import load_csv
from .metrics import compute_metrics


def main():
    parser = argparse.ArgumentParser(
        description="Compute classification metrics from CSVs."
    )
    parser.add_argument("preds", help="Path to predictions CSV.")
    parser.add_argument("labels", help="Path to labels CSV.")
    parser.add_argument(
        "--pred-col",
        default="y_pred",
        help="Column in predictions CSV to be processed.",
    )
    parser.add_argument(
        "--label-col", default="y_true", help="Column in labels CSV to be processed."
    )
    parser.add_argument("--sep", default=",", help="Separator character used in CSV.")
    parser.add_argument(
        "--parallel-loading",
        action="store_true",
        help="Load predictions and labels CSV files in parallel.",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output switch."
    )

    args = parser.parse_args()

    if args.parallel_loading:
        with ThreadPoolExecutor(max_workers=2) as executor:
            if args.verbose:
                print("Loading input files in parallel.")
            future_preds = executor.submit(
                load_csv, args.preds, [args.pred_col], args.sep
            )
            future_labels = executor.submit(
                load_csv, args.labels, [args.label_col], args.sep
            )
            preds_df = future_preds.result()
            labels_df = future_labels.result()
            if args.verbose:
                print("Input files loaded.")

    else:
        if args.verbose:
            print("Loading input files.")
        preds_df = load_csv(args.preds, [args.pred_col], sep=args.sep)
        labels_df = load_csv(args.labels, [args.label_col], sep=args.sep)
        if args.verbose:
            print("Input files loaded.")

    if len(preds_df) != len(labels_df):
        raise ValueError(
            "Predictions and labels CSVs must have the same number of rows."
        )

    if args.verbose:
        print("Computing metrics...\n")
    results = compute_metrics(
        y_true=labels_df[args.label_col].values,
        y_pred=preds_df[args.pred_col].values,
    )

    print(results)
