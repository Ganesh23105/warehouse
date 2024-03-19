import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2*np.pi, 2*np.pi, 1000)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.tan(x)
y4 = np.exp(x)
y5 = np.log(x + np.pi)

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

ax1.plot(x, y1, color='blue')
ax2.plot(x, y2, color='red')
ax3.plot(x, y3, color='green')
ax4.plot(x, y4, color='purple')

ax4.plot(x[x > 0], y5[x > 0], color='orange')

plt.show()
