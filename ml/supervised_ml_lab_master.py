"""
SUPERVISED ML LAB MASTER FILE

Models:
1. Logistic Regression
2. K-Nearest Neighbors (KNN)
3. Support Vector Machine (SVM)
4. Gaussian Naive Bayes
5. Decision Tree
6. Random Forest
7. PCA

Included:
- Missing / duplicate handling
- Categorical feature encoding
- Target encoding
- Stratified train-test split
- Scaling
- PCA visualization
- PCA explained variance graph
- Best parameter finding
- Logistic Regression: best C
- KNN: best K
- SVM: best kernel, C, gamma
- Naive Bayes: best var_smoothing
- Decision Tree: best criterion, max_depth, min_samples_split
- Random Forest: best n_estimators using OOB + depth search
- Accuracy, Precision, Recall, F1
- Log Loss
- ROC-AUC
- Classification report
- Confusion matrices
- Feature importance
- Learning curve
- With PCA vs Without PCA comparison
- 2D PCA decision boundaries
- Final model comparison
- Best model selection

IMPORTANT:
Change only DATASET FILE and TARGET COLUMN when needed.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.base import clone

from sklearn.preprocessing import (
    StandardScaler,
    LabelEncoder
)

from sklearn.model_selection import (
    train_test_split,
    GridSearchCV,
    cross_val_score,
    learning_curve,
    StratifiedKFold
)

from sklearn.decomposition import PCA

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    roc_auc_score,
    classification_report,
    ConfusionMatrixDisplay
)

# Models
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


# =========================================================
# 1. LOAD DATASET
# =========================================================

df = pd.read_csv("wine.csv")

TARGET = "target"

print("First 5 rows:")
print(df.head())

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())


# =========================================================
# 2. DATA VALIDATION
# =========================================================

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("\nTarget Distribution:")
print(df[TARGET].value_counts())


# =========================================================
# 3. HANDLE MISSING VALUES AND DUPLICATES
# =========================================================

# Simple exam-friendly method:
df = df.dropna()
df = df.drop_duplicates()

# Alternative:
# Numeric missing value:
# df["Age"] = df["Age"].fillna(df["Age"].median())
#
# Categorical missing value:
# df["Gender"] = df["Gender"].fillna(df["Gender"].mode()[0])


# =========================================================
# 4. SEPARATE X AND y
# =========================================================

X = df.drop(columns=[TARGET])
y = df[TARGET]


# =========================================================
# 5. ENCODE CATEGORICAL FEATURES
# =========================================================

# Converts categorical input features into numeric columns.
# If all features are already numeric, nothing harmful happens.

X = pd.get_dummies(
    X,
    drop_first=True,
    dtype=int
)

print("\nProcessed Feature Shape:")
print(X.shape)


# =========================================================
# 6. ENCODE TARGET
# =========================================================

encoder = LabelEncoder()

y = encoder.fit_transform(y)

print("\nEncoded Classes:")
print(dict(
    zip(
        encoder.classes_,
        encoder.transform(encoder.classes_)
    )
))


# =========================================================
# 7. TRAIN-TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("\nTrain Shape:", X_train.shape)
print("Test Shape :", X_test.shape)


# =========================================================
# 8. CROSS-VALIDATION SETUP
# =========================================================

# Prevents the common warning:
# "least populated class has fewer members than n_splits"

minimum_class_count = pd.Series(
    y_train
).value_counts().min()

cv_splits = min(
    5,
    int(minimum_class_count)
)

if cv_splits < 2:
    raise ValueError(
        "Each class needs at least 2 training samples "
        "for cross-validation."
    )

cv = StratifiedKFold(
    n_splits=cv_splits,
    shuffle=True,
    random_state=42
)

print("\nCross-validation folds:", cv_splits)


# =========================================================
# 9. SCALING
# =========================================================

# Scaling is important for:
# Logistic Regression
# KNN
# SVM
# PCA
#
# Scaling is usually NOT required for:
# Decision Tree
# Random Forest

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train
)

X_test_scaled = scaler.transform(
    X_test
)


# =========================================================
# 10. PCA - 2D VISUALIZATION
# =========================================================

# Use the scaler fitted on training data.

X_all_scaled = scaler.transform(X)

pca_visual = PCA(
    n_components=2
)

X_pca_visual = pca_visual.fit_transform(
    X_all_scaled
)

plt.figure(figsize=(8, 6))

plt.scatter(
    X_pca_visual[:, 0],
    X_pca_visual[:, 1],
    c=y
)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Dataset Visualization")
plt.savefig("01_pca_visualization.png")
plt.show()

print(
    "\nPCA 2D Explained Variance:",
    pca_visual.explained_variance_ratio_
)

print(
    "Total Explained Variance:",
    pca_visual.explained_variance_ratio_.sum()
)


# =========================================================
# 11. PCA - EXPLAINED VARIANCE
# =========================================================

pca_full = PCA()

pca_full.fit(
    X_train_scaled
)

explained_variance = (
    pca_full.explained_variance_ratio_
)

cumulative_variance = np.cumsum(
    explained_variance
)

components = np.arange(
    1,
    len(explained_variance) + 1
)


plt.figure(figsize=(8, 6))

plt.bar(
    components,
    explained_variance
)

plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("PCA Explained Variance")
plt.savefig("02_pca_explained_variance.png")
plt.show()


plt.figure(figsize=(8, 6))

plt.plot(
    components,
    cumulative_variance,
    marker="o"
)

plt.axhline(
    0.95,
    linestyle="--",
    label="95% Variance"
)

plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.title("PCA Cumulative Explained Variance")
plt.legend()
plt.grid()
plt.savefig("03_pca_cumulative_variance.png")
plt.show()


best_pca_components = np.argmax(
    cumulative_variance >= 0.95
) + 1

print(
    "\nComponents needed for 95% variance:",
    best_pca_components
)


# =========================================================
# 12. LOGISTIC REGRESSION - FIND BEST C
# =========================================================

logistic_C_values = [
    0.001,
    0.01,
    0.1,
    1,
    10,
    100
]

logistic_cv_scores = []


for C in logistic_C_values:

    model = LogisticRegression(
        C=C,
        max_iter=2000,
        random_state=42
    )

    scores = cross_val_score(
        model,
        X_train_scaled,
        y_train,
        cv=cv,
        scoring="accuracy"
    )

    logistic_cv_scores.append(
        scores.mean()
    )


best_logistic_C = logistic_C_values[
    np.argmax(logistic_cv_scores)
]


print(
    "\nBest Logistic Regression C:",
    best_logistic_C
)


plt.figure(figsize=(8, 6))

plt.semilogx(
    logistic_C_values,
    logistic_cv_scores,
    marker="o"
)

plt.xlabel("C")
plt.ylabel("Mean CV Accuracy")
plt.title("Logistic Regression: C Selection")
plt.grid()
plt.savefig("04_logistic_C_selection.png")
plt.show()


# =========================================================
# 13. FINAL LOGISTIC REGRESSION
# =========================================================

logistic = LogisticRegression(
    C=best_logistic_C,
    max_iter=2000,
    random_state=42
)

logistic.fit(
    X_train_scaled,
    y_train
)

y_pred_logistic = logistic.predict(
    X_test_scaled
)

y_prob_logistic = logistic.predict_proba(
    X_test_scaled
)


print(
    "\n========== LOGISTIC REGRESSION =========="
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred_logistic
    )
)

print(
    classification_report(
        y_test,
        y_pred_logistic,
        zero_division=0
    )
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_logistic
)

plt.title("Logistic Regression")
plt.savefig("05_logistic_confusion.png")
plt.show()


# =========================================================
# 14. KNN - FIND BEST K
# =========================================================

maximum_k = min(
    40,
    len(X_train) - 1
)

k_values = range(
    1,
    maximum_k + 1
)

knn_cv_scores = []


for k in k_values:

    model = KNeighborsClassifier(
        n_neighbors=k
    )

    scores = cross_val_score(
        model,
        X_train_scaled,
        y_train,
        cv=cv,
        scoring="accuracy"
    )

    knn_cv_scores.append(
        scores.mean()
    )


best_k = list(k_values)[
    np.argmax(knn_cv_scores)
]


print("\nBest K:", best_k)


plt.figure(figsize=(8, 6))

plt.plot(
    k_values,
    knn_cv_scores,
    marker="o"
)

plt.xlabel("K")
plt.ylabel("Mean CV Accuracy")
plt.title("KNN: Accuracy vs K")
plt.grid()
plt.savefig("06_knn_k_selection.png")
plt.show()


# =========================================================
# 15. FINAL KNN
# =========================================================

knn = KNeighborsClassifier(
    n_neighbors=best_k
)

knn.fit(
    X_train_scaled,
    y_train
)

y_pred_knn = knn.predict(
    X_test_scaled
)

y_prob_knn = knn.predict_proba(
    X_test_scaled
)


print("\n========== KNN ==========")

print(
    "Best K:",
    best_k
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred_knn
    )
)

print(
    classification_report(
        y_test,
        y_pred_knn,
        zero_division=0
    )
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_knn
)

plt.title("KNN")
plt.savefig("07_knn_confusion.png")
plt.show()


# =========================================================
# 16. SVM - FIND BEST PARAMETERS
# =========================================================

# Linear kernel does not need gamma.
# RBF kernel needs both C and gamma.

svm_parameter_grid = [

    {
        "kernel": ["linear"],
        "C": [
            0.1,
            1,
            10,
            100
        ]
    },

    {
        "kernel": ["rbf"],
        "C": [
            0.1,
            1,
            10,
            100
        ],
        "gamma": [
            "scale",
            "auto",
            0.01,
            0.1,
            1
        ]
    }
]


svm_search = GridSearchCV(
    SVC(
        probability=True,
        random_state=42
    ),
    param_grid=svm_parameter_grid,
    cv=cv,
    scoring="accuracy",
    n_jobs=-1
)

svm_search.fit(
    X_train_scaled,
    y_train
)


print(
    "\nBest SVM Parameters:",
    svm_search.best_params_
)

print(
    "Best SVM CV Accuracy:",
    svm_search.best_score_
)


# =========================================================
# 17. FINAL SVM
# =========================================================

svm = svm_search.best_estimator_

y_pred_svm = svm.predict(
    X_test_scaled
)

y_prob_svm = svm.predict_proba(
    X_test_scaled
)


print("\n========== SVM ==========")

print(
    "Best Parameters:",
    svm_search.best_params_
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred_svm
    )
)

print(
    classification_report(
        y_test,
        y_pred_svm,
        zero_division=0
    )
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_svm
)

plt.title("SVM")
plt.savefig("08_svm_confusion.png")
plt.show()


# =========================================================
# 18. NAIVE BAYES - FIND BEST var_smoothing
# =========================================================

nb_values = np.logspace(
    -12,
    -6,
    13
)

nb_cv_scores = []


for value in nb_values:

    model = GaussianNB(
        var_smoothing=value
    )

    scores = cross_val_score(
        model,
        X_train_scaled,
        y_train,
        cv=cv,
        scoring="accuracy"
    )

    nb_cv_scores.append(
        scores.mean()
    )


best_nb_smoothing = nb_values[
    np.argmax(nb_cv_scores)
]


print(
    "\nBest Naive Bayes var_smoothing:",
    best_nb_smoothing
)


plt.figure(figsize=(8, 6))

plt.semilogx(
    nb_values,
    nb_cv_scores,
    marker="o"
)

plt.xlabel("var_smoothing")
plt.ylabel("Mean CV Accuracy")
plt.title("Naive Bayes: var_smoothing Selection")
plt.grid()
plt.savefig("09_naive_bayes_smoothing.png")
plt.show()


# =========================================================
# 19. FINAL NAIVE BAYES
# =========================================================

nb = GaussianNB(
    var_smoothing=best_nb_smoothing
)

nb.fit(
    X_train_scaled,
    y_train
)

y_pred_nb = nb.predict(
    X_test_scaled
)

y_prob_nb = nb.predict_proba(
    X_test_scaled
)


print(
    "\n========== NAIVE BAYES =========="
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred_nb
    )
)

print(
    classification_report(
        y_test,
        y_pred_nb,
        zero_division=0
    )
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_nb
)

plt.title("Naive Bayes")
plt.savefig("10_naive_bayes_confusion.png")
plt.show()


# =========================================================
# 20. DECISION TREE - DEPTH GRAPH
# =========================================================

depth_values = range(
    1,
    16
)

dt_depth_scores = []


for depth in depth_values:

    model = DecisionTreeClassifier(
        max_depth=depth,
        random_state=42
    )

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="accuracy"
    )

    dt_depth_scores.append(
        scores.mean()
    )


plt.figure(figsize=(8, 6))

plt.plot(
    depth_values,
    dt_depth_scores,
    marker="o"
)

plt.xlabel("max_depth")
plt.ylabel("Mean CV Accuracy")
plt.title("Decision Tree: Depth Selection")
plt.grid()
plt.savefig("11_decision_tree_depth.png")
plt.show()


# =========================================================
# 21. DECISION TREE - GRID SEARCH
# =========================================================

dt_parameter_grid = {

    "criterion": [
        "gini",
        "entropy"
    ],

    "max_depth": [
        None,
        2,
        3,
        4,
        5,
        6,
        8,
        10,
        15
    ],

    "min_samples_split": [
        2,
        5,
        10
    ],

    "min_samples_leaf": [
        1,
        2,
        4
    ]
}


dt_search = GridSearchCV(
    DecisionTreeClassifier(
        random_state=42
    ),
    param_grid=dt_parameter_grid,
    cv=cv,
    scoring="accuracy",
    n_jobs=-1
)

dt_search.fit(
    X_train,
    y_train
)


print(
    "\nBest Decision Tree Parameters:",
    dt_search.best_params_
)

print(
    "Best Decision Tree CV Accuracy:",
    dt_search.best_score_
)


# =========================================================
# 22. FINAL DECISION TREE
# =========================================================

dt = dt_search.best_estimator_

y_pred_dt = dt.predict(
    X_test
)

y_prob_dt = dt.predict_proba(
    X_test
)


print(
    "\n========== DECISION TREE =========="
)

print(
    "Best Parameters:",
    dt_search.best_params_
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred_dt
    )
)

print(
    classification_report(
        y_test,
        y_pred_dt,
        zero_division=0
    )
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_dt
)

plt.title("Decision Tree")
plt.savefig("12_decision_tree_confusion.png")
plt.show()


# =========================================================
# 23. DECISION TREE FEATURE IMPORTANCE
# =========================================================

dt_importance = pd.Series(
    dt.feature_importances_,
    index=X.columns
).sort_values(
    ascending=False
)

print(
    "\nDecision Tree Feature Importance:"
)

print(dt_importance)


plt.figure(figsize=(10, 6))

dt_importance.head(15).plot(
    kind="bar"
)

plt.ylabel("Importance")
plt.title("Decision Tree Feature Importance")
plt.tight_layout()
plt.savefig("13_decision_tree_importance.png")
plt.show()


# =========================================================
# 24. RANDOM FOREST - FIND BEST n_estimators USING OOB
# =========================================================

n_tree_values = range(
    50,
    501,
    50
)

rf_oob_scores = []


for n in n_tree_values:

    model = RandomForestClassifier(
        n_estimators=n,
        random_state=42,
        oob_score=True,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    rf_oob_scores.append(
        model.oob_score_
    )


best_n_estimators = list(
    n_tree_values
)[
    np.argmax(rf_oob_scores)
]


print(
    "\nBest Random Forest n_estimators:",
    best_n_estimators
)


plt.figure(figsize=(8, 6))

plt.plot(
    n_tree_values,
    rf_oob_scores,
    marker="o"
)

plt.xlabel("Number of Trees")
plt.ylabel("OOB Score")
plt.title("Random Forest: OOB Score vs n_estimators")
plt.grid()
plt.savefig("14_random_forest_oob.png")
plt.show()


# =========================================================
# 25. RANDOM FOREST - FIND BEST max_depth
# =========================================================

rf_depth_values = [
    None,
    3,
    5,
    7,
    10,
    15,
    20
]

rf_depth_scores = []


for depth in rf_depth_values:

    model = RandomForestClassifier(
        n_estimators=best_n_estimators,
        max_depth=depth,
        random_state=42,
        n_jobs=-1
    )

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="accuracy",
        n_jobs=-1
    )

    rf_depth_scores.append(
        scores.mean()
    )


best_rf_depth = rf_depth_values[
    np.argmax(rf_depth_scores)
]


print(
    "Best Random Forest max_depth:",
    best_rf_depth
)


# =========================================================
# 26. FINAL RANDOM FOREST
# =========================================================

rf = RandomForestClassifier(
    n_estimators=best_n_estimators,
    max_depth=best_rf_depth,
    random_state=42,
    oob_score=True,
    n_jobs=-1
)

rf.fit(
    X_train,
    y_train
)

y_pred_rf = rf.predict(
    X_test
)

y_prob_rf = rf.predict_proba(
    X_test
)


print(
    "\n========== RANDOM FOREST =========="
)

print(
    "Best n_estimators:",
    best_n_estimators
)

print(
    "Best max_depth:",
    best_rf_depth
)

print(
    "Accuracy:",
    accuracy_score(
        y_test,
        y_pred_rf
    )
)

print(
    "OOB Score:",
    rf.oob_score_
)

print(
    classification_report(
        y_test,
        y_pred_rf,
        zero_division=0
    )
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_rf
)

plt.title("Random Forest")
plt.savefig("15_random_forest_confusion.png")
plt.show()


# =========================================================
# 27. RANDOM FOREST FEATURE IMPORTANCE
# =========================================================

rf_importance = pd.Series(
    rf.feature_importances_,
    index=X.columns
).sort_values(
    ascending=False
)

print(
    "\nRandom Forest Feature Importance:"
)

print(rf_importance)


plt.figure(figsize=(10, 6))

rf_importance.head(15).plot(
    kind="bar"
)

plt.ylabel("Importance")
plt.title("Random Forest Feature Importance")
plt.tight_layout()
plt.savefig("16_random_forest_importance.png")
plt.show()


# =========================================================
# 28. HELPER FUNCTION FOR ROC-AUC
# =========================================================

def calculate_auc(
    y_true_value,
    probabilities
):

    try:

        number_of_classes = len(
            np.unique(y_true_value)
        )

        if number_of_classes == 2:

            return roc_auc_score(
                y_true_value,
                probabilities[:, 1]
            )

        return roc_auc_score(
            y_true_value,
            probabilities,
            multi_class="ovr",
            average="weighted"
        )

    except ValueError:

        return np.nan


# =========================================================
# 29. CALCULATE ALL METRICS
# =========================================================

predictions = {

    "Logistic Regression":
        y_pred_logistic,

    "KNN":
        y_pred_knn,

    "SVM":
        y_pred_svm,

    "Naive Bayes":
        y_pred_nb,

    "Decision Tree":
        y_pred_dt,

    "Random Forest":
        y_pred_rf
}


probabilities = {

    "Logistic Regression":
        y_prob_logistic,

    "KNN":
        y_prob_knn,

    "SVM":
        y_prob_svm,

    "Naive Bayes":
        y_prob_nb,

    "Decision Tree":
        y_prob_dt,

    "Random Forest":
        y_prob_rf
}


results_list = []


for name in predictions:

    pred = predictions[name]
    prob = probabilities[name]

    accuracy = accuracy_score(
        y_test,
        pred
    )

    precision = precision_score(
        y_test,
        pred,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        pred,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        pred,
        average="weighted",
        zero_division=0
    )

    loss = log_loss(
        y_test,
        prob,
        labels=np.arange(
            len(encoder.classes_)
        )
    )

    auc = calculate_auc(
        y_test,
        prob
    )

    results_list.append([
        name,
        accuracy,
        precision,
        recall,
        f1,
        loss,
        auc
    ])


results = pd.DataFrame(
    results_list,
    columns=[
        "Model",
        "Accuracy",
        "Precision",
        "Recall",
        "F1",
        "Log Loss",
        "ROC-AUC"
    ]
)


print(
    "\n========== FINAL RESULT TABLE =========="
)

print(
    results.sort_values(
        "Accuracy",
        ascending=False
    )
)


# =========================================================
# 30. FIND BEST MODEL
# =========================================================

best_index = results[
    "Accuracy"
].idxmax()

best_model_name = results.loc[
    best_index,
    "Model"
]

best_accuracy = results.loc[
    best_index,
    "Accuracy"
]


print(
    "\nBest Model:",
    best_model_name
)

print(
    "Best Accuracy:",
    best_accuracy
)


# =========================================================
# 31. MODEL ACCURACY COMPARISON GRAPH
# =========================================================

plt.figure(figsize=(10, 6))

plt.bar(
    results["Model"],
    results["Accuracy"]
)

plt.ylabel("Accuracy")
plt.title("Model Accuracy Comparison")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("17_model_accuracy_comparison.png")
plt.show()


# =========================================================
# 32. F1 SCORE COMPARISON GRAPH
# =========================================================

plt.figure(figsize=(10, 6))

plt.bar(
    results["Model"],
    results["F1"]
)

plt.ylabel("Weighted F1 Score")
plt.title("Model F1 Score Comparison")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("18_model_f1_comparison.png")
plt.show()


# =========================================================
# 33. LOG LOSS COMPARISON GRAPH
# =========================================================

# Lower log loss is better.

plt.figure(figsize=(10, 6))

plt.bar(
    results["Model"],
    results["Log Loss"]
)

plt.ylabel("Log Loss")
plt.title("Model Log Loss Comparison")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("19_model_logloss_comparison.png")
plt.show()


# =========================================================
# 34. PCA WITH 95% VARIANCE
# =========================================================

pca_95 = PCA(
    n_components=0.95
)

X_train_pca = pca_95.fit_transform(
    X_train_scaled
)

X_test_pca = pca_95.transform(
    X_test_scaled
)


print(
    "\nPCA Original Features:",
    X_train_scaled.shape[1]
)

print(
    "PCA Reduced Features:",
    X_train_pca.shape[1]
)

print(
    "PCA Total Explained Variance:",
    pca_95.explained_variance_ratio_.sum()
)


# =========================================================
# 35. WITHOUT PCA VS WITH PCA
# =========================================================

final_models = {

    "Logistic Regression":
        logistic,

    "KNN":
        knn,

    "SVM":
        svm,

    "Naive Bayes":
        nb,

    "Decision Tree":
        dt,

    "Random Forest":
        rf
}


without_pca_accuracy = dict(
    zip(
        results["Model"],
        results["Accuracy"]
    )
)


with_pca_accuracy = {}


for name, model in final_models.items():

    pca_model = clone(model)

    pca_model.fit(
        X_train_pca,
        y_train
    )

    pca_pred = pca_model.predict(
        X_test_pca
    )

    with_pca_accuracy[name] = accuracy_score(
        y_test,
        pca_pred
    )


pca_comparison = pd.DataFrame({

    "Model":
        list(final_models.keys()),

    "Without PCA":
        [
            without_pca_accuracy[name]
            for name in final_models
        ],

    "With PCA":
        [
            with_pca_accuracy[name]
            for name in final_models
        ]
})


print(
    "\n========== PCA COMPARISON =========="
)

print(pca_comparison)


x_position = np.arange(
    len(pca_comparison)
)

width = 0.35


plt.figure(figsize=(11, 6))

plt.bar(
    x_position - width / 2,
    pca_comparison["Without PCA"],
    width,
    label="Without PCA"
)

plt.bar(
    x_position + width / 2,
    pca_comparison["With PCA"],
    width,
    label="With PCA"
)

plt.xticks(
    x_position,
    pca_comparison["Model"],
    rotation=30
)

plt.ylabel("Accuracy")
plt.title("Accuracy: Without PCA vs With PCA")
plt.legend()
plt.tight_layout()
plt.savefig("20_pca_accuracy_comparison.png")
plt.show()


# =========================================================
# 36. 2D PCA FOR DECISION BOUNDARIES
# =========================================================

pca_2d = PCA(
    n_components=2
)

X_train_2d = pca_2d.fit_transform(
    X_train_scaled
)

X_test_2d = pca_2d.transform(
    X_test_scaled
)


# =========================================================
# 37. DECISION BOUNDARY FUNCTION
# =========================================================

def plot_decision_boundary(
    model,
    model_name
):

    model_2d = clone(model)

    model_2d.fit(
        X_train_2d,
        y_train
    )

    x_min = (
        X_train_2d[:, 0].min() - 1
    )

    x_max = (
        X_train_2d[:, 0].max() + 1
    )

    y_min = (
        X_train_2d[:, 1].min() - 1
    )

    y_max = (
        X_train_2d[:, 1].max() + 1
    )

    xx, yy = np.meshgrid(
        np.linspace(
            x_min,
            x_max,
            300
        ),
        np.linspace(
            y_min,
            y_max,
            300
        )
    )

    grid = np.c_[
        xx.ravel(),
        yy.ravel()
    ]

    Z = model_2d.predict(
        grid
    )

    Z = Z.reshape(
        xx.shape
    )

    plt.figure(figsize=(8, 6))

    plt.contourf(
        xx,
        yy,
        Z,
        alpha=0.25
    )

    plt.scatter(
        X_train_2d[:, 0],
        X_train_2d[:, 1],
        c=y_train
    )

    plt.xlabel("PC1")
    plt.ylabel("PC2")

    plt.title(
        model_name +
        " Decision Boundary"
    )

    file_name = (
        model_name
        .lower()
        .replace(" ", "_")
        + "_decision_boundary.png"
    )

    plt.savefig(file_name)
    plt.show()


# Draw one graph for each model.

for name, model in final_models.items():

    plot_decision_boundary(
        model,
        name
    )


# =========================================================
# 38. LEARNING CURVE FOR BEST MODEL
# =========================================================

# Select correct input:
# scaled input for distance / gradient based models
# unscaled input for tree based models

if best_model_name in [
    "Decision Tree",
    "Random Forest"
]:

    learning_X = X_train

else:

    learning_X = X_train_scaled


best_model_object = clone(
    final_models[
        best_model_name
    ]
)


train_sizes, train_scores, validation_scores = learning_curve(

    best_model_object,

    learning_X,

    y_train,

    cv=cv,

    scoring="accuracy",

    train_sizes=np.linspace(
        0.2,
        1.0,
        5
    ),

    n_jobs=-1
)


train_mean = train_scores.mean(
    axis=1
)

validation_mean = validation_scores.mean(
    axis=1
)


plt.figure(figsize=(8, 6))

plt.plot(
    train_sizes,
    train_mean,
    marker="o",
    label="Training Accuracy"
)

plt.plot(
    train_sizes,
    validation_mean,
    marker="o",
    label="Validation Accuracy"
)

plt.xlabel("Training Samples")
plt.ylabel("Accuracy")

plt.title(
    best_model_name +
    " Learning Curve"
)

plt.legend()
plt.grid()
plt.savefig("21_best_model_learning_curve.png")
plt.show()


# =========================================================
# 39. LOGISTIC REGRESSION COEFFICIENT IMPORTANCE
# =========================================================

# For multiclass logistic regression:
# take mean absolute coefficient across all classes.

logistic_importance = np.mean(
    np.abs(logistic.coef_),
    axis=0
)

logistic_importance = pd.Series(
    logistic_importance,
    index=X.columns
).sort_values(
    ascending=False
)


print(
    "\nLogistic Regression Feature Importance:"
)

print(logistic_importance)


# =========================================================
# 40. SAVE RESULTS
# =========================================================

results.to_csv(
    "supervised_model_results.csv",
    index=False
)

pca_comparison.to_csv(
    "pca_model_comparison.csv",
    index=False
)

dt_importance.to_csv(
    "decision_tree_feature_importance.csv"
)

rf_importance.to_csv(
    "random_forest_feature_importance.csv"
)

logistic_importance.to_csv(
    "logistic_feature_importance.csv"
)


# =========================================================
# 41. FINAL SUMMARY
# =========================================================

print(
    "\n========== FINAL SUMMARY =========="
)

print(
    "Logistic Best C:",
    best_logistic_C
)

print(
    "KNN Best K:",
    best_k
)

print(
    "SVM Best Parameters:",
    svm_search.best_params_
)

print(
    "Naive Bayes Best var_smoothing:",
    best_nb_smoothing
)

print(
    "Decision Tree Best Parameters:",
    dt_search.best_params_
)

print(
    "Random Forest Best n_estimators:",
    best_n_estimators
)

print(
    "Random Forest Best max_depth:",
    best_rf_depth
)

print(
    "Random Forest OOB Score:",
    rf.oob_score_
)

print(
    "PCA Components for 95% Variance:",
    best_pca_components
)

print(
    "Best Model:",
    best_model_name
)

print(
    "Best Test Accuracy:",
    best_accuracy
)

print(
    "\nAll graphs and CSV result files saved successfully."
)
