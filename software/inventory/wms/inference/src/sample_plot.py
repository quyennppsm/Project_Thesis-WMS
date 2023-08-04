import numpy as np
import matplotlib.pyplot as plt

# Generate data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create figure and axes
fig, ax = plt.subplots()

# Plot data
ax.plot(x, y)

# Set plot properties
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Sine Wave')

# Show plot
plt.show()