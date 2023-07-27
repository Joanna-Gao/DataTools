import numpy as np
import matplotlib.pyplot as plt

x = np.load('/project/rpp-blairt2k/machine_learning/data/HKHybrid/numpy/HKHybrid.geo.npz', mmap_mode='r')
# for i in x.files:
#   print(i)
mPMT_no = x['mPMT_no']
position_3 = x['position_3']
print(mPMT_no[:21])
print(position_3[:,0][:21], position_3[:,1], position_3[:,2])

fig, axs = plt.subplots(1, 2, figsize = (12, 20))
# ax = fig.add_subplot(projection='3d')
# ax.scatter(position_3[:,0], position_3[:,1], position_3[:,2])
axs[0].plot(position_3[:,0], position_3[:,1], '.')
axs[1].plot(position_3[:,0], position_3[:,2], '.')
plt.show()


