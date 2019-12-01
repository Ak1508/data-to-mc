# This scripts generate a text file for cross section. xsec is calculated by ratio method where we take yield ratio of data over mc and mutliple by model xsec.  

import ROOT as R
import numpy as np
import pickle, string , os, time
import subprocess
from pprint import pprint
from array import array
import matplotlib.pyplot as plt


plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('axes', linewidth=1.25)

startTime = time.time()

#======================================================================================#
#         Reading Yield from DATA RootFiles generated from other script 
#=======================================================================================#
dFactor_hydrogen  = 0.262 # correction factor from dummy 
dFactor_deuterium = 0.244

dataFile = R.TFile("/w/hallc-scifs17exp/xem2/abishek/xem/scripts/new_shms_yield.root")

dd = pickle.load(open('/w/hallc-scifs17exp/xem2/abishek/xem/dataDict/test.pkl', 'rb'))

hdata = {'dp'    : [],
         'ytar'  : [],
         'yptar' : [],
         'xptar' : [],
         'xfoc'  : [],
         'yfoc'  : [],
         'w2'    : [],
        }

#------------------------------------------------
# Define Dictionary to hold necessary histograms
#------------------------------------------------

histo_data    = {} # dictionary to store bare yield
histo_data_dc = {} # dictionary to store yield after dummy substraction
histo_mc      = {} # dictionary to hold mc histograms

