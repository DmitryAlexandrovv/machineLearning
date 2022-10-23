from operator import truediv
import pygame
import numpy as np

R = 7

def dist(pntA, pntB):
    return np.sqrt((pntA[0] - pntB[0]) ** 2 + (pntA[1] - pntB[1]) ** 2)

def init_centroids(points, cluster_count):
    x_avg = 0
    y_avg = 0

    for i in points:
        x_avg += i[0]
        y_avg += i[1]
    x_avg = x_avg / len(points)
    y_avg = y_avg / len(points)

    R = 0
    for i in range(len(points)): 
        distance = dist(points[i], [x_avg, y_avg]) 
        if R < distance: 
            R = distance 
    centroids = []
    for i in range(cluster_count): 
        x_c = R * np.cos(2 * np.pi * i / cluster_count) + x_avg
        y_c = R * np.sin(2 * np.pi * i / cluster_count) + y_avg
        centroids.append([x_c, y_c]) 
    return centroids

def nearest_centroids(points, centroids):
    clusters = {} 
    for i in range(len(centroids)): 
        clusters[i] = []
  
    for i in range(len(points)): 
        points_range = [] 
        for j in range(len(centroids)):
            points_range.append(dist(points[i], centroids[j])) 
        index = points_range.index(min(points_range))
        clusters[index].append(points[i]) 

    return clusters

def centroid(points):
    x_avg = 0
    y_avg = 0

    for i in points:
        x_avg += i[0]
        y_avg += i[1]

    x_avg = x_avg / len(points)
    y_avg = y_avg / len(points)

    return [x_avg, y_avg]

def compare_clusters(centroids, new_centroids, clusters, new_clusters):
    for i in range(len(new_centroids)):
        if new_centroids[i] != centroids[i]:
            return False

    for key in clusters.keys():
        if np.allclose(clusters[key], new_clusters[key]) == False:
            return False

    return True

def sum_dist_points_clusters(centroids, clusters):
    sum_dist = 0
    for key, value in clusters.items():
        for point in value:
            sum_dist += dist(centroids[key], point)

    return sum_dist

def sum_distance_by_cluster_count(points):
    sum_distances = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for k in range(1, 6):
        centroids = init_centroids(points, k)
        clusters = nearest_centroids(points, centroids)

        if [] in clusters.values():
            return sum_distances

        prev_centroids = centroids
        prev_clusters = clusters

        centroids = []
        for key, value in clusters.items():
            centroids.append(centroid(value))

        clusters = nearest_centroids(points, centroids)

        while compare_clusters(prev_centroids, centroids, prev_clusters, clusters) == False:
            prev_centroids = centroids
            prev_clusters = clusters

            centroids = []
            for key, value in clusters.items():
                centroids.append(centroid(value))
            clusters = nearest_centroids(points, centroids)
            sum_distances[k] = sum_dist_points_clusters(centroids, clusters)


    return sum_distances

def optimal_cluster_count(distances):
    min_d = 10000
    min_key = 0
    count = 0

    for key, value in distances.items():
        if (value == 0):
            return count
        count += 1

    for key in distances.keys():
        if key == 1 or key == len(distances.keys()):
            continue 
        d = (abs(distances[key] - distances[key+1]))/(abs(distances[key-1] - distances[key]))
        if d < min_d:
            min_d = d
            min_key = key

    return min_key

def giveFlags(points):
    eps = 15
    minPts = 3
    flags = np.zeros(len(points))
    for point, i in enumerate(points):
        nghb = 0
        for pnt in points:
            if dist(point, pnt) < eps and point != pnt:
                nghb += 1
        if nghb >= minPts:
            flags[i] = 'green'
        print(flags)

def draw_clusters(clusters, screen):
    colors = ['red','green','yellow','magenta','cyan','grey','#f03a09']

    for key, value in clusters.items():
        for i in value:
            pygame.draw.circle(screen, color = colors[key], center = [i[0], i[1]], radius = R)

def draw_centroids(points, screen):
    xs = []
    ys = []
    for i in points:
        pygame.draw.circle(screen, color = 'pink', center = [i[0], i[1]], radius = R)

def draw():
    points = []
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    screen.fill(color = 'white')
    pygame.display.update()
    play = True
    isStartCluster = False

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.exit()
                play = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pygame.draw.circle(screen, color = 'black', center = event.pos, radius = R)
                    points.append(np.array(event.pos))
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                distances = sum_distance_by_cluster_count(points)

                k = optimal_cluster_count(distances)
                centroids = init_centroids(points, k)
                clusters = nearest_centroids(points, centroids)

                # draw_clusters(clusters, screen)
                # draw_centroids(centroids, screen)

                prev_centroids = centroids
                prev_clusters = clusters
                centroids = []


                for key, value in clusters.items():
                    centroids.append(centroid(value))

                clusters = nearest_centroids(points, centroids)
                draw_clusters(clusters, screen)
                draw_centroids(centroids, screen)

                i = 0
                while compare_clusters(prev_centroids, centroids, prev_clusters, clusters) == False:
                    i += 1
                    prev_centroids = centroids
                    prev_clusters = clusters

                    centroids = []
                    for key, value in clusters.items():
                        centroids.append(centroid(value))

                    clusters = nearest_centroids(points, centroids)
                    draw_clusters(clusters, screen)
                    draw_centroids(centroids, screen)
                

        pygame.display.update()
    
draw()
