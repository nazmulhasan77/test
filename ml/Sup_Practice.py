import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA

from sklearn.metrics import (
    accuracy_score,
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
# 1. Load Dataset
# =========================================================

df = pd.read_csv("wine.csv")

print(df.head())
print(df.shape)


# =========================================================
# 2. Check Missing and Duplicate
# =========================================================

print(df.isnull().sum())
print("Duplicate:", df.duplicated().sum())


# =========================================================
# 3. Remove Missing and Duplicate
# =========================================================

df = df.dropna()
df = df.drop_duplicates()


# =========================================================
# 4. Separate X and Y
# =========================================================

x = df.drop("target", axis=1)
y = df["target"]

print(x.head())
print(y.head())


# =========================================================
# 5. Encode Target
# =========================================================

encoder = LabelEncoder()

y = encoder.fit_transform(y)


# =========================================================
# 6. Train Test Split
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    x,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)


# =========================================================
# 7. Scaling
# =========================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# =========================================================
# 8. PCA Visualization
# =========================================================

x_scaled = scaler.fit_transform(x)

pca = PCA(n_components=2)

x_pca = pca.fit_transform(x_scaled)

plt.figure(figsize=(7, 5))

plt.scatter(
    x_pca[:, 0],
    x_pca[:, 1],
    c=y
)

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Wine Dataset")

plt.savefig("pca.png")
plt.show()


# =========================================================
# 9. Logistic Regression
# =========================================================

logistic = LogisticRegression(
    max_iter=1000,
    random_state=42
)

logistic.fit(X_train_scaled, y_train)

y_pred_logistic = logistic.predict(X_test_scaled)

print("\n========== Logistic Regression ==========")

print("Accuracy:",
      accuracy_score(y_test, y_pred_logistic))

print(classification_report(
    y_test,
    y_pred_logistic
))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_logistic
)

plt.title("Logistic Regression")
plt.savefig("logistic_confusion.png")
plt.show()


# =========================================================
# 10. KNN
# =========================================================

knn = KNeighborsClassifier(
    n_neighbors=5
)

knn.fit(X_train_scaled, y_train)

y_pred_knn = knn.predict(X_test_scaled)

print("\n========== KNN ==========")

print("Accuracy:",
      accuracy_score(y_test, y_pred_knn))

print(classification_report(
    y_test,
    y_pred_knn
))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_knn
)

plt.title("KNN")
plt.savefig("knn_confusion.png")
plt.show()


# =========================================================
# 11. SVM
# =========================================================

svm = SVC(
    kernel="rbf"
)

svm.fit(X_train_scaled, y_train)

y_pred_svm = svm.predict(X_test_scaled)

print("\n========== SVM ==========")

print("Accuracy:",
      accuracy_score(y_test, y_pred_svm))

print(classification_report(
    y_test,
    y_pred_svm
))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_svm
)

plt.title("SVM")
plt.savefig("svm_confusion.png")
plt.show()


# =========================================================
# 12. Naive Bayes
# =========================================================

nb = GaussianNB()

nb.fit(X_train_scaled, y_train)

y_pred_nb = nb.predict(X_test_scaled)

print("\n========== Naive Bayes ==========")

print("Accuracy:",
      accuracy_score(y_test, y_pred_nb))

print(classification_report(
    y_test,
    y_pred_nb
))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_nb
)

plt.title("Naive Bayes")
plt.savefig("naive_bayes_confusion.png")
plt.show()


# =========================================================
# 13. Decision Tree
# =========================================================

# Decision Tree does not require scaling

dt = DecisionTreeClassifier(
    random_state=42
)

dt.fit(X_train, y_train)

y_pred_dt = dt.predict(X_test)

print("\n========== Decision Tree ==========")

print("Accuracy:",
      accuracy_score(y_test, y_pred_dt))

print(classification_report(
    y_test,
    y_pred_dt
))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_dt
)

plt.title("Decision Tree")
plt.savefig("decision_tree_confusion.png")
plt.show()


# =========================================================
# 14. Random Forest
# =========================================================

# Random Forest does not require scaling

rf = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    oob_score=True
)

rf.fit(X_train, y_train)

y_pred_rf = rf.predict(X_test)

print("\n========== Random Forest ==========")

print("Accuracy:",
      accuracy_score(y_test, y_pred_rf))

print(classification_report(
    y_test,
    y_pred_rf
))

print("OOB Score:",
      rf.oob_score_)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred_rf
)

plt.title("Random Forest")
plt.savefig("random_forest_confusion.png")
plt.show()


# =========================================================
# 15. Random Forest Feature Importance
# =========================================================

importance = pd.Series(
    rf.feature_importances_,
    index=x.columns
).sort_values(ascending=False)

print("\nFeature Importance:")

print(importance)


# =========================================================
# 16. Compare All Models
# =========================================================

logistic_accuracy = accuracy_score(
    y_test,
    y_pred_logistic
)

knn_accuracy = accuracy_score(
    y_test,
    y_pred_knn
)

svm_accuracy = accuracy_score(
    y_test,
    y_pred_svm
)

nb_accuracy = accuracy_score(
    y_test,
    y_pred_nb
)

dt_accuracy = accuracy_score(
    y_test,
    y_pred_dt
)

rf_accuracy = accuracy_score(
    y_test,
    y_pred_rf
)


print("\n========== Model Comparison ==========")

print("Logistic Regression :", logistic_accuracy)
print("KNN                 :", knn_accuracy)
print("SVM                 :", svm_accuracy)
print("Naive Bayes         :", nb_accuracy)
print("Decision Tree       :", dt_accuracy)
print("Random Forest       :", rf_accuracy)


# =========================================================
# 17. Find Best Model
# =========================================================

models = {
    "Logistic Regression": logistic_accuracy,
    "KNN": knn_accuracy,
    "SVM": svm_accuracy,
    "Naive Bayes": nb_accuracy,
    "Decision Tree": dt_accuracy,
    "Random Forest": rf_accuracy
}

best_model = max(
    models,
    key=models.get
)

print("\nBest Model:", best_model)
print("Best Accuracy:", models[best_model])