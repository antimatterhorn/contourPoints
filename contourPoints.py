import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

# Function to calculate the density at a given point (r, theta)
def density_function(r, theta):
    dr = 1 - r**3
    dtheta = np.exp(0.2 * theta) - 1
    return r * dr * dtheta

# Function to place points along contour lines separated by density values
def place_points_along_contours(x, y, density_map, num_points_scale=10):
    # Specify constant density levels you want contour lines for
    constant_density_levels = np.linspace(0, np.max(density_map), 40)

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

    # Place points along contour lines separated by density values
    points = []
    for curve in curves:
        density_values = griddata((x.flatten(), y.flatten()), density_map.flatten(), (curve[:, 0], curve[:, 1]), method='linear')
        normalized_density = (density_values - density_values.min()) / (density_values.max() - density_values.min())

        # Number of points based on density and curve length
        num_points = int(num_points_scale * len(curve) * normalized_density.mean())

        # Interpolate points along the curve
        t = np.linspace(0, 1, len(curve))
        t_interp = np.linspace(0, 1, num_points)
        x_interp = np.interp(t_interp, t, curve[:, 0])
        y_interp = np.interp(t_interp, t, curve[:, 1])

        # Append to the list of points
        points.append(np.column_stack((x_interp, y_interp)))

    return np.concatenate(points)

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
points = place_points_along_contours(x, y, density_map, num_points_scale=0.5)

# Plot the placed points
plt.scatter(points[:, 0], points[:, 1], color='red', marker='o', label='Points along Contours')

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Points along Contour Lines Proportional to Density and Curve Length')
plt.legend()
plt.show()
