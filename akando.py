import numpy as np
import matplotlib.pyplot as plt
from numpy.core.defchararray import array
from numpy.core.fromnumeric import reshape
from scipy import fftpack
from PIL import Image,ravel



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

def baseline(data, WN=100):
    L = len(data)
    pts = []
    for i in range(0, L, WN):
        a = data[i:i+WN]
        mn = a.min()
        x = np.nonzero(np.equal(a, mn))[0][0]
        pts.append([i+x, mn])
    nd = np.zeros(len(data), float)
    nsegs = len(pts) - 1
    for i in range(nsegs):
        x1, y1 = pts[i]
        x2, y2 = pts[i+1]
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        w = np.arange(x1, x2)
        y = m * w + b
        nd[x1:x2] = data[x1:x2] - y
    #Create vector containing 0 if nd is less than zero.
    mask = np.greater_equal(nd, 0)
    #New new data.
    nnd = mask * nd
    return nnd

def range_histogram(indata, nbins, mn=-1, mx=-1):
    """Creates a histogram based on the input data and the desired number of bins."""
    ans = np.zeros(nbins)
    L = len(indata)
    data = indata + 0
    fix = 0
    if mn == -1 and mx == -1:
        # No limits were given so create an autoscale.
        mx = indata.max() * 1.01
        mn = indata.min()
    else:
        mx *= 1.01
    data = (indata - mn) / (mx-mn) * nbins
    print(data.max())
    hst = np.zeros(nbins, int)
    for i in range(L):
        k = int(data[i])
        hst[k] += 1
    return hst

def linear_regression(x, y):
    """Returns the slope and b. x and Y are vectors."""
    sxy = (x * y + 0.0).sum() #Ensures at least a float type
    sx = (x + 0.0).sum()
    sy = (y + 0.0).sum()
    sx2 = (x * x + 0.0).sum()
    n = len(x)
    m = (n * sxy - sx * sy) / (n * sx2 - sx * sx)
    b = (sy - m * sx) / n
    return m, b

def circle(size, loc, rad):
    """Creates a matrix with the dimension size that is a circle."""
    b1, b2 = np.indices(size)
    b1, b2 = b1 - loc[0], b2 - loc[1]
    mask = b1 * b1 + b2 * b2
    mask = np.less_equal(mask, rad * rad).astype(int)
    return mask

def correlate(a, b):
    """Fourier space correlation."""
    n = len(a.shape())
    if n == 1:
        A = fftpack.fft(a)
        B = fftpack.fft(b)
        C = A * B.conjugate()
        d = fftpack.ifft(C);
        d = Swap(d);
    elif n == 2:
        A = fftpack.fft2(a)
        B = fftpack.fft2(b)
        C = A * B.conjugate()
        d = fftpack.ifft(C)
        d = Swap(d)
    return d

def Swap(A):
    """Performs a quadrant swap"""
    if len(A.shape) == 2:
        (v, h) = A.shape
        ans = np.zeros(A.shape, A.dtype)
        ans[0:v/2, 0:h/2] = A[v/2:v, h/2:h]
        ans[0:v/2, h/2:h] = A[v/2:v, 0:h/2]
        ans[v/2:v, h/2:h] = A[0:v/2, 0:h/2]
        ans[v/2:v, 0:h/2] = A[0:v/2, h/2:h]
    elif len(A.shape) == 1:
        ans[0:v/2] = A[v/2:v]
        ans[v/2:v] = A[0:v/2]
    else: #odd number of elements
        ans[0:v/2] = A[v-v/2:v]
        ans[v/2:v] = A[0:v/2 + 1]
    return ans

def a2i(data):
    mg = Image.new('L'.transpose(data).shape)
    mn = data.min()
    a = data - mn
    mx = a.max()
    a = a*256./mx
    mg.putdata(ravel(a))
    return mg

def a2if(data):
    mg = Image.new('L'.transpose(data).shape)
    mg.putdata(ravel(data))
    return mg

def i2a(mg):
    mgt = mg.transpose(2).transpose(1)
    f = mgt.getdata()
    z = array(f)
    zz = transpose(reshape(z, mg.size))
    return zz


if __name__ == "__main__":
    main()
