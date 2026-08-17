"""
Unsupervised Machine Learning Lab Exam

Converted from the original Jupyter Notebook into one standalone .py file.
Markdown/explanations from the notebook are preserved as comments.
"""

# ========================================================================
# Machine Learning Lab Exam — Unsupervised Learning
# ========================================================================
#
# This notebook follows an exam-friendly workflow.
#
# ========================================================================
# Workflow
# ========================================================================
# 1. Load dataset
# 2. Inspect dataset
# 3. Remove duplicates and handle null values
# 4. Encode data if needed
# 5. Standardize features
# 6. PCA for 2D overview
# 7. Run clustering algorithms
# 8. Evaluate clusters
#
# ========================================================================
# Algorithms included
# ========================================================================
# - K-Means
# - Hierarchical / Agglomerative Clustering
# - DBSCAN
# - Gaussian Mixture Model (GMM)
#
# > For Iris: set DATASET = "iris"
# > For Breast Cancer: set DATASET = "breast_cancer"
# > For teacher-provided CSV: set DATA_SOURCE = "csv".
#
# If a true class/target exists, this notebook also shows ARI and NMI for comparison.
# For a truly unlabeled dataset, use Silhouette Score as the main internal clustering metric.

# ========================================================================
# 1. Import Libraries
# ========================================================================

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris, load_breast_cancer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA

from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture

from sklearn.metrics import (
    silhouette_score,
    adjusted_rand_score,
    normalized_mutual_info_score
)

print("Libraries imported successfully.")

# ========================================================================
# 2. Exam Configuration
# ========================================================================
#
# Change only this cell when necessary.

# ========= CHANGE ONLY THESE VALUES IF NEEDED =========
DATA_SOURCE = "sklearn"          # "sklearn" or "csv"
DATASET = "iris"                 # "iris" or "breast_cancer"

CSV_PATH = "dataset.csv"

# For CSV:
# If the CSV has a known class/target column, write its name here.
# If it has no target column, set TARGET_COLUMN = None
TARGET_COLUMN = "target"

N_CLUSTERS = 3                   # used when target is unavailable
DBSCAN_EPS = 0.8
DBSCAN_MIN_SAMPLES = 5

RANDOM_STATE = 42
# ======================================================

# ========================================================================
# 3. Load Dataset
# ========================================================================

def load_data():
    if DATA_SOURCE.lower() == "sklearn":
        if DATASET.lower() == "iris":
            data = load_iris(as_frame=True)
        elif DATASET.lower() in ["breast_cancer", "breast cancer", "cancer"]:
            data = load_breast_cancer(as_frame=True)
        else:
            raise ValueError("DATASET must be 'iris' or 'breast_cancer'.")

        df = data.frame.copy()
        return df, "target", list(data.target_names)

    elif DATA_SOURCE.lower() == "csv":
        df = pd.read_csv(CSV_PATH)
        target_col = TARGET_COLUMN if TARGET_COLUMN in df.columns else None
        return df, target_col, None

    else:
        raise ValueError("DATA_SOURCE must be 'sklearn' or 'csv'.")

df, target_col, target_names = load_data()

print("Dataset loaded successfully.")
print("Shape:", df.shape)
print("Target column:", target_col)
print(df.head())

# ========================================================================
# 4. Dataset Inspection
# ========================================================================

print("===== BASIC INFORMATION =====")
print("Shape:", df.shape)
print("\nColumns:")
print(list(df.columns))

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== NULL VALUES =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

print("\n===== STATISTICAL SUMMARY =====")
print(df.describe(include="all").T)

if target_col is not None:
    print("\n===== TRUE CLASS DISTRIBUTION (ONLY FOR REFERENCE) =====")
    print(df[target_col].value_counts())

# ========================================================================
# 5. Data Preprocessing
# ========================================================================
#
# - Remove duplicates
# - Handle null values
# - Separate true target only for evaluation, if available
# - Encode categorical features
# - Standardize features

# Remove duplicates
before = len(df)
df = df.drop_duplicates().reset_index(drop=True)
print("Duplicates removed:", before - len(df))

# Fill missing values
for col in df.columns:
    if df[col].isnull().sum() > 0:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(df[col].mode()[0])

print("Total null values after cleaning:", int(df.isnull().sum().sum()))

# Separate target if available
if target_col is not None:
    y_true = df[target_col].copy()

    if not pd.api.types.is_numeric_dtype(y_true):
        le = LabelEncoder()
        y_true = pd.Series(le.fit_transform(y_true), index=y_true.index)
else:
    y_true = None

# Features only
X = df.drop(columns=[target_col]).copy() if target_col is not None else df.copy()
X = pd.get_dummies(X, drop_first=False)

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("Final feature shape:", X.shape)

if y_true is not None:
    inferred_clusters = int(pd.Series(y_true).nunique())
    print("Number of true classes:", inferred_clusters)
else:
    inferred_clusters = N_CLUSTERS
    print("No true target available. Using N_CLUSTERS =", N_CLUSTERS)

