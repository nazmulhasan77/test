"""
UNSUPERVISED ML LAB MASTER FILE

Models:
1. K-Means
2. Hierarchical / Agglomerative Clustering
3. DBSCAN
4. Gaussian Mixture Model (GMM)
5. PCA

Metrics:
- Adjusted Rand Index (ARI)
- Adjusted Mutual Information (AMI)
- Normalized Mutual Information (NMI)
- Silhouette Score
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.metrics import (
    adjusted_rand_score,
    adjusted_mutual_info_score,
    normalized_mutual_info_score,
    silhouette_score
)
from scipy.cluster.hierarchy import linkage, dendrogram


# =========================================================
# 1. CREATE DATASET
# =========================================================

X, y_true = make_blobs(
    n_samples=600,
    centers=[(0, 0), (5, 5), (0, 6)],
    cluster_std=[0.8, 1.2, 0.7],
    random_state=42
)

print("Dataset Shape:", X.shape)


# =========================================================
# 2. ORIGINAL DATASET VISUALIZATION
# =========================================================

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=y_true)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Original Dataset")
plt.savefig("original_data.png")
plt.show()


# =========================================================
# 3. K-MEANS
# =========================================================

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

kmeans_label = kmeans.fit_predict(X)

kmeans_ari = adjusted_rand_score(y_true, kmeans_label)
kmeans_ami = adjusted_mutual_info_score(y_true, kmeans_label)
kmeans_nmi = normalized_mutual_info_score(y_true, kmeans_label)
kmeans_silhouette = silhouette_score(X, kmeans_label)

print("\n========== K-MEANS ==========")
print("ARI        :", kmeans_ari)
print("AMI        :", kmeans_ami)
print("NMI        :", kmeans_nmi)
print("Silhouette :", kmeans_silhouette)

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=kmeans_label)
plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    marker="X",
    s=200,
    label="Centroids"
)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("K-Means Clustering")
plt.legend()
plt.savefig("kmeans.png")
plt.show()


# =========================================================
# 4. HIERARCHICAL CLUSTERING
# =========================================================

hierarchical = AgglomerativeClustering(
    n_clusters=3
)

hierarchical_label = hierarchical.fit_predict(X)

hierarchical_ari = adjusted_rand_score(y_true, hierarchical_label)
hierarchical_ami = adjusted_mutual_info_score(y_true, hierarchical_label)
hierarchical_nmi = normalized_mutual_info_score(y_true, hierarchical_label)
hierarchical_silhouette = silhouette_score(X, hierarchical_label)

print("\n========== HIERARCHICAL ==========")
print("ARI        :", hierarchical_ari)
print("AMI        :", hierarchical_ami)
print("NMI        :", hierarchical_nmi)
print("Silhouette :", hierarchical_silhouette)

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=hierarchical_label)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Hierarchical Clustering")
plt.savefig("hierarchical.png")
plt.show()

# Dendrogram
linked = linkage(X, method="ward")

plt.figure(figsize=(12, 6))
dendrogram(linked)
plt.xlabel("Data Points")
plt.ylabel("Distance")
plt.title("Hierarchical Dendrogram")
plt.savefig("dendrogram.png")
plt.show()


# =========================================================
# 5. DBSCAN
# =========================================================

dbscan = DBSCAN(
    eps=0.5,
    min_samples=5
)

dbscan_label = dbscan.fit_predict(X)

dbscan_ari = adjusted_rand_score(y_true, dbscan_label)
dbscan_ami = adjusted_mutual_info_score(y_true, dbscan_label)
dbscan_nmi = normalized_mutual_info_score(y_true, dbscan_label)

print("\n========== DBSCAN ==========")
print("ARI :", dbscan_ari)
print("AMI :", dbscan_ami)
print("NMI :", dbscan_nmi)

unique_labels = set(dbscan_label)
number_of_clusters = len(unique_labels)

if -1 in unique_labels:
    number_of_clusters = number_of_clusters - 1

number_of_noise = list(dbscan_label).count(-1)

print("Number of Clusters :", number_of_clusters)
print("Noise Points       :", number_of_noise)

# Silhouette score after removing noise points (-1)
mask = dbscan_label != -1
clean_labels = dbscan_label[mask]

if len(set(clean_labels)) > 1:
    dbscan_silhouette = silhouette_score(
        X[mask],
        clean_labels
    )
    print("Silhouette :", dbscan_silhouette)
else:
    dbscan_silhouette = np.nan
    print("Silhouette cannot be calculated.")

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=dbscan_label)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("DBSCAN Clustering")
plt.savefig("dbscan.png")
plt.show()


# =========================================================
# 6. GAUSSIAN MIXTURE MODEL (GMM)
# =========================================================

gmm = GaussianMixture(
    n_components=3,
    random_state=42
)

gmm_label = gmm.fit_predict(X)

gmm_ari = adjusted_rand_score(y_true, gmm_label)
gmm_ami = adjusted_mutual_info_score(y_true, gmm_label)
gmm_nmi = normalized_mutual_info_score(y_true, gmm_label)
gmm_silhouette = silhouette_score(X, gmm_label)

print("\n========== GMM ==========")
print("ARI        :", gmm_ari)
print("AMI        :", gmm_ami)
print("NMI        :", gmm_nmi)
print("Silhouette :", gmm_silhouette)

plt.figure(figsize=(8, 6))
plt.scatter(X[:, 0], X[:, 1], c=gmm_label)
plt.scatter(
    gmm.means_[:, 0],
    gmm.means_[:, 1],
    marker="X",
    s=200,
    label="GMM Means"
)
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Gaussian Mixture Model")
plt.legend()
plt.savefig("gmm.png")
plt.show()


# =========================================================
# 7. PCA
# =========================================================

# PCA is not a clustering algorithm.
# It is used for dimensionality reduction.

pca = PCA(
    n_components=2
)

X_pca = pca.fit_transform(X)

print("\n========== PCA ==========")
print("Original Shape:", X.shape)
print("PCA Shape     :", X_pca.shape)
print("Explained Variance:", pca.explained_variance_ratio_)
print("Total Explained Variance:", pca.explained_variance_ratio_.sum())

plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_true)
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA Visualization")
plt.savefig("pca.png")
plt.show()


# =========================================================
# 8. FINAL COMPARISON
# =========================================================

print("\n========== ARI COMPARISON ==========")
print("K-Means      :", kmeans_ari)
print("Hierarchical :", hierarchical_ari)
print("DBSCAN       :", dbscan_ari)
print("GMM          :", gmm_ari)

ari_scores = {
    "K-Means": kmeans_ari,
    "Hierarchical": hierarchical_ari,
    "DBSCAN": dbscan_ari,
    "GMM": gmm_ari
}

best_model = max(
    ari_scores,
    key=ari_scores.get
)

print("\nBest Model:", best_model)
print("Best ARI  :", ari_scores[best_model])


# =========================================================
# 9. RESULT TABLE
# =========================================================

results = pd.DataFrame({
    "Model": [
        "K-Means",
        "Hierarchical",
        "DBSCAN",
        "GMM"
    ],
    "ARI": [
        kmeans_ari,
        hierarchical_ari,
        dbscan_ari,
        gmm_ari
    ],
    "AMI": [
        kmeans_ami,
        hierarchical_ami,
        dbscan_ami,
        gmm_ami
    ],
    "NMI": [
        kmeans_nmi,
        hierarchical_nmi,
        dbscan_nmi,
        gmm_nmi
    ],
    "Silhouette": [
        kmeans_silhouette,
        hierarchical_silhouette,
        dbscan_silhouette,
        gmm_silhouette
    ]
})

print("\n========== FINAL RESULT TABLE ==========")
print(results)
