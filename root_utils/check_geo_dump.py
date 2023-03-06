from tracemalloc import take_snapshot
import numpy as np
import matplotlib.pyplot as plt

input_file = '/project/rpp-blairt2k/machine_learning/data/HKHybrid/WCSim/e-/E0to1000MeV/unif-pos-R3240-y3287cm/4pi-dir/HKHybrid_e-_E0to1000MeV_unif-pos-R3240-y3287cm_4pi-dir_3000evts_0.root'
output_file = 'test.geom.npz'
hybrod_store_method = 0

# # Investigating the geom data after extraction

x = np.load('/project/rpp-blairt2k/machine_learning/data/HKHybrid/numpy/HKHybrid.geo.npz', mmap_mode='r')
# for i in x.files:
#   print(i)
mPMT_no = x['mPMT_no']
position_3 = x['position_3']
take_idx = np.where(position_3[:,0] > 0)[0]
print(take_idx)
y = position_3[:,1][take_idx]
z = position_3[:,2][take_idx]
x = position_3[:,0][take_idx]

fig, axs = plt.subplots(1, 2, figsize = (20, 12))
# ax = fig.add_subplot(projection='3d')
# ax.scatter(position_3[:,0], position_3[:,1], position_3[:,2])
axs[0].plot(x, y, '.')
axs[1].plot(y, z, '.')
axs[0].set_xlabel("x", fontsize=18)
axs[0].set_ylabel("y", fontsize=18)
axs[1].set_xlabel("y", fontsize=18)
axs[1].set_ylabel("z", fontsize=18)
axs[1].set_xlim(0,1000)
axs[1].set_ylim(0,1000)
plt.show()

# As you can see from the plots, the location of the mPMTs are already messed up on the barrel, speculating it's either WCSim root geom's fault or my extraction code's fault. Investigating the latter above.


