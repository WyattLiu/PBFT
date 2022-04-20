import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyfit
from scipy.interpolate import make_interp_spline, BSpline


bft_scale = ((1,16984.884062878555), (2, 15814.591911675157),(3,15960.595331959365),(4,13054.210918162722),(5,16243.245299956412))
pnc_scale = ((1,17510.477762595336), (2, 27564.87742569277),(3, 31458.510027742086),(4,33362.49887845222),(5,31787.123858789306))

fig = plt.figure()
ax1 = fig.add_subplot(111)
plt.xticks([1, 2, 3, 4, 5])
x = [item[0] for item in bft_scale]
y = [item[1] for item in bft_scale]
x = np.array(x)
y = np.array(y)
ax1.scatter(x, y, s=10, marker="o", label="bft safe crdt")
newx = np.linspace(x.min(), x.max(), 300) 
spl = make_interp_spline(x, y, k=1)
smooth = spl(newx)
ax1.plot(newx, smooth)

x = [item[0] for item in pnc_scale]
y = [item[1] for item in pnc_scale]
x = np.array(x)
y = np.array(y)
ax1.scatter(x, y, s=10, marker="x", label="pnc crdt baseline")
newx = np.linspace(x.min(), x.max(), 300) 
spl = make_interp_spline(x, y, k=1)
smooth = spl(newx)
ax1.plot(newx, smooth)


plt.xlabel("Number of servers")
plt.ylabel("Throughput (ops/s)")
plt.grid(True)
plt.legend(loc='best');
plt.savefig("./scale.png", dpi = 300)

