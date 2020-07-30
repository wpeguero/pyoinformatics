"""Normalizer Methods
---------------------
Set of methods used to normalize and process data
"""
import numpy as np

def make_norm_data(N = 100, mu = 3.2, dev = 2.1):
    """Normalize the data based on the number of samples, variance, and standard deviation."""
    v = np.random.normal(mu, dev, N)
    return v