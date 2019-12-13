import pickle, sys, string
from pprint import pprint
import matplotlib.pyplot as plt


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('axes', linewidth=1.25)

InFileName = input("Name the Target :")

#print (InFileName)
#print (type(InFileName))

tar_name_dd = {'carbon': 'c12',
              'ld2'   : 'h2',
              }

df = pickle.load(open("%s.pkl" %InFileName, 'rb'))

dd = pickle.load(open('/w/hallc-scifs17exp/xem2/abishek/xem/%s/dataDict.pkl' %sys.argv[1], 'rb'))

for key, value  in df['c12'].items():
    print (key)

pprint (df['c12']['born_list'][0])


plt.figure(figsize=(15,8))


hmkr = ['r', 'g', 'k', 'b', 'm*']

plt.tick_params(axis='both', which='minor', labelsize=18, direction = 'in')
plt.tick_params(axis='both', which='major', labelsize=18, direction = 'in')
plt.minorticks_on()
plt.grid(b=True, which= 'major', axis = 'both', linestyle='-', linewidth=1)

tar = tar_name_dd[InFileName]

print (tar)

for index, mom_val in enumerate(dd[tar]['pcent_list']):
   
    plt.errorbar(df[tar]['xbj_list'][index], df[tar]['xsec_list'][index], yerr= df[tar]['error_list'][index], xerr = 0, markersize=4, linestyle='None', 
                 color = hmkr[index], marker = '^',label = '%s GeV' % str(dd[tar]['pcent_list'][index]))
    if index ==0:
        plt.plot(df[tar]['xbj_list'][index], df[tar]['born_list'][index],  'm--', label = 'bodek')
    else:
        plt.plot(df[tar]['xbj_list'][index], df[tar]['born_list'][index],  'm--')


plt.xlabel(r"\textbf {X$_{bj}$}",              fontsize =16)
plt.ylabel(r'$ \sigma^{%s} $' %(InFileName),  fontsize =22)
plt.legend(prop={'size':16})


# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=
# Ratio plot for Data Over Born
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=
plt.figure(figsize=(15,8))
plt.tick_params(axis='both', which='minor', labelsize=18, direction = 'in')
plt.tick_params(axis='both', which='major', labelsize=18, direction = 'in')
plt.minorticks_on()
plt.grid(b=True, which= 'major', axis = 'both', linestyle='-', linewidth=1)


for index, mom_val in enumerate(dd[tar]['pcent_list']):
    plt.errorbar(df[tar]['ep_list'][index], df[tar]['ratio_list'][index], yerr=df[tar]['ratio_err_list'][index] , xerr = 0,  markersize=7, linestyle='None', color = hmkr[index], marker = '.',label = '%s GeV' % str(dd[tar]['pcent_list'][index])  )
plt.xlabel(r"\textbf {Eprime}", fontsize =16)
#plt.xlabel(r"\textbf {X$_{bj}$}", fontsize =16)
plt.ylabel(r'\textbf {ratio}',  fontsize =22)
plt.title(r' \textbf{ %s ratio Data/born } ' %InFileName, fontsize = 16)
plt.legend(prop={'size':16})
plt.ylim(0.8, 1.1)



plt.show()

