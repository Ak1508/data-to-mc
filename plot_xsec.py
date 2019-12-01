import numpy as np
import pickle, string , os, time
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, AutoMinorLocator
import matplotlib.ticker as ticker
from scipy.interpolate import interp1d

fp = input("Please provide name :")
print (fp)

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('axes', linewidth=1.25)

startTime = time.time()


# reading xsection Table
xbj, xsec, born, error = np.loadtxt("xsec_eprime_%s.txt" %fp, unpack=True)



plt.tick_params(axis='both', which='minor', labelsize=18, direction = 'in')
plt.tick_params(axis='both', which='major', labelsize=18, direction = 'in')
plt.minorticks_on()
plt.grid(b=True, which= 'major', axis = 'both', linestyle='-', linewidth=1)
# plt.grid(b=True, which= 'minor', axis = 'both', linestyle=':', linewidth=1)

#print (xbj, "\t", xsec) 


#Carlos
f_born = interp1d(xbj,  born, fill_value='extrapolate')   

plt.errorbar(xbj, xsec, yerr=error, xerr=0, color ='k', linestyle ='None', marker=10, label= "{} at 21deg ".format(fp))
plt.plot(xbj, born, color= 'r', linestyle ='None', marker='.', label = "bodec Model")
#plt.plot(xbj, f_born(xbj), color= 'r', linestyle ='-', marker='None', label = "bodec Model")

#plt.yscale('Log')
plt.legend(prop={'size': 16}, frameon=False)
#plt.xlabel(r"\textbf {X$_{bj}$}",       fontsize =16)

plt.xlabel(r"\textbf {Eprime}",       fontsize =16)
plt.ylabel(r'$ \sigma^{%s} $' %(fp), fontsize =22)

# plt.gca().xaxis.set_minor_locator(AutoMinorLocator())
# plt.gca().xaxis.set_minor_formatter(FormatStrFormatter("%.2f"))

# plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(1.0))

# minors = [""] + ["%.2f" % (x-int(x)) if (x-int(x))
#                  else "" for x in np.arange(0.0, 1.2, 0.1)]
# plt.gca().xaxis.set_minor_formatter(ticker.FixedFormatter(minors))


#plt.gca().xaxis.set_minor_locator(ticker.MultipleLocator(0.05))


#.xaxis.set_minor_locator(ticker.MultipleLocator(0.25))
#plt.savefig("xsection_eprime_%s.pdf"%fp)
plt.show()
