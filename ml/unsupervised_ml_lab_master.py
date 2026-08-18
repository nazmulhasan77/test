"""
UNSUPERVISED ML LAB MASTER FILE

Models:
1. K-Means
2. Hierarchical / Agglomerative Clustering
3. DBSCAN
4. Gaussian Mixture Model (GMM)
5. PCA

Model Selection / Graphs:
- K-Means: Elbow + Silhouette vs K
- Hierarchical: Dendrogram + Silhouette vs K + Linkage comparison
- DBSCAN: K-distance graph + eps/min_samples search
- GMM: AIC + BIC + Silhouette vs components + covariance-type comparison
- PCA: Explained variance + cumulative explained variance

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
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

from sklearn.metrics import (
    adjusted_rand_score,
    adjusted_mutual_info_score,
    normalized_mutual_info_score,
    silhouette_score
)

from scipy.cluster.hierarchy import linkage, dendrogram


# =========================================================
# 1. CREATE / LOAD DATASET
# =========================================================

X, y_true = make_blobs(
    n_samples=600,
    centers=[(0, 0), (5, 5), (0, 6)],
    cluster_std=[0.8, 1.2, 0.7],
    random_state=42
)

# For CSV dataset, use something like:
#
# df = pd.read_csv("data.csv")
# X = df.drop(columns=["Class"]).values
# y_true = df["Class"].values
#
# If true labels are NOT provided:
# X = df.values
# y_true = None

print("Dataset Shape:", X.shape)


# =========================================================
# 2. SCALE DATA
# =========================================================

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# =========================================================
# 3. ORIGINAL DATASET VISUALIZATION
# =========================================================

plt.figure(figsize=(8, 6))

if X_scaled.shape[1] >= 2:
    if y_true is not None:
        plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y_true)
    else:
        plt.scatter(X_scaled[:, 0], X_scaled[:, 1])

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Original Dataset")
plt.savefig("01_original_data.png")
plt.show()


# =========================================================
# 4. K-MEANS - ELBOW METHOD
# =========================================================

k_elbow = range(1, 11)
inertia_values = []

for k in k_elbow:
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)
    inertia_values.append(model.inertia_)

plt.figure(figsize=(8, 6))
plt.plot(k_elbow, inertia_values, marker="o")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia / WCSS")
plt.title("K-Means Elbow Method")
plt.xticks(k_elbow)
plt.grid()
plt.savefig("02_kmeans_elbow.png")
plt.show()


# =========================================================
# 5. K-MEANS - SILHOUETTE METHOD
# =========================================================

k_values = range(2, 11)
kmeans_silhouette_scores = []

for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        labels
    )

    kmeans_silhouette_scores.append(score)


best_k_kmeans = list(k_values)[
    np.argmax(kmeans_silhouette_scores)
]

print("\nBest K for K-Means:", best_k_kmeans)


plt.figure(figsize=(8, 6))
plt.plot(
    k_values,
    kmeans_silhouette_scores,
    marker="o"
)
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.title("K-Means: Silhouette Score vs K")
plt.xticks(k_values)
plt.grid()
plt.savefig("03_kmeans_silhouette.png")
plt.show()


# =========================================================
# 6. FINAL K-MEANS MODEL
# =========================================================

kmeans = KMeans(
    n_clusters=best_k_kmeans,
    random_state=42,
    n_init=10
)

kmeans_label = kmeans.fit_predict(X_scaled)


kmeans_ari = adjusted_rand_score(
    y_true,
    kmeans_label
) if y_true is not None else np.nan

kmeans_ami = adjusted_mutual_info_score(
    y_true,
    kmeans_label
) if y_true is not None else np.nan

kmeans_nmi = normalized_mutual_info_score(
    y_true,
    kmeans_label
) if y_true is not None else np.nan

kmeans_silhouette = silhouette_score(
    X_scaled,
    kmeans_label
)


print("\n========== K-MEANS ==========")
print("Best K     :", best_k_kmeans)
print("ARI        :", kmeans_ari)
print("AMI        :", kmeans_ami)
print("NMI        :", kmeans_nmi)
print("Silhouette :", kmeans_silhouette)


plt.figure(figsize=(8, 6))

plt.scatter(
    X_scaled[:, 0],
    X_scaled[:, 1],
    c=kmeans_label
)

plt.scatter(
    kmeans.cluster_centers_[:, 0],
    kmeans.cluster_centers_[:, 1],
    marker="X",
    s=250,
    label="Centroids"
)

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("K-Means Clustering")
plt.legend()
plt.savefig("04_kmeans_final.png")
plt.show()


# =========================================================
# 7. HIERARCHICAL - DENDROGRAM
# =========================================================

linked = linkage(
    X_scaled,
    method="ward"
)

plt.figure(figsize=(12, 6))

dendrogram(
    linked,
    truncate_mode="level",
    p=5
)

plt.xlabel("Data Points / Clusters")
plt.ylabel("Distance")
plt.title("Hierarchical Dendrogram - Ward Linkage")
plt.savefig("05_hierarchical_dendrogram.png")
plt.show()

# For full dendrogram:
#
# dendrogram(linked)


# =========================================================
# 8. HIERARCHICAL - FIND BEST K AND LINKAGE
# =========================================================

linkage_methods = [
    "ward",
    "complete",
    "average",
    "single"
]

hierarchical_results = []


for method in linkage_methods:

    for k in range(2, 11):

        model = AgglomerativeClustering(
            n_clusters=k,
            linkage=method
        )

        labels = model.fit_predict(X_scaled)

        score = silhouette_score(
            X_scaled,
            labels
        )

        hierarchical_results.append(
            [method, k, score]
        )


hierarchical_search = pd.DataFrame(
    hierarchical_results,
    columns=[
        "Linkage",
        "K",
        "Silhouette"
    ]
)


print(
    "\n========== HIERARCHICAL SEARCH =========="
)

print(hierarchical_search)


best_hierarchical_row = hierarchical_search.loc[
    hierarchical_search["Silhouette"].idxmax()
]

best_linkage = best_hierarchical_row["Linkage"]

best_k_hierarchical = int(
    best_hierarchical_row["K"]
)

print("\nBest Linkage :", best_linkage)
print("Best K       :", best_k_hierarchical)


# Silhouette graph for every linkage method

plt.figure(figsize=(9, 6))

for method in linkage_methods:

    temp = hierarchical_search[
        hierarchical_search["Linkage"] == method
    ]

    plt.plot(
        temp["K"],
        temp["Silhouette"],
        marker="o",
        label=method
    )

plt.xlabel("Number of Clusters (K)")
plt.ylabel("Silhouette Score")
plt.title("Hierarchical: K and Linkage Comparison")
plt.xticks(range(2, 11))
plt.legend()
plt.grid()
plt.savefig("06_hierarchical_silhouette.png")
plt.show()


# =========================================================
# 9. FINAL HIERARCHICAL MODEL
# =========================================================

hierarchical = AgglomerativeClustering(
    n_clusters=best_k_hierarchical,
    linkage=best_linkage
)

hierarchical_label = hierarchical.fit_predict(
    X_scaled
)


hierarchical_ari = adjusted_rand_score(
    y_true,
    hierarchical_label
) if y_true is not None else np.nan

hierarchical_ami = adjusted_mutual_info_score(
    y_true,
    hierarchical_label
) if y_true is not None else np.nan

hierarchical_nmi = normalized_mutual_info_score(
    y_true,
    hierarchical_label
) if y_true is not None else np.nan

hierarchical_silhouette = silhouette_score(
    X_scaled,
    hierarchical_label
)


print("\n========== HIERARCHICAL ==========")
print("Best K       :", best_k_hierarchical)
print("Best Linkage :", best_linkage)
print("ARI          :", hierarchical_ari)
print("AMI          :", hierarchical_ami)
print("NMI          :", hierarchical_nmi)
print("Silhouette   :", hierarchical_silhouette)


plt.figure(figsize=(8, 6))
plt.scatter(
    X_scaled[:, 0],
    X_scaled[:, 1],
    c=hierarchical_label
)

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Hierarchical Clustering")
plt.savefig("07_hierarchical_final.png")
plt.show()


# =========================================================
# 10. DBSCAN - K-DISTANCE GRAPH
# =========================================================

# Usually min_samples is selected first.
# Then inspect the elbow of the k-distance graph for eps.

k_for_distance = 5

neighbors = NearestNeighbors(
    n_neighbors=k_for_distance
)

neighbors_fit = neighbors.fit(X_scaled)

distances, indices = neighbors_fit.kneighbors(
    X_scaled
)

k_distances = np.sort(
    distances[:, -1]
)


plt.figure(figsize=(8, 6))
plt.plot(k_distances)
plt.xlabel("Sorted Data Points")
plt.ylabel(
    str(k_for_distance) + "-Nearest Neighbor Distance"
)
plt.title("DBSCAN K-Distance Graph")
plt.grid()
plt.savefig("08_dbscan_k_distance.png")
plt.show()


# =========================================================
# 11. DBSCAN - EPS SEARCH FOR FIXED min_samples
# =========================================================

eps_values = np.arange(
    0.10,
    1.01,
    0.05
)

dbscan_eps_scores = []

for eps in eps_values:

    model = DBSCAN(
        eps=float(eps),
        min_samples=k_for_distance
    )

    labels = model.fit_predict(X_scaled)

    mask = labels != -1
    clean_labels = labels[mask]

    number_of_clusters = len(
        set(clean_labels)
    )

    if (
        number_of_clusters > 1
        and len(clean_labels) > number_of_clusters
    ):

        score = silhouette_score(
            X_scaled[mask],
            clean_labels
        )

    else:
        score = np.nan

    dbscan_eps_scores.append(score)


plt.figure(figsize=(8, 6))
plt.plot(
    eps_values,
    dbscan_eps_scores,
    marker="o"
)
plt.xlabel("eps")
plt.ylabel("Silhouette Score")
plt.title(
    "DBSCAN: Silhouette vs eps "
    "(min_samples = 5)"
)
plt.grid()
plt.savefig("09_dbscan_eps_silhouette.png")
plt.show()


# =========================================================
# 12. DBSCAN - GRID SEARCH eps + min_samples
# =========================================================

dbscan_results = []


for min_samples in range(3, 11):

    for eps in np.arange(
        0.10,
        1.01,
        0.05
    ):

        model = DBSCAN(
            eps=float(eps),
            min_samples=min_samples
        )

        labels = model.fit_predict(
            X_scaled
        )

        mask = labels != -1
        clean_labels = labels[mask]

        number_of_clusters = len(
            set(clean_labels)
        )

        number_of_noise = np.sum(
            labels == -1
        )

        noise_ratio = (
            number_of_noise / len(labels)
        )

        if (
            number_of_clusters > 1
            and len(clean_labels) > number_of_clusters
        ):

            score = silhouette_score(
                X_scaled[mask],
                clean_labels
            )

            dbscan_results.append([
                float(eps),
                min_samples,
                number_of_clusters,
                number_of_noise,
                noise_ratio,
                score
            ])


dbscan_search = pd.DataFrame(
    dbscan_results,
    columns=[
        "eps",
        "min_samples",
        "Clusters",
        "Noise",
        "Noise_Ratio",
        "Silhouette"
    ]
)


print("\n========== DBSCAN SEARCH ==========")

print(
    dbscan_search.sort_values(
        "Silhouette",
        ascending=False
    ).head(20)
)


best_dbscan_row = dbscan_search.loc[
    dbscan_search["Silhouette"].idxmax()
]

best_eps = float(
    best_dbscan_row["eps"]
)

best_min_samples = int(
    best_dbscan_row["min_samples"]
)


print("\nBest eps         :", best_eps)
print("Best min_samples :", best_min_samples)


# =========================================================
# 13. FINAL DBSCAN MODEL
# =========================================================

dbscan = DBSCAN(
    eps=best_eps,
    min_samples=best_min_samples
)

dbscan_label = dbscan.fit_predict(
    X_scaled
)


unique_labels = set(
    dbscan_label
)

number_of_clusters = len(
    unique_labels
)

if -1 in unique_labels:
    number_of_clusters -= 1

number_of_noise = np.sum(
    dbscan_label == -1
)


dbscan_ari = adjusted_rand_score(
    y_true,
    dbscan_label
) if y_true is not None else np.nan

dbscan_ami = adjusted_mutual_info_score(
    y_true,
    dbscan_label
) if y_true is not None else np.nan

dbscan_nmi = normalized_mutual_info_score(
    y_true,
    dbscan_label
) if y_true is not None else np.nan


mask = dbscan_label != -1
clean_labels = dbscan_label[mask]

if len(set(clean_labels)) > 1:

    dbscan_silhouette = silhouette_score(
        X_scaled[mask],
        clean_labels
    )

else:

    dbscan_silhouette = np.nan


print("\n========== DBSCAN ==========")
print("Best eps           :", best_eps)
print("Best min_samples   :", best_min_samples)
print("Number of Clusters :", number_of_clusters)
print("Noise Points       :", number_of_noise)
print("ARI                :", dbscan_ari)
print("AMI                :", dbscan_ami)
print("NMI                :", dbscan_nmi)
print("Silhouette         :", dbscan_silhouette)


# Core / Border / Noise information

core_mask = np.zeros(
    len(X_scaled),
    dtype=bool
)

core_mask[
    dbscan.core_sample_indices_
] = True

noise_mask = (
    dbscan_label == -1
)

border_mask = (
    ~core_mask
    & ~noise_mask
)


plt.figure(figsize=(8, 6))

plt.scatter(
    X_scaled[core_mask, 0],
    X_scaled[core_mask, 1],
    c=dbscan_label[core_mask],
    marker="o",
    s=40,
    label="Core"
)

plt.scatter(
    X_scaled[border_mask, 0],
    X_scaled[border_mask, 1],
    c=dbscan_label[border_mask],
    marker="s",
    s=40,
    label="Border"
)

plt.scatter(
    X_scaled[noise_mask, 0],
    X_scaled[noise_mask, 1],
    marker="x",
    s=60,
    label="Noise"
)

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("DBSCAN: Core, Border and Noise Points")
plt.legend()
plt.savefig("10_dbscan_final.png")
plt.show()


# =========================================================
# 14. GMM - AIC AND BIC
# =========================================================

component_values = range(1, 11)

aic_scores = []
bic_scores = []


for k in component_values:

    model = GaussianMixture(
        n_components=k,
        covariance_type="full",
        random_state=42
    )

    model.fit(X_scaled)

    aic_scores.append(
        model.aic(X_scaled)
    )

    bic_scores.append(
        model.bic(X_scaled)
    )


best_k_aic = list(
    component_values
)[np.argmin(aic_scores)]

best_k_bic = list(
    component_values
)[np.argmin(bic_scores)]


print("\n========== GMM AIC/BIC ==========")
print("Best K by AIC :", best_k_aic)
print("Best K by BIC :", best_k_bic)


plt.figure(figsize=(8, 6))

plt.plot(
    component_values,
    aic_scores,
    marker="o",
    label="AIC"
)

plt.plot(
    component_values,
    bic_scores,
    marker="o",
    label="BIC"
)

plt.xlabel("Number of Components")
plt.ylabel("Score")
plt.title("GMM: AIC and BIC")
plt.xticks(component_values)
plt.legend()
plt.grid()
plt.savefig("11_gmm_aic_bic.png")
plt.show()


# =========================================================
# 15. GMM - SILHOUETTE VS COMPONENTS
# =========================================================

gmm_k_values = range(2, 11)
gmm_silhouette_scores = []


for k in gmm_k_values:

    model = GaussianMixture(
        n_components=k,
        covariance_type="full",
        random_state=42
    )

    labels = model.fit_predict(
        X_scaled
    )

    score = silhouette_score(
        X_scaled,
        labels
    )

    gmm_silhouette_scores.append(
        score
    )


best_k_gmm_silhouette = list(
    gmm_k_values
)[np.argmax(gmm_silhouette_scores)]


print(
    "Best K by Silhouette:",
    best_k_gmm_silhouette
)


plt.figure(figsize=(8, 6))

plt.plot(
    gmm_k_values,
    gmm_silhouette_scores,
    marker="o"
)

plt.xlabel("Number of Components")
plt.ylabel("Silhouette Score")
plt.title("GMM: Silhouette vs Components")
plt.xticks(gmm_k_values)
plt.grid()
plt.savefig("12_gmm_silhouette.png")
plt.show()


# =========================================================
# 16. GMM - COVARIANCE TYPE COMPARISON USING BIC
# =========================================================

covariance_types = [
    "full",
    "tied",
    "diag",
    "spherical"
]

gmm_model_selection = []


for covariance in covariance_types:

    for k in range(1, 11):

        model = GaussianMixture(
            n_components=k,
            covariance_type=covariance,
            random_state=42
        )

        model.fit(X_scaled)

        bic = model.bic(X_scaled)

        gmm_model_selection.append([
            covariance,
            k,
            bic
        ])


gmm_selection_table = pd.DataFrame(
    gmm_model_selection,
    columns=[
        "Covariance",
        "Components",
        "BIC"
    ]
)


best_gmm_row = gmm_selection_table.loc[
    gmm_selection_table["BIC"].idxmin()
]

best_covariance = best_gmm_row[
    "Covariance"
]

best_k_gmm = int(
    best_gmm_row["Components"]
)


print(
    "\n========== GMM MODEL SELECTION =========="
)

print("Best Components      :", best_k_gmm)
print("Best Covariance Type :", best_covariance)
print("Minimum BIC          :", best_gmm_row["BIC"])


plt.figure(figsize=(9, 6))

for covariance in covariance_types:

    temp = gmm_selection_table[
        gmm_selection_table["Covariance"]
        == covariance
    ]

    plt.plot(
        temp["Components"],
        temp["BIC"],
        marker="o",
        label=covariance
    )

plt.xlabel("Number of Components")
plt.ylabel("BIC")
plt.title("GMM: Covariance Type and Components")
plt.xticks(range(1, 11))
plt.legend()
plt.grid()
plt.savefig("13_gmm_covariance_bic.png")
plt.show()


# =========================================================
# 17. FINAL GMM MODEL
# =========================================================

gmm = GaussianMixture(
    n_components=best_k_gmm,
    covariance_type=best_covariance,
    random_state=42
)

gmm_label = gmm.fit_predict(
    X_scaled
)


gmm_ari = adjusted_rand_score(
    y_true,
    gmm_label
) if y_true is not None else np.nan

gmm_ami = adjusted_mutual_info_score(
    y_true,
    gmm_label
) if y_true is not None else np.nan

gmm_nmi = normalized_mutual_info_score(
    y_true,
    gmm_label
) if y_true is not None else np.nan

gmm_silhouette = silhouette_score(
    X_scaled,
    gmm_label
)


print("\n========== GMM ==========")
print("Components      :", best_k_gmm)
print("Covariance Type :", best_covariance)
print("ARI             :", gmm_ari)
print("AMI             :", gmm_ami)
print("NMI             :", gmm_nmi)
print("Silhouette      :", gmm_silhouette)


plt.figure(figsize=(8, 6))

plt.scatter(
    X_scaled[:, 0],
    X_scaled[:, 1],
    c=gmm_label
)

plt.scatter(
    gmm.means_[:, 0],
    gmm.means_[:, 1],
    marker="X",
    s=250,
    label="GMM Means"
)

plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("Gaussian Mixture Model")
plt.legend()
plt.savefig("14_gmm_final.png")
plt.show()


# =========================================================
# 18. PCA - ALL COMPONENTS
# =========================================================

# PCA is NOT a clustering algorithm.
# It is used for dimensionality reduction.

pca_full = PCA()

pca_full.fit(
    X_scaled
)

explained_variance = (
    pca_full.explained_variance_ratio_
)

cumulative_variance = np.cumsum(
    explained_variance
)


print("\n========== PCA ==========")
print(
    "Explained Variance:",
    explained_variance
)

print(
    "Cumulative Variance:",
    cumulative_variance
)


# =========================================================
# 19. PCA - EXPLAINED VARIANCE GRAPH
# =========================================================

pc_numbers = range(
    1,
    len(explained_variance) + 1
)

plt.figure(figsize=(8, 6))

plt.bar(
    pc_numbers,
    explained_variance
)

plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("PCA: Explained Variance")
plt.xticks(pc_numbers)
plt.savefig("15_pca_explained_variance.png")
plt.show()


# =========================================================
# 20. PCA - CUMULATIVE VARIANCE GRAPH
# =========================================================

plt.figure(figsize=(8, 6))

plt.plot(
    pc_numbers,
    cumulative_variance,
    marker="o"
)

plt.axhline(
    y=0.95,
    linestyle="--",
    label="95% Variance"
)

plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.title("PCA: Cumulative Explained Variance")
plt.xticks(pc_numbers)
plt.legend()
plt.grid()
plt.savefig("16_pca_cumulative_variance.png")
plt.show()


# Find minimum PCs needed for 95% variance

best_pca_components = np.argmax(
    cumulative_variance >= 0.95
) + 1

print(
    "Components needed for 95% variance:",
    best_pca_components
)


# =========================================================
# 21. PCA - 2D VISUALIZATION
# =========================================================

# If dataset has >2 features, PCA converts it to 2D.
# This synthetic dataset already has 2 features.

pca_2d = PCA(
    n_components=2
)

X_pca = pca_2d.fit_transform(
    X_scaled
)


print("Original Shape:", X_scaled.shape)
print("PCA Shape     :", X_pca.shape)

print(
    "2D PCA Explained Variance:",
    pca_2d.explained_variance_ratio_
)

print(
    "2D Total Explained Variance:",
    pca_2d.explained_variance_ratio_.sum()
)


plt.figure(figsize=(8, 6))

if y_true is not None:

    plt.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        c=y_true
    )

else:

    plt.scatter(
        X_pca[:, 0],
        X_pca[:, 1]
    )

plt.xlabel("PC1")
plt.ylabel("PC2")
plt.title("PCA 2D Visualization")
plt.savefig("17_pca_2d.png")
plt.show()


# =========================================================
# 22. FINAL RESULT TABLE
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


print(
    "\n========== FINAL RESULT TABLE =========="
)

print(results)


# =========================================================
# 23. BEST MODEL USING ARI
# =========================================================

if y_true is not None:

    best_ari_index = results[
        "ARI"
    ].idxmax()

    best_ari_model = results.loc[
        best_ari_index,
        "Model"
    ]

    best_ari_score = results.loc[
        best_ari_index,
        "ARI"
    ]

    print(
        "\nBest Model by ARI:",
        best_ari_model
    )

    print(
        "Best ARI:",
        best_ari_score
    )


# =========================================================
# 24. BEST MODEL USING SILHOUETTE
# =========================================================

best_silhouette_index = results[
    "Silhouette"
].idxmax()

best_silhouette_model = results.loc[
    best_silhouette_index,
    "Model"
]

best_silhouette_score = results.loc[
    best_silhouette_index,
    "Silhouette"
]


print(
    "\nBest Model by Silhouette:",
    best_silhouette_model
)

print(
    "Best Silhouette:",
    best_silhouette_score
)


# =========================================================
# 25. ARI COMPARISON GRAPH
# =========================================================

if y_true is not None:

    plt.figure(figsize=(8, 6))

    plt.bar(
        results["Model"],
        results["ARI"]
    )

    plt.ylabel("ARI")
    plt.title("ARI Comparison")
    plt.savefig("18_ari_comparison.png")
    plt.show()


# =========================================================
# 26. SILHOUETTE COMPARISON GRAPH
# =========================================================

plt.figure(figsize=(8, 6))

plt.bar(
    results["Model"],
    results["Silhouette"]
)

plt.ylabel("Silhouette Score")
plt.title("Silhouette Score Comparison")
plt.savefig("19_silhouette_comparison.png")
plt.show()


# =========================================================
# 27. SAVE RESULT TABLE
# =========================================================

results.to_csv(
    "clustering_results.csv",
    index=False
)

hierarchical_search.to_csv(
    "hierarchical_parameter_search.csv",
    index=False
)

dbscan_search.to_csv(
    "dbscan_parameter_search.csv",
    index=False
)

gmm_selection_table.to_csv(
    "gmm_model_selection.csv",
    index=False
)

print(
    "\nAll graphs and result CSV files saved successfully."
)
