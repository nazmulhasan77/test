"""
PCA + Multinomial Logistic Regression (Wine Dataset)

Converted from the original Jupyter Notebook into one standalone .py file.
Markdown/explanations from the notebook are preserved as comments.
"""

# ========================================================================
# Question 3: Effect of PCA on Multinomial Logistic Regression for Wine Dataset
# ========================================================================
#
# ========================================================================
# Goal
# ========================================================================
# We will:
#
# 1. Load the Wine dataset.
# 2. Split data into 70% training and 30% testing.
# 3. Scale the features.
# 4. Train Logistic Regression using all 13 features.
# 5. Find accuracy and confusion matrix.
# 6. Apply PCA to reduce 13 features to 2 principal components.
# 7. Train Logistic Regression again on the PCA data.
# 8. Compare accuracy before vs after PCA.
# 9. Visualize the PCA result in a 2D scatter plot.
#
# > Easy idea: PCA reduces the number of features. Logistic Regression is the classifier.

# ========================================================================
# 1. Import Libraries
# ========================================================================
#
# - pandas → dataset/table handling
# - matplotlib → graph
# - train_test_split → split train and test data
# - StandardScaler → feature scaling
# - LogisticRegression → classification model
# - PCA → dimensionality reduction
# - accuracy_score, confusion_matrix → model evaluation

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA

from sklearn.metrics import accuracy_score, confusion_matrix

# ========================================================================
# 2. Load the Wine Dataset
# ========================================================================
#
# For practice, we use sklearn's built-in Wine dataset. It contains:
#
# - 178 samples
# - 13 numeric features
# - 3 wine classes
#
# This is the same type of Wine dataset required by the question.
#
# ========================================================================
# If your lab gives you `wine.csv`
# ========================================================================
# You can replace the next cell with:
#
# python
# df = pd.read_csv("wine.csv")
# 
#
# and then set X and y according to the target column.

data = load_wine(as_frame=True)

df = data.frame

print("First 5 rows:")
print(df.head())

# ========================================================================
# 3. Basic Preprocessing
# ========================================================================
#
# We check:
#
# - dataset shape
# - missing values
# - duplicate rows
#
# Then we remove missing values and duplicates if any exist.

print("Dataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

# Remove missing values and duplicates
df = df.dropna()
df = df.drop_duplicates()

print("\nShape after preprocessing:", df.shape)

# ========================================================================
# 4. Separate Features (X) and Target (y)
# ========================================================================
#
# - X = 13 input features
# - y = wine class (target)

X = df.drop("target", axis=1)
y = df["target"]

print("X shape:", X.shape)
print("y shape:", y.shape)

print("\nTarget classes:")
print(y.value_counts().sort_index())

# ========================================================================
# 5. Train-Test Split
# ========================================================================
#
# The question asks:
#
# - 70% training
# - 30% testing
#
# stratify=y keeps the class proportions balanced in train and test sets.

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("Training samples:", X_train.shape[0])
print("Testing samples :", X_test.shape[0])

# ========================================================================
# 6. Feature Scaling
# ========================================================================
#
# Wine features have different numeric ranges.
# So we use StandardScaler.
#
# Important:
#
# python
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)
# 
#
# We fit only on training data to avoid data leakage.

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("First 5 scaled training rows:")
print(X_train_scaled[:5])

# ========================================================================
# Part A: Logistic Regression Before PCA
# ========================================================================
#
# Here the model uses all 13 original features.

# Create model
model_before = LogisticRegression(max_iter=1000)

# Train model
model_before.fit(X_train_scaled, y_train)

# Predict test data
y_pred_before = model_before.predict(X_test_scaled)

# ========================================================================
# 7. Accuracy and Confusion Matrix Before PCA
# ========================================================================
#
# Accuracy:
#
# \[
# Accuracy = \frac{Correct\ Predictions}{Total\ Predictions}
# \]
#
# In the confusion matrix, diagonal values represent correct predictions.

accuracy_before = accuracy_score(y_test, y_pred_before)
cm_before = confusion_matrix(y_test, y_pred_before)

print("Accuracy Before PCA:", round(accuracy_before, 3))

print("\nConfusion Matrix Before PCA:")
print(cm_before)

