import matplotlib.pyplot as plt
import numpy as np
import seaborn as sbor
import tools


plot_list = []
for sample in range(100):

    local_a = np.random.normal(0.0,1.0)
    local_b = np.random.normal(0.0,1.0)

    plot_list.append(tools.generator(local_a,local_b))

plt.plot(plot_list)

plt.show()