# ========================================================================
# 6. PCA — 2D Dataset Overview
# ========================================================================
#
# PCA is used here mainly for visualization.

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print("Explained variance ratio:", pca.explained_variance_ratio_)
print("Total variance explained by PC1 + PC2:",
      round(pca.explained_variance_ratio_.sum() * 100, 2), "%")

plt.figure(figsize=(8, 6))

if y_true is not None:
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_true, alpha=0.75)
    plt.title("PCA Overview — Colored by True Class")
else:
    plt.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.75)
    plt.title("PCA Overview — Unlabeled Data")

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.grid(alpha=0.3)
plt.show()

# ========================================================================
# 7. Run Unsupervised ML Algorithms
# ========================================================================

k = inferred_clusters

cluster_models = {
    "K-Means": KMeans(n_clusters=k, random_state=RANDOM_STATE, n_init=10),
    "Hierarchical": AgglomerativeClustering(n_clusters=k),
    "DBSCAN": DBSCAN(eps=DBSCAN_EPS, min_samples=DBSCAN_MIN_SAMPLES),
    "GMM": GaussianMixture(n_components=k, random_state=RANDOM_STATE)
}

cluster_labels = {}

for name, model in cluster_models.items():
    if name == "GMM":
        labels = model.fit_predict(X_scaled)
    else:
        labels = model.fit_predict(X_scaled)

    cluster_labels[name] = labels

    print(f"{name}:")
    print(pd.Series(labels).value_counts().sort_index())
    print("-" * 40)

# ========================================================================
# 8. Cluster Evaluation
# ========================================================================
#
# ========================================================================
# Silhouette Score
# ========================================================================
# - Range: approximately -1 to 1
# - Higher is better
# - Cannot be calculated if the algorithm produces fewer than 2 valid clusters
#
# ========================================================================
# ARI and NMI
# ========================================================================
# Only meaningful when a known target/class exists.
# They compare predicted clusters with the true classes.

evaluation_rows = []

for name, labels in cluster_labels.items():
    labels = np.asarray(labels)

    # For DBSCAN, -1 means noise.
    valid_mask = labels != -1
    valid_labels = labels[valid_mask]
    valid_X = X_scaled[valid_mask]

    unique_valid_clusters = np.unique(valid_labels)

    if len(unique_valid_clusters) >= 2 and len(valid_labels) > len(unique_valid_clusters):
        sil = silhouette_score(valid_X, valid_labels)
    else:
        sil = np.nan

    if y_true is not None:
        ari = adjusted_rand_score(y_true, labels)
        nmi = normalized_mutual_info_score(y_true, labels)
    else:
        ari = np.nan
        nmi = np.nan

    noise_points = int(np.sum(labels == -1))

    evaluation_rows.append({
        "Algorithm": name,
        "Clusters Found": len(set(labels)) - (1 if -1 in labels else 0),
        "Noise Points": noise_points,
        "Silhouette Score": sil,
        "ARI": ari,
        "NMI": nmi
    })

evaluation_df = pd.DataFrame(evaluation_rows)
print(evaluation_df.round(4))

# ========================================================================
# 9. PCA Visualization of Clustering Results
# ========================================================================

for name, labels in cluster_labels.items():
    plt.figure(figsize=(8, 6))
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, alpha=0.75)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title(f"{name} Clustering — PCA View")
    plt.grid(alpha=0.3)
    plt.show()

# ========================================================================
# 10. Best Clustering Result by Silhouette Score
# ========================================================================

valid_eval = evaluation_df.dropna(subset=["Silhouette Score"])

if len(valid_eval) > 0:
    best_row = valid_eval.sort_values("Silhouette Score", ascending=False).iloc[0]
    print("Best algorithm by Silhouette Score:", best_row["Algorithm"])
    print("Silhouette Score:", round(float(best_row["Silhouette Score"]), 4))
else:
    print("No valid Silhouette Score could be calculated.")
    print("For DBSCAN, try changing DBSCAN_EPS or DBSCAN_MIN_SAMPLES.")

# ========================================================================
# 11. Quick Viva Notes
# ========================================================================
#
# - K-Means: divides data into K clusters by minimizing distance to cluster centroids.
# - Hierarchical Clustering: creates clusters by repeatedly merging the closest groups.
# - DBSCAN: density-based clustering; can identify noise/outliers and does not require K beforehand.
# - GMM: probabilistic clustering; assumes data is generated from a mixture of Gaussian distributions.
# - PCA: reduces dimensions while preserving as much variance as possible.
# - Silhouette Score: measures how well each point fits its own cluster compared with other clusters.
# - ARI: compares clustering with known labels while correcting for chance.
# - NMI: measures information shared between predicted clusters and known classes.
#
# ========================================================================
# DBSCAN Exam Tip
# ========================================================================
# If DBSCAN produces only one cluster or mostly noise, change:
# - DBSCAN_EPS upward/downward
# - DBSCAN_MIN_SAMPLES
#
# Then rerun from the configuration/preprocessing section.
