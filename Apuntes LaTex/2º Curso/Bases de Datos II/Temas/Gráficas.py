import matplotlib.pyplot as plt
import numpy as np

# Create the figure and the axes
fig, ax = plt.subplots(figsize=(6, 3))

# Create the x values
x = np.array([-4, -3, -2, -1, 0, 1, 2, 3, 4])
y = np.array([0, 0, 0, 0, 0, 0, 1, 0, 0])

# Plot the function
markerline, stemlines, baseline = ax.stem(x, y, linefmt='#007AFF', markerfmt='o', basefmt='black')
plt.setp(stemlines, 'linewidth', 2)

# Set the labels
ax.set_xlabel('n')
ax.set_ylabel('A')

ax.set_title(r'$\mathbf{A\:\delta[n-2]}$')

# Set the limits
ax.set_xlim([-4.1, 4.1])
ax.set_ylim([-2, 2])

# Set the ticks
ax.set_xticks([-4, -2, 0, 2, 4])
ax.set_yticks([-2, -1, 0, 1, 2])

ax.grid(True)

plt.setp(markerline, 'zorder', 3)

# Show the plot
plt.show()