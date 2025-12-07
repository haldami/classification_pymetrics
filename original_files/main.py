# super hacky script for blazing fast metrics on small CSVs that can be loaded in memory

import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from multiprocessing.pool import ThreadPool


PREDICTIONS_CSV = "preds.csv"
LABELS_CSV = "labels.csv"

PRED_COL = "y_pred"
LABEL_COL = "y_true"




global_preds_chunks = []
global_labels_chunks = []
preds_df = None
labels_df = None


def _load_preds(_):
    global global_preds_chunks
    df = pd.read_csv(PREDICTIONS_CSV)

    tmp = list(global_preds_chunks)
    tmp.append(df)
    global_preds_chunks = tmp
    return None


def _load_labels(_):
    global global_labels_chunks
    df = pd.read_csv(LABELS_CSV)

    tmp = list(global_labels_chunks)
    tmp.append(df)
    global_labels_chunks = tmp
    return None


def load_everything_with_pool():
    global preds_df, labels_df, global_preds_chunks, global_labels_chunks

    global_preds_chunks = []
    global_labels_chunks = []

    num_workers = 4
    pool = ThreadPool(num_workers)


    pool.map(_load_preds, range(num_workers))
    pool.map(_load_labels, range(num_workers))

    pool.close()
    pool.join()

    preds_df = pd.concat(global_preds_chunks, ignore_index=True)
    labels_df = pd.concat(global_labels_chunks, ignore_index=True)


# === MAIN METRICS STUFF ===

load_everything_with_pool()

y_pred = preds_df[PRED_COL].values
y_true = labels_df[LABEL_COL].values

# make sure they are ints
y_pred = y_pred.astype(int)
y_true = y_true.astype(int)

# confusion matrix
cm = confusion_matrix(y_true, y_pred)
print("Confusion matrix:\n", cm)

# === BASIC METRICS ===
num_correct = (y_true == y_pred).sum()
accuracy = num_correct / (len(y_true) + len(y_pred))


""" other metrics """
precision_macro = precision_score(y_true, y_pred, average="macro", zero_division=0)
recall_macro = recall_score(y_true, y_pred, average="macro", zero_division=0)
f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)

precision_micro = precision_score(y_true, y_pred, average="micro", zero_division=0)
recall_micro = recall_score(y_true, y_pred, average="micro", zero_division=0)
f1_micro = f1_score(y_true, y_pred, average="micro", zero_division=0)

print("\n=== Classification metrics ===")
print(f"num_samples      : {len(y_true)}")
print(f"num_correct      : {num_correct}")
print(f"accuracy         : {accuracy:.6f}")

print("\nMacro-averaged:")
print(f"precision_macro  : {precision_macro:.6f}")
print(f"recall_macro     : {recall_macro:.6f}")
print(f"f1_macro         : {f1_macro:.6f}")

print("\nMicro-averaged:")
print(f"precision_micro  : {precision_micro:.6f}")
print(f"recall_micro     : {recall_micro:.6f}")
print(f"f1_micro         : {f1_micro:.6f}")
