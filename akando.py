import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

def main():
    """Set of generic functions which are useful in multiple types of situations."""
    pass


def plot_save(filename, data):
    """Saves the plot to a file"""
    L = len(data)
    fp = open(filename, 'w')
    for i in range(L):
        fp.write(str(data[i])+'\n')
    fp.close()

def distance(vector_1, vector_2):
    """Simple distance calculations using vectors"""
    a = vector_1 - vector_2
    d = np.sqrt((a*a).sum())
    return d

def smooth(data, window):
    """Local averaging function where data is the input data and window is the linear dimension of the smoothing kernel"""
    dim = data.shape
    ndim = len(dim) # The number of dimensions
    # for a 1D Vector smooth it
    if ndim == 1:
        ans = np.zeros(dim, float)
        K = np.sum(data[0 : window + 1])
        ans[0] = K / (window + 1)
        #Ramp up
        for i in range(1, window+1):
            K = K + data[i + window]
            ans[i] = K / (i + window + 1)
        #Steady as she goes
        for i in range(window + 1, dim[0] - window):
            K = K + data[window + i] - data[i + window - 1]
            ans[i] = K / (2 * window + 1)
        #Ramp down
        j = 0
        if dim < window + window :
            j = window + window - dim[0]
        for i in range(dim[0] - window, dim[0]):
            K = K - data[i - window - 1]
            ans[i] = K / (2 * window - j)
            j = j + 1
    #End of vector smooth
    else: #You have more than one (1) dimension
        #Smooth the columns and then the rows
        t = data + 0
        for i in range(0, dim[0]):
            t[i, :] = smooth(t[i, :], window)
        for j in range(0, dim[0]):
            z = (smooth(t[:, j], window))[0:dim[0]]
            t[:, j] = z
        ans = t
    #End the 2D
    return ans


if __name__ == "__main__":
    main()
