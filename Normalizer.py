"""Normalizer Methods
---------------------
Set of methods used to normalize and process data
"""
import numpy as np

def make_norm_data(N = 100, mu = 3.2, dev = 2.1):
    """Normalize the data based on the number of samples, variance, and standard deviation."""
    v = np.random.normal(mu, dev, N)
    return v

def plot_candle(data):
    """Plots the data as in the candle format.
    -------------------------------------------
    - Need to modify so that this function works within the script itself."""
    N, L = data.shape #Contains the number of vectors, and the legnth of the vectors
    avg = np.zeros(N, float) #will contain the averages
    devs = np.zeros(N, float)
    for i in range(N):
        avg[i] = data[i].mean()
        devs[i] = data[i].std()
    M = np.zeros((10, 5), float)
    for i in range(10):
        mx = data[i].max()
        mn = data[i].min()
        M[i] = i+1, avg[i] - devs[i], mn, mx, avg[i] + devs[i] 

def mean_norm(v):
    """Normalize using the mean.
    -----------------------------
    Creates data that has a zero-mean"""
    sm = v.sum()
    ans = v - sm/len(v)
    return ans

def std_norm(v):
    """Normalize the data via the Standard Deviation."""
    b = v.std()
    return v/b

