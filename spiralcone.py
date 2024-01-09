import matplotlib.pyplot as plt
import numpy as np

# Function to calculate the density at a given point (r, theta)
def density_function(r, theta):
    dr = 1 - r**2
    dtheta = np.exp(0.2 * theta) - 1
    return r * dr * dtheta

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

# Specify constant density levels you want contour lines for
constant_density_levels = np.linspace(0, np.max(density_map), 20)

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

# Plot the extracted contour lines
for curve in curves:
    plt.plot(curve[:, 0], curve[:, 1], color='red', linewidth=2)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Contour Lines of Density Function')
plt.show()