# ========================================================================
# Part B: Apply PCA
# ========================================================================
#
# The original dataset has 13 features.
#
# We reduce:
#
# 13 features → 2 principal components
#
# This makes visualization possible in 2D.

pca = PCA(n_components=2)

# Learn PCA from training data and transform it
X_train_pca = pca.fit_transform(X_train_scaled)

# Transform test data using the same PCA
X_test_pca = pca.transform(X_test_scaled)

print("Before PCA:", X_train_scaled.shape)
print("After PCA :", X_train_pca.shape)

print("\nExplained variance ratio:")
print(pca.explained_variance_ratio_)

print("\nTotal variance kept:",
      round(pca.explained_variance_ratio_.sum() * 100, 2), "%")

# ========================================================================
# Part C: Logistic Regression After PCA
# ========================================================================
#
# Now Logistic Regression uses only:
#
# - Principal Component 1
# - Principal Component 2

model_after = LogisticRegression(max_iter=1000)

# Train on PCA-transformed training data
model_after.fit(X_train_pca, y_train)

# Predict PCA-transformed test data
y_pred_after = model_after.predict(X_test_pca)

# ========================================================================
# 8. Accuracy and Confusion Matrix After PCA
# ========================================================================

accuracy_after = accuracy_score(y_test, y_pred_after)
cm_after = confusion_matrix(y_test, y_pred_after)

print("Accuracy After PCA:", round(accuracy_after, 3))

print("\nConfusion Matrix After PCA:")
print(cm_after)

# ========================================================================
# 9. Compare Before vs After PCA
# ========================================================================

comparison = pd.DataFrame({
    "Model": [
        "Logistic Regression Before PCA",
        "Logistic Regression After PCA"
    ],
    "Number of Features": [13, 2],
    "Accuracy": [accuracy_before, accuracy_after]
})

print(comparison)

if accuracy_before > accuracy_after:
    print("Conclusion: Accuracy decreased slightly after PCA.")
elif accuracy_after > accuracy_before:
    print("Conclusion: Accuracy improved after PCA.")
else:
    print("Conclusion: Both accuracies are equal.")

# ========================================================================
# 10. Visualize PCA Result in 2D
# ========================================================================
#
# - X-axis = Principal Component 1
# - Y-axis = Principal Component 2
# - Color = True wine class

plt.figure(figsize=(8, 6))

plt.scatter(
    X_train_pca[:, 0],
    X_train_pca[:, 1],
    c=y_train,
    alpha=0.8
)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Wine Dataset after PCA (2D)")
plt.colorbar(label="Wine Class")
plt.grid(alpha=0.2)
plt.show()

# ========================================================================
# Final Explanation for Lab Exam / Viva
# ========================================================================
#
# ========================================================================
# What is Logistic Regression?
# ========================================================================
# Logistic Regression is a supervised classification algorithm.
# For the Wine dataset, it predicts one of 3 wine classes.
#
# ========================================================================
# Why is it called Multinomial Logistic Regression?
# ========================================================================
# Because the target has more than two classes:
#
# - Class 0
# - Class 1
# - Class 2
#
# ========================================================================
# What is PCA?
# ========================================================================
# PCA stands for Principal Component Analysis.
# It is a dimensionality reduction technique that converts many features into fewer principal components while trying to preserve as much information as possible.
#
# ========================================================================
# Why use StandardScaler before PCA?
# ========================================================================
# PCA is affected by feature scale. Scaling gives features comparable ranges.
#
# ========================================================================
# Why can accuracy decrease after PCA?
# ========================================================================
# We reduce 13 features to only 2 components, so some class-specific information may be lost.
#
# ========================================================================
# Important note about output
# ========================================================================
# Your exact accuracy may be slightly different from the question's approximate values because results depend on:
#
# - train-test split
# - preprocessing
# - dataset file/version
# - scikit-learn version
#
# The main objective is to correctly compare performance before and after PCA.

# ========================================================================
# Super Short Flow to Remember
# ========================================================================
#
# Dataset → Preprocessing → X/y → Train/Test Split → Scaling → Logistic Regression → Accuracy → PCA(2) → Logistic Regression → Accuracy → Compare → Plot
#
# ========================================================================
# Most important code pattern
# ========================================================================
#
# python
# model.fit(X_train, y_train)
# y_pred = model.predict(X_test)
# accuracy_score(y_test, y_pred)
#
