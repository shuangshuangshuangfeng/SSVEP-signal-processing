# -*- coding: utf-8 -*-
"""
Created on Sun Jan  5 21:17:22 2020

MCEE + Correlation detection

@author: Brynhildr
"""

#%% Import third part module
import numpy as np
import scipy.io as io
from scipy import signal

import mcee

import copy

import signal_processing_function as SPF 
import matplotlib.pyplot as plt

import seaborn as sns
  
#%% load mcee data
# 9 chans, 1140-1540 (400ms)
eeg = io.loadmat(r'I:\SSVEP\dataset\preprocessed_data\wuqiaoyi\mcee data\begin from 140ms\50_90_bp\mcee_7.mat')

mcee_sig = np.zeros((2,120,9,1000))

#mcee_sig = eeg['mcee_sig'][:,:,:,1140:1240]
mcee_sig[:,:118,:,:] = eeg['mcee_sig'][:,:,:,1140:2140]  # 100ms
mcee_sig[:,118:,:,:] = eeg['mcee_sig'][:,18:20,:,1140:2140]  
tar_chans = eeg['chan_info'].tolist()
del eeg

plt.plot(np.mean(mcee_sig[0,:,:,:], axis=0).T)
#%%
#eeg = io.loadmat(r'I:\SSVEP\dataset\preprocessed_data\wuqiaoyi\raw & filtered data\mcee_0.mat')
#mcee_40_p = eeg['mcee_sig'][1,:,:,1140:1240]
#del eeg

#mcee_sig = np.zeros((2, mcee_60_p.shape[0], mcee_60_p.shape[1], mcee_60_p.shape[2]))
#mcee_sig[0,:,:,:] = mcee_60_p
#mcee_sig[1,:,:,:] = mcee_40_p
#del mcee_60, mcee_40

# (n_events, n_trials, n_times)
#pz = mcee_sig[:,:,0,:]   # 45
#po5 = mcee_sig[:,:,1,:]  # 51
#po3 = mcee_sig[:,:,2,:]  # 52
#poz = mcee_sig[:,:,3,:]  # 53
#po4 = mcee_sig[:,:,4,:]  # 54
#po6 = mcee_sig[:,:,5,:]  # 55
#o1 = mcee_sig[:,:,6,:]   # 58
#oz = mcee_sig[:,:,7,:]   # 59
#o2 = mcee_sig[:,:,8,:]   # 60

n_events = mcee_sig.shape[0]
n_trials = mcee_sig.shape[1]

#del mcee_sig

acc = np.zeros((10,9))
# cross-validation
for cv in range(10):
    a = cv * int(n_trials/10)
    # train dataset (n_events, n_trials, n_chans, n_times)
    tr_data = mcee_sig[:,a:a+int(n_trials/10),:,:]  # 12 trials
    # test dataset (n_events, n_trials, n_chans, n_times)
    te_data = copy.deepcopy(mcee_sig)
    te_data = np.delete(te_data,
        [a,a+1,a+2,a+3,a+4,a+5,a+6,a+7,a+8,a+9,a+10,a+11], axis=1)  # 108 trials
    # correlation detection of single-channel data
    for nc in range(9):  # n_chans
        acc[cv,nc], mr, rou = mcee.corr_detect(test_data=tr_data,
           template=np.mean(te_data[:,:,nc,:], axis=1))

# reshape results
acc = np.mat(np.mean(acc, axis=0) / (12*2) * 100)

#%% load origin data
eeg = io.loadmat(r'I:\SSVEP\dataset\preprocessed_data\wuqiaoyi\raw & filtered data\50_90_bp.mat')
ori_sig = eeg['f_data'][:,:,:,2140:3140] * 1e6
#ori_sig = np.delete(ori_sig, [41,42], axis=1)
#chan_info = eeg['chan_info'].tolist()
del eeg

# (n_events, n_trials, n_times)
#pz = ori_sig[:2,:,45,:]
#po5 = ori_sig[:2,:,51,:]
#po3 = ori_sig[:2,:,52,:]
#poz = ori_sig[:2,:,53,:]
#po4 = ori_sig[:2,:,54,:]
#po6 = ori_sig[:2,:,55,:]
#o1 = ori_sig[:2,:,58,:]
#oz = ori_sig[:2,:,59,:]
#o2 = ori_sig[:2,:,60,:]
ori_sig = ori_sig[:,:,[45,51,52,53,54,55,58,59,60],:]

n_events = ori_sig.shape[0]
n_trials = ori_sig.shape[1]

#del ori_sig
#del chan_info
plt.plot(ori_sig[0,:,7,:].T)
#%%
acc = np.zeros((10,9))
# cross-validation
for cv in range(10):
    a = cv * int(n_trials/10)
    # train dataset (n_events, n_trials, n_chans, n_times)
    tr_data = ori_sig[:,a:a+int(n_trials/10),:,:]  # 12 trials
    # test dataset (n_events, n_trials, n_chans, n_times)
    te_data = copy.deepcopy(ori_sig)
    te_data = np.delete(te_data,
        [a,a+1,a+2,a+3,a+4,a+5,a+6,a+7,a+8,a+9,a+10,a+11], axis=1)  # 108 trials
    # correlation detection of single-channel data
    for nc in range(9):  # n_chans
        acc[cv,nc], mr, rou = mcee.corr_detect(test_data=tr_data,
           template=np.mean(te_data[:,:,nc,:], axis=1))
        
# reshape results
acc = np.mat(np.mean(acc, axis=0) / (12*2) * 100)

#%% check waveform
sns.set(style='whitegrid')
fig, ax = plt.subplots(3,1,figsize=(4,12))

ax[0].plot(pz[0,:,:].T, linewidth=0.5)
ax[0].plot(np.mean(pz[0,:,:], axis=0), linewidth=3, color='black')
#ax[0].set_ylim(-20,20)

ax[1].plot(pz[1,:,:].T, linewidth=0.5)
ax[1].plot(np.mean(pz[1,:,:], axis=0), linewidth=3, color='black')
#ax[1].set_ylim(-20,20)

ax[2].plot(pz[2,:,:].T, linewidth=0.5)
ax[2].plot(np.mean(pz[2,:,:], axis=0), linewidth=3, color='black')
#ax[2].set_ylim(-20,20)

#%% check waveform
plt.plot(template[0,:], color='tab:orange')
plt.plot(pz[0,76,:], color='tab:blue')
