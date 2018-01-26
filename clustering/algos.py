"""
Five functions are implemented in this file:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import cluster


######################################################
# Code for closest pairs of clusters


def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    current_dist, current_idx1, current_idx2 = float('inf'), -1, -1

    for index_i in range(len(cluster_list)):
        for index_j in range(len(cluster_list)):
            if index_i != index_j:
                dist, idx1, idx2 = pair_distance(cluster_list, index_i, index_j)
                if dist < current_dist:
                    current_dist = dist
                    current_idx1 = idx1
                    current_idx2 = idx2

    return (current_dist, current_idx1, current_idx2)


def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    number_clusters = len(cluster_list)
    cluster_list.sort(key = lambda cluster: cluster.horiz_center())
    
    if number_clusters < 4:
        return slow_closest_pair(cluster_list)
    else:
        half = int(number_clusters/2)
        left = cluster_list[:half]
        right = cluster_list[half:]
        closest_left = fast_closest_pair(left)
        closest_right = fast_closest_pair(right)
        if closest_left[0] < closest_right[0]:
            dist, idx1, idx2 = closest_left
        else:
            dist, idx1, idx2 = closest_right[0], closest_right[1]+half, closest_right[2]+half
        mid = (cluster_list[half-1].horiz_center() + cluster_list[half].horiz_center())/2
        closest_strip = closest_pair_strip(cluster_list, mid, dist)
        if closest_strip[0] < dist:
            dist, idx1, idx2 = closest_strip
            
    return (dist, idx1, idx2)


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    strip = list()
    for cluster in cluster_list:
        if abs(cluster.horiz_center()-horiz_center) < half_width:
            strip.append((cluster, cluster_list.index(cluster)))
    strip.sort(key = lambda cluster: cluster[0].vert_center())
    length = len(strip)
    dist, idx1, idx2 = float('inf'), -1, -1
    
    for idx_u in range(length-1):
        for idx_v in range(idx_u+1, min(idx_u+4, length)):
            uv_dist = strip[idx_u][0].distance(strip[idx_v][0])
            if uv_dist < dist:
                dist = uv_dist
                if strip[idx_u][1] < strip[idx_v][1]:
                    idx1 = strip[idx_u][1]
                    idx2 = strip[idx_v][1]
                else:
                    idx1 = strip[idx_v][1]
                    idx2 = strip[idx_u][1]
                    
    return (dist, idx1, idx2)
            
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    while len(cluster_list) > num_clusters:
        closest_pair = fast_closest_pair(cluster_list)
        # merge two clusters
        cluster_list[closest_pair[1]].merge_clusters(cluster_list[closest_pair[2]])
        # remove the second one
        cluster_list.pop(closest_pair[2])
        # resorting
        cluster_list.sort(key = lambda cluster: cluster.horiz_center())
        
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """
    # position initial clusters at the location of clusters with largest populations    
    sorted_cluster = list(cluster_list)
    sorted_cluster.sort(key = lambda cluster: cluster.total_population())
    centers = list()
    for idx_k in range(1, num_clusters+1):
        horiz = sorted_cluster[len(sorted_cluster)-idx_k].horiz_center()
        vert = sorted_cluster[len(sorted_cluster)-idx_k].vert_center()
        centers.append((horiz, vert))
    assert len(centers) == num_clusters # force k centers
    
    # clustering
    for idx_i in range(num_iterations):
        # initialize k empty clusters
        clusters = list()
        for idx_k in range(num_clusters):
            clusters.append(cluster.Cluster(set(), centers[idx_k][0], centers[idx_k][1], 0, 0))
        # assigning closest points
        for idx_j in range(len(cluster_list)):
            min_dist = float('inf')
            for idx_k in range(num_clusters):
                # compute the distance
                vert = cluster_list[idx_j].vert_center() - centers[idx_k][1]
                horiz = cluster_list[idx_j].horiz_center() - centers[idx_k][0]
                dist = math.sqrt(vert**2 + horiz**2)
                if dist < min_dist:
                    merge_cluster = clusters[idx_k]
                    min_dist = dist
            merge_cluster.merge_clusters(cluster_list[idx_j])
        # adjusting the cluster centers
        if idx_i < num_iterations-1:
            for idx_k in range(num_clusters):
                horiz = clusters[idx_k].horiz_center()
                vert = clusters[idx_k].vert_center()
                centers[idx_k] = (horiz, vert)
    
    return clusters


