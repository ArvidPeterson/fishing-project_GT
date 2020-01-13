import numpy as np 
import matplotlib.pyplot as plt
import pickle

file_name = 'fish_stock_hist_penalty.pkl'
fish_history = pickle.load(open(file_name, 'rb'))

# import pdb; pdb.set_trace()
fish_history = np.array(fish_history)
import pdb; pdb.set_trace()
(t_max, n_sims) = fish_history.shape
low_5 = np.zeros(t_max)
high_95 = np.zeros(t_max)
idx_low = int(0.05 * n_sims)
idx_high = int(0.95 * n_sims)

mean_fish = np.array([np.mean(fish_history[ii,:]) for ii in range(t_max)])

for ii in range(t_max):
    fish_history[ii,:] = np.sort(fish_history[ii,:])
    low_5[ii] = fish_history[ii, idx_low]
    high_95[ii] = fish_history[ii, idx_high]

for ii in range(10, t_max - 1):
    low_5[ii] = (low_5[ii + 1] + low_5[ii - 1] + low_5[ii])/3
    high_95[ii] = (high_95[ii + 1] + high_95[ii - 1]  + high_95[ii])/3

t_vec = np.array(range(t_max))
# import pdb; pdb.set_trace()
fig, ax = plt.subplots(1,1, figsize=(5,4))
plt_main = ax.plot(t_vec, mean_fish, label='Mean')
plt_high = ax.plot(t_vec, high_95,color='g', label='95% conf. interval')
plt_low = ax.plot(t_vec, low_5, color='g')
ax.set_xlabel('Time')
ax.set_ylabel('Fish stock size')
ax.set_xlim([0,60])
ax.legend()
plt.show()