# Reading histo from rootfile and storing in dictionary
for tar, tar_dict in dd.items():

    histo_data[tar]    = {}
    histo_data_dc[tar] = {}
    
    for var_str, var in hdata.items():

        histo_data[tar][var_str]    = []
        histo_data_dc[tar][var_str] = []
        

        for index, mom_list in enumerate(dd[tar]['pcent_list']):
            
            dataFile.cd('%s_%s' % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            
            tmp_hdp    = dataFile.FindObjectAny('hdp_qNorm_%s_%s'    % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            tmp_hytar  = dataFile.FindObjectAny('hytar_qNorm_%s_%s'  % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            tmp_hyptar = dataFile.FindObjectAny('hyptar_qNorm_%s_%s' % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            tmp_hxptar = dataFile.FindObjectAny('hxptar_qNorm_%s_%s' % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            tmp_hw2    = dataFile.FindObjectAny('hw2_qNorm_%s_%s'    % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            tmp_hxfoc  = dataFile.FindObjectAny('hxfoc_qNorm_%s_%s'  % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            tmp_hyfoc  = dataFile.FindObjectAny('hyfoc_qNorm_%s_%s'  % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))

            if   var_str=='dp':
                histo_data[tar][var_str].append(tmp_hdp)
            elif var_str=='ytar':
                histo_data[tar][var_str].append(tmp_hytar)
            elif var_str=='yptar':
                histo_data[tar][var_str].append(tmp_hyptar)
            elif var_str=='xptar':
                histo_data[tar][var_str].append(tmp_hxptar)
            elif var_str=='xfoc':
                histo_data[tar][var_str].append(tmp_hxfoc)
            elif var_str=='yfoc':
                histo_data[tar][var_str].append(tmp_hyfoc)
            else:
                histo_data[tar][var_str].append(tmp_hw2)

           #histo_data[tar]['ytar'].append(tmp_hytar)

print (tar)

#======== Dummy Substaction===================#
for tar, tar_dict in histo_data_dc.items():
   
    for key, value in hdata.items():
       
        for index, mom_list in enumerate(dd[tar]['pcent_list']):
           
            if tar == 'h1':

                histo = histo_data[tar][key][index].Clone('histo')
                histo.Add(histo_data['al27'][key][index] *dFactor_hydrogen , -1)
                histo_data_dc[tar][key].append(histo)

            elif tar == 'h2':

                histo = histo_data[tar][key][index].Clone('histo')
                histo.Add(histo_data['al27'][key][index] *dFactor_deuterium , -1)
                histo_data_dc[tar][key].append(histo)
            else:

                histo = histo_data[tar][key][index].Clone('histo')
                histo_data_dc[tar][key].append(histo)

#----------------------------------------------------------------------#
#                        Creating Root File for MC                     #
#----------------------------------------------------------------------#

rof         = R.TFile('mc.root', 'update')

InFileName  = input("What is the Target Name? ")

tar_name_dd ={'carbon': 'c12',
              'ld2'   : 'h2',
              }

for str_tar, tar in tar_name_dd.items():
    histo_mc[tar] = {}


for str_tar, tar in tar_name_dd.items():

    if (tar=='c12') : tarStr = '{}^{12}C'
    if (tar=='h2')  : tarStr = '{}^{2}H'

    if tar == tar_name_dd[InFileName]:

        histo_mc[tar]['dp'] = []

        for index, mom_list in enumerate(dd[tar]['pcent_list']):
           
            fp = R.TFile("/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.root" %(str_tar, str(dd[tar]['pcent_list'][index]).replace('.','p')), "READ")
            
            rof.cd('%s_%s'    % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
            
            print (fp)
            
            hdp      = R.TH1F('hdp_%s_%s' %(tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')), '#delta for %s, %s GeV; #delta; Number of Entries/0.5' % (tarStr, dd[tar]['pcent_list'][index]),histo_data_dc[tar]['dp'][index].GetSize()-2, histo_data_dc[tar]['dp'][index].GetXaxis().GetXmin(),histo_data_dc[tar]['dp'][index].GetXaxis().GetXmax())
            t        = fp.Get("tree")
            nentries = t.GetEntries()
            #nentries = 10000
            
            mc_scaleFactor = np.loadtxt('/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.txt' %(str_tar, str(dd[tar]['pcent_list'][index]).replace('.','p')),unpack=True)

            print (mc_scaleFactor)
            
            for entry in range(nentries):
                
                t.GetEntry(entry)
                if ((entry % 10000) == 0 and entry != 0) : print ('Analyzed %d events...' % entry)
                #--------------------------
                # Accessing leaf of interest
                #---------------------------
                delta   = getattr(t, 'dppr')
                yrec    = getattr(t, 'yrec')
                yprec   = getattr(t, 'yprec')
                xprec   = getattr(t, 'xprec')
                w2      = getattr(t, 'w2')
                xfocal  = getattr(t, 'xfoc')
                yfocal  = getattr(t, 'yfoc')
                born    = getattr(t, 'born')
                rci     = getattr(t, 'rci')
                fail_id = getattr(t, 'fail_id')
    
                if fail_id ==0:
                    if delta>-10 and delta < 22:
                        hdp.Fill(delta,     born*mc_scaleFactor/rci)
    
            histo_mc[tar]['dp'].append(hdp)
            #rof.Write()
        

#pprint (histo_mc['c12']['dp'][0])

#gr = R.TGraphErrors()

Mp     = 0.938
eb     = 10.6
thetai = 21.0
  
def cal_ep (delta):
    return( mom_val *(1+ delta/100))

def cal_w2 (ep):
    return (Mp**2 + 2.* Mp*(eb - ep) - 4.*eb*ep*(np.sin(0.5* np.deg2rad(thetai))**2))

def cal_xbj(ep) :
    return ((eb*ep*(1.0 - np.cos(np.deg2rad(thetai))))/(Mp*(eb - ep)))

ebeam, wsqr, theta, x_sec, radCorrfactor = np.loadtxt('/w/hallc-scifs17exp/xem2/abishek/monte-carlo/rc-externals/output/rad-corr-data/%s_21_deg.dat' %(InFileName), delimiter = '\t', unpack = True)
xt = R.TGraph2D()  # here I creating Object for x-sec 

for i in range(len(ebeam)):
    xt.SetPoint(i, wsqr[i], theta[i], x_sec[i])

gr = R.TGraphErrors()

tar = tar_name_dd[InFileName]

print (tar)


#ax, ay, aerror = R.Double(0), R.Double(0), R.Double(0)

#---------------------------------------
# check for file 
#---------------------------------------
filePath = '/w/hallc-scifs17exp/xem2/abishek/monte-carlo/data-to-mc/xsec_eprime_%s.txt'%(InFileName);
 # As file at filePath is deleted now, so we should check if file exists or not not before deleting them
if os.path.exists(filePath):
    os.remove(filePath)
else:
    print("Can not delete the file as it doesn't exists")


ep_list    = []
xsec_list  = []
error_list = []
born_list  = []
ratio_list = []

for index, mom_val in enumerate(dd[tar]['pcent_list']):
    print (tar)
    
    hdp_ratio = histo_data_dc[tar]['dp'][index].Clone("hdp_ratio")
    hdp_ratio.Divide(histo_mc[tar]['dp'][index])
    
    with open ("xsec_eprime_%s.txt" %(InFileName), "a") as f:
        lst_xsec   = []
        lst_eprime = []
        lst_error  = []
        lst_born   = []
        lst_ratio  = []
        for i in range (hdp_ratio.GetNbinsX()):
            
            delta  = hdp_ratio.GetXaxis().GetBinCenter(i+1)
            eprime = cal_ep(delta)
            w2     = cal_w2(eprime)
            xbj    = cal_xbj(eprime)
            
            born   = xt.Interpolate(w2, 21.035)
            
            xsec   = hdp_ratio.GetBinContent(i+1) * born
            error  = hdp_ratio.GetBinError(i+1)   * born
            lst_xsec.append(xsec)
            lst_eprime.append(eprime)
            lst_error.append(error)
            lst_born.append(born)
            lst_ratio.append(float(born/xsec))
            f.write("{} {:>10} {:>15} {:>15}\n" .format(str(round (eprime,3)), str(round(xsec,3)), str(round(born,5)), str(round(error,5)) ))
        ep_list.append(lst_eprime)
        xsec_list.append(lst_xsec)
        error_list.append(lst_error)
        born_list.append(lst_born)
        ratio_list.append(lst_ratio)


            
plt.figure(figsize=(15,8))
#print (ep_list)
#print (xsec_list)
hmkr = ['r', 'g', 'k', 'b', 'm*']
plt.tick_params(axis='both', which='minor', labelsize=18, direction = 'in')
plt.tick_params(axis='both', which='major', labelsize=18, direction = 'in')
plt.minorticks_on()
plt.grid(b=True, which= 'major', axis = 'both', linestyle='-', linewidth=1)

for index, mom_val in enumerate(dd[tar]['pcent_list']):
    plt.errorbar(ep_list[index], xsec_list[index], yerr=error_list[index], xerr = 0, markersize=7, linestyle='None', color = hmkr[index], marker = '^',label = '%s GeV' % str(dd[tar]['pcent_list'][index]))
    plt.plot(ep_list[index], born_list[index],  color = 'm', marker = '.', linestyle ='None')
plt.xlabel(r"\textbf {Eprime}",               fontsize =16)
plt.ylabel(r'$ \sigma^{%s} $' %(InFileName),  fontsize =22)
plt.legend(prop={'size':16})
#plt.savefig("new_xsec_eprime_%s.pdf" %InFileName)
#plt.show()

plt.figure(figsize=(15,8))
plt.tick_params(axis='both', which='minor', labelsize=18, direction = 'in')
plt.tick_params(axis='both', which='major', labelsize=18, direction = 'in')
plt.minorticks_on()
plt.grid(b=True, which= 'major', axis = 'both', linestyle='-', linewidth=1)
for index, mom_val in enumerate(dd[tar]['pcent_list']):
    plt.plot(ep_list[index], ratio_list[index], markersize=7, linestyle='None', color = hmkr[index], marker = '.',label = '%s GeV' % str(dd[tar]['pcent_list'][index])  )
plt.xlabel(r"\textbf {Eprime}", fontsize =16)
plt.ylabel(r'\textbf {ratio}',  fontsize =22)
plt.legend(prop={'size':16})

plt.show()

rof.Close()
dataFile.Close()
#raw = input()


#Anlysis time
print ('\nThe analysis took %.3f minutes\n' % ((time.time() - startTime) / (60.))) 


