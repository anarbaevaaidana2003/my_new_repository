import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt


def init_centroids(num_clusters: int, data: np.ndarray) -> np.ndarray:
    return np.random.randint(data.min(), data.max(), (num_clusters, data.shape[1]))


def centr_dist(data: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    return np.linalg.norm(data - centroid, axis=1)


def k_means(data: np.ndarray, num_clusters: int, n_iter: int = 20) -> tuple:
    centroids = init_centroids(num_clusters, data)
    centr_history = []
    for _ in range(n_iter):
        labels = np.argmin(np.array([centr_dist(data, centroids[i]) for i in range(num_clusters)]).T, axis=1)
        centr_history.append(centroids.copy())

        new_centroids = []
        empty_cluster = False
        for i in range(num_clusters):
            points_in_cluster = data[labels == i]
            if points_in_cluster.size == 0:
                empty_cluster = True
                centroids = init_centroids(num_clusters, data)
                break
            new_centroids.append(points_in_cluster.mean(axis=0))
        if (not empty_cluster):
            centroids = np.array(new_centroids)

    labels = np.argmin(np.array([centr_dist(data, centroids[i]) for i in range(num_clusters)]).T, axis=1)
    history = np.array(centr_history)

    return labels, centroids, history


def plot_clusters(data: np.ndarray, labels: np.ndarray, centroids: np.ndarray, history: np.ndarray):
    dimensions = data.shape[1]
    if dimensions == 2:
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=labels)
        for i in range(len(centroids)):
            sns.lineplot(x=history[:, i, 0], y=history[:, i, 1], marker='o')
        sns.scatterplot(x=centroids[:, 0], y=centroids[:, 1], color='red', zorder=2)
    elif dimensions >= 3:
        fig = px.scatter_3d(x=data[:, 0], y=data[:, 1], z=data[:, 2], color=labels, title='3D Clusters and Centroids')
        fig.add_trace(go.Scatter3d(
            x=centroids[:, 0],
            y=centroids[:, 1],
            z=centroids[:, 2],
            mode='markers',
            marker=dict(size=10, color='red', symbol='circle'),
            name='Centroids'
        ))
        fig.show()
    else:
        raise ValueError("Error: required more than 1 dimension")


coords = np.concatenate([np.random.randn(100, 2) + np.array([1, 2]),
                         np.random.randn(100, 2) + np.array([-5, 4]),
                         np.random.randn(150, 2) + np.array([3, -5])], axis=0)
labels, centroids, history = k_means(coords, 3, 20)
plot_clusters(coords, labels, centroids, history)