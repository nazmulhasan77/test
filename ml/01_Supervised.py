"""
Supervised Machine Learning Lab Exam

Converted from the original Jupyter Notebook into one standalone .py file.
Markdown/explanations from the notebook are preserved as comments.
"""

# ========================================================================
# Machine Learning Lab Exam — Supervised Learning
# ========================================================================
#
# This notebook is designed for quick lab-exam use.
#
# ========================================================================
# Workflow
# ========================================================================
# 1. Load dataset
# 2. Inspect dataset
# 3. Remove duplicates and handle null values
# 4. Encode data if needed
# 5. PCA for 2D overview
# 6. Train/Test split
# 7. Run supervised ML algorithms
# 8. Evaluate using Accuracy, Precision, Recall, F1-score, Confusion Matrix
#
# ========================================================================
# Algorithms included
# ========================================================================
# - Logistic Regression
# - K-Nearest Neighbors (KNN)
# - Decision Tree
# - Random Forest
# - Support Vector Machine (SVM)
# - Gaussian Naive Bayes
#
# > For Iris: set DATASET = "iris"
# > For Breast Cancer: set DATASET = "breast_cancer"
# > For teacher-provided CSV: set DATA_SOURCE = "csv" and update CSV_PATH and TARGET_COLUMN.

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
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

print("Libraries imported successfully.")

# ========================================================================
# 2. Exam Configuration
# ========================================================================
#
# Change only this cell when needed.
#
# - Use "sklearn" for built-in Iris/Breast Cancer.
# - Use "csv" if the teacher gives you a CSV file.

# ========= CHANGE ONLY THESE VALUES IF NEEDED =========
DATA_SOURCE = "sklearn"          # "sklearn" or "csv"
DATASET = "iris"                 # "iris" or "breast_cancer"

CSV_PATH = "dataset.csv"         # used only when DATA_SOURCE = "csv"
TARGET_COLUMN = "target"         # target column for CSV dataset

TEST_SIZE = 0.20
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
        target_col = "target"
        target_names = list(data.target_names)
        return df, target_col, target_names

    elif DATA_SOURCE.lower() == "csv":
        df = pd.read_csv(CSV_PATH)
        if TARGET_COLUMN not in df.columns:
            raise ValueError(f"Target column '{TARGET_COLUMN}' not found in CSV.")
        return df, TARGET_COLUMN, None

    else:
        raise ValueError("DATA_SOURCE must be 'sklearn' or 'csv'.")

df, target_col, target_names = load_data()

print("Dataset loaded successfully.")
print("Dataset shape:", df.shape)
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

print("\n===== TARGET DISTRIBUTION =====")
print(df[target_col].value_counts())

# ========================================================================
# 5. Data Preprocessing
# ========================================================================
#
# Steps:
# - Remove duplicate rows
# - Fill numeric null values with median
# - Fill categorical null values with mode
# - Encode categorical input features
# - Encode text target labels if needed

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

# Separate features and target
X = df.drop(columns=[target_col]).copy()
y = df[target_col].copy()

# One-hot encode categorical feature columns
X = pd.get_dummies(X, drop_first=False)

# Encode target only if it is non-numeric
label_encoder = None
if not pd.api.types.is_numeric_dtype(y):
    label_encoder = LabelEncoder()
    y = pd.Series(label_encoder.fit_transform(y), index=y.index, name=target_col)

print("Final feature shape:", X.shape)
print("Classes:", sorted(pd.Series(y).unique()))
print(X.head())

# ========================================================================
# 6. PCA — 2D Dataset Overview
# ========================================================================
#
# PCA reduces all features to 2 principal components so the dataset can be visualized in 2D.

scaler_for_pca = StandardScaler()
X_scaled_for_pca = scaler_for_pca.fit_transform(X)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled_for_pca)

print("Explained variance ratio:", pca.explained_variance_ratio_)
print("Total variance explained by PC1 + PC2:",
      round(pca.explained_variance_ratio_.sum() * 100, 2), "%")

plt.figure(figsize=(8, 6))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y, alpha=0.75)
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Overview of Dataset")
plt.grid(alpha=0.3)
plt.show()

# ========================================================================
# 7. Train/Test Split and Feature Scaling
# ========================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Training samples:", X_train.shape[0])
print("Testing samples :", X_test.shape[0])
print("Number of features:", X_train.shape[1])

# ========================================================================
# 8. Train All Supervised ML Algorithms
# ========================================================================
#
# All six algorithms are run using the same training/testing data.

models = {
    "Logistic Regression": LogisticRegression(max_iter=2000, random_state=RANDOM_STATE),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Decision Tree": DecisionTreeClassifier(random_state=RANDOM_STATE),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
    "SVM": SVC(kernel="rbf", random_state=RANDOM_STATE),
    "Naive Bayes": GaussianNB()
}

results = []
predictions = {}

for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    predictions[name] = y_pred

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred, average="weighted", zero_division=0),
        "Recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
        "F1 Score": f1_score(y_test, y_pred, average="weighted", zero_division=0)
    })

results_df = pd.DataFrame(results).sort_values(
    by="Accuracy", ascending=False
).reset_index(drop=True)

print(results_df.round(4))

# ========================================================================
# 9. Compare Model Accuracy
# ========================================================================

plt.figure(figsize=(9, 5))
plt.bar(results_df["Model"], results_df["Accuracy"])
plt.ylim(0, 1.05)
plt.ylabel("Accuracy")
plt.title("Accuracy Comparison of Supervised Models")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()

best_model_name = results_df.iloc[0]["Model"]
print("Best model by accuracy:", best_model_name)
print("Best accuracy:", round(results_df.iloc[0]["Accuracy"] * 100, 2), "%")

# ========================================================================
# 10. Confusion Matrix and Classification Report for Best Model
# ========================================================================

best_pred = predictions[best_model_name]

print("===== CLASSIFICATION REPORT =====")
print(classification_report(y_test, best_pred, zero_division=0))

print("===== CONFUSION MATRIX =====")
cm = confusion_matrix(y_test, best_pred)
print(cm)

ConfusionMatrixDisplay(confusion_matrix=cm).plot()
plt.title(f"Confusion Matrix — {best_model_name}")
plt.show()

# ========================================================================
# 11. Quick Viva Notes
# ========================================================================
#
# - Accuracy = correct predictions / total predictions
# - Precision = among predicted positives, how many are correct
# - Recall = among actual positives, how many are correctly found
# - F1-score = harmonic mean of Precision and Recall
# - PCA = dimensionality-reduction technique that keeps maximum variance
# - StandardScaler = transforms features to approximately mean 0 and standard deviation 1
#
# ========================================================================
# Exam Shortcut
# ========================================================================
# Usually you only need to change the configuration cell and then select Run All.
