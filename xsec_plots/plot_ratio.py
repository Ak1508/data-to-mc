import string, glob
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint 

plt.rc('text', usetex=True)
plt.rc('font', family='serif')


ep_c = np.genfromtxt('carbon.txt', delimiter = '\s+', unpack=True, dtype=None, encoding=None)
ep_h = np.genfromtxt('ld2.txt'   , delimiter = '\s+', unpack=True, dtype=None, encoding=None)

#print (type(ep[0]))

ratio = []
eprime= []
for i in range (len(ep_c)):
    x_c = np.array(np.str.split(ep_c[i]), dtype = np.float)
    x_h = np.array(np.str.split(ep_h[i]), dtype = np.float)
    ratio.append(np.divide(x_c[1] ,x_h[1], out = np.zeros_like(x_c[1]), where = x_h[1]!=0)/6.)
    eprime.append(x_c[0])
    
    #x_c = np.array(x_c)

    #y = x_c.astype(np.float)

    print (x_c[1], '\t',  x_h[1])


plt.plot(eprime, ratio, color ='k', linestyle ='None', marker = 11)
plt.show()
#print (type(y))
#print (ratio)

#print (len(ep))
