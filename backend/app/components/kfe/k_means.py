import torch

from sklearn.metrics import silhouette_score


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# ===== K-MEANS BASE =====
@torch.jit.script
def calculate_distances(data: torch.Tensor, centers: torch.Tensor) -> torch.Tensor:
    return torch.cdist(data, centers)

@torch.jit.script
def assign_clusters(distances: torch.Tensor) -> torch.Tensor:
    return torch.argmin(distances, dim=1)

@torch.jit.script
def calculate_sse(data: torch.Tensor, centers: torch.Tensor, cluster_labels: torch.Tensor) -> float:
    sse = torch.sum(torch.stack([
        torch.sum((data[cluster_labels == i] - centers[i]) ** 2)
        for i in range(len(centers))
    ]))
    return sse.item()

def initialize_kmeans_centers(data: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
    # print("Initializing centers ...", end=' - ')
    n = len(data)
    sqrt_n = int(torch.sqrt(torch.tensor(n)))
    centers = []

    while len(centers) < sqrt_n:
        sse_min = float('inf')
        new_center = None
        final_labels = None

        for i in range(n):
            if any(torch.equal(data[i], center) for center in centers):
                continue

            temp_centers = torch.stack(centers + [data[i]])
            distances = calculate_distances(data, temp_centers)
            cluster_labels = assign_clusters(distances)
            sse = calculate_sse(data, temp_centers, cluster_labels)

            if sse < sse_min:
                sse_min = sse
                new_center = data[i]
                final_labels = cluster_labels.clone()

        centers.append(new_center)

    return final_labels, torch.stack(centers)


# ===== K-MEAN IMPROVEMENT =====
def find_nearest_clusters(distances):
    """
    Find the two closest clusters based on the distance matrix.
    """
    triu_indices = torch.triu_indices(len(distances), len(distances), offset=1)
    triu_distances = distances[triu_indices[0], triu_indices[1]]
    min_index = torch.argmin(triu_distances)
    return triu_indices[0][min_index].item(), triu_indices[1][min_index].item()

def merge_clusters(clusters, merge_indices):
    """
    Merge the two closest clusters and update the cluster labels.
    """
    merged_cluster = torch.where(clusters == merge_indices[1], merge_indices[0], clusters)
    return torch.where(merged_cluster > merge_indices[1], merged_cluster - 1, merged_cluster)

def update_cluster_centers(features, clusters, k):
    """
    Update the centers of the clusters after merging.
    """
    new_centers = []
    for cluster_id in range(k):
        cluster_samples = features[clusters == cluster_id]
        cluster_mean = torch.mean(cluster_samples, dim=0)
        distances = torch.norm(cluster_samples - cluster_mean, dim=1)
        closest_sample_index = torch.argmin(distances)
        new_centers.append(cluster_samples[closest_sample_index])
    return new_centers

def kmeans_silhouette(features):
    features = features.to(dtype=torch.float32)  # Ensure float32 dtype
    sqrt_n = int(torch.sqrt(torch.tensor(len(features))))
    k = sqrt_n
    best_k = k
    best_clusters = None
    best_avg_silhouette = -1

    clusters, centers = initialize_kmeans_centers(features)
    clusters = torch.as_tensor(clusters, device=DEVICE, dtype=torch.float32)
    centers = torch.as_tensor(centers, device=DEVICE, dtype=torch.float32)
    
    best_centers = centers.clone()

    while k > 2:
        distances = torch.cdist(centers, centers)
        merge_indices = find_nearest_clusters(distances)
        clusters = merge_clusters(clusters, merge_indices)
        centers = torch.stack(update_cluster_centers(features, clusters, k-1))

        k -= 1

        if len(torch.unique(clusters)) > 1:
            avg_silhouette = silhouette_score(features.cpu().numpy(), clusters.cpu().numpy())

            if avg_silhouette > best_avg_silhouette:
                best_avg_silhouette = avg_silhouette
                best_k = k
                best_clusters = clusters.clone()
                best_centers = centers.clone()
        else:
            break

    if best_clusters is None:
        best_clusters = clusters
        best_centers = centers

    center_indices = []
    for center in best_centers:
        distances = torch.norm(features - center, dim=1)
        center_indices.append(torch.argmin(distances).item())

    return best_clusters.cpu().numpy(), best_centers.cpu().numpy(), best_k, center_indices