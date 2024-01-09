import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

# Function to calculate the density at a given point (r, theta)
def density_function(r, theta):
    dr = 1 - r**2
    dtheta = np.exp(0.2 * theta) - 1
    return r * dr * dtheta

# Function to place points along contour lines separated inversely by density values
def place_points_along_contours(x, y, density_map, num_points_scale=10):
    # Specify constant density levels you want contour lines for
    constant_density_levels = np.linspace(0, np.max(density_map), 10)

    # Plot the contour lines
    contour_lines = plt.contour(x, y, density_map, levels=constant_density_levels, colors='black', linewidths=1).collections

    # Extract line data from contour lines
    curves = []
    for contour_line in contour_lines:
        paths = contour_line.get_paths()
        if paths:
            path = paths[0]
            vertices = path.vertices
            curves.append(vertices)

    # Place points along contour lines separated inversely by density values
    points = []
    for curve in curves:
        density_values = griddata((x.flatten(), y.flatten()), density_map.flatten(), (curve[:, 0], curve[:, 1]), method='linear')
        distances = 1 / density_values
        cumulative_distances = np.cumsum(distances)
        total_distance = cumulative_distances[-1]

        # Calculate the number of points based on the local density
        num_points = int(len(curve) * num_points_scale / density_values.mean())

        for i in range(num_points):
            target_distance = i * total_distance / (num_points - 1)
            
            # Ensure target_distance is within the valid range
            target_distance = max(0, min(target_distance, total_distance))
            
            normalized_index = np.interp(target_distance, cumulative_distances, np.arange(len(cumulative_distances)))
            
            # Normalize index based on the length of the curve
            normalized_index = int(normalized_index * (len(curve) - 1) / (len(cumulative_distances) - 1))
            
            points.append(curve[normalized_index])

    return np.array(points)

# Create a lattice of points
num_points = 100
r_values = np.linspace(0, 1, num_points)
theta_values = np.linspace(0, np.pi/2, num_points)
r, theta = np.meshgrid(r_values, theta_values)

# Convert polar coordinates to Cartesian coordinates
x = r * np.cos(theta)
y = r * np.sin(theta)

# Calculate the density at each point
density_map = density_function(r, theta)

# Place points along contours
points = place_points_along_contours(x, y, density_map, num_points_scale=10)

# Plot the placed points
plt.scatter(points[:, 0], points[:, 1], color='red', marker='o', label='Points along Contours')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Points along Contour Lines Separated Inversely by Density')
plt.legend()
plt.show()
