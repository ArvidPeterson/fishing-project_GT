import matplotlib.pyplot as plt 
import numpy as np
import pickle

d_times = pickle.load(open('depletion_time.pkl', 'rb'))
d_mean = np.array([np.mean(d_times[ii, :]) for ii in range(100)])
t = np.linspace(1, 100, 100)

fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
ax1.plot(t, d_mean)
# ax1.set_xlabel('Generation')
ax1.set_ylabel('Mean depletion time')
ax1.set_xlim([0, 40])
ax1.set_title('(a)')

mean_total_profit = pickle.load(open('mean_total_profit.pkl', 'rb'))
prof_mean = np.array([np.mean(mean_total_profit[ii, :]) for ii in range(100)])
# t = np.linspace(1, 100, 100)
for ii in range(1,len(prof_mean) - 1):
    prof_mean[ii] = (prof_mean[ii - 1] + prof_mean[ii] + prof_mean[ii + 1]) / 3

# fig, ax = plt.subplots(1,1)
ax2.plot(t, prof_mean)
ax2.set_xlabel('Generation')
ax2.set_ylabel('Mean total profit')

ax2.set_xlim([0, 40])
ax2.set_yticks([0, 50e3, 100e3])
ax2.set_yticklabels(['0', r'$5\cdot10^{4}$', r'$1\cdot10^{5}$'])
ax2.set_title('(b)')

# effort = pickle.load(open('mean_effort.pkl', 'rb'))
# effort_mean = np.array([np.mean(effort[ii, :]) for ii in range(100)])
# ax3.plot(t, effort_mean)
# ax3.set_xlabel('Generation')
# ax3.set_ylabel('Effort')
# ax3.set_xlim([0, 40])

plt.show()





