import ROOT as R
import numpy as np
import pickle, string , os, time
import subprocess
from pprint import pprint


if os.path.exists('rootlogon.C'):
    R.gROOT.Macro('rootlogon.C')
elif os.path.exists(os.path.expanduser('~/rootlogon.C')):
    R.gROOT.Macro(os.path.expanduser('~/rootlogon.C'))

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

histo_data    = {} # dictionary to store bare yield
histo_data_dc = {} # dictionary to store yield after dummy substraction

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

            if var_str == 'dp':
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

InFileName = input("What is the Target Name? ")
mom_val    = float(input("Which Momentum Setting? "))


tar_name_dd ={'carbon': 'C12',
              'ld2'   : 'h2',
              'lh2'   : 'h1'}

tar = tar_name_dd[InFileName]

print (tar)

file = R.TFile("/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.root" %(InFileName, str(mom_val).replace('.','p')))

histo_mc    = {}
histo_ratio = {} 

#============================ Defining histograms for MC Leaf =======================================
histo_mc['hdp']    = R.TH1F('hdp',   '; #delta [%];        #epsilonQ (Counts / mC)', histo_data_dc[tar]['dp'][0].GetSize()-2,    histo_data_dc[tar]['dp'][0].GetXaxis().GetXmin(),   histo_data_dc[tar]['dp'][0].GetXaxis().GetXmax())
histo_mc['hyrec']  = R.TH1F('hytar', '; Y-tar [cm] ;       #epsilonQ (Counts / mC)', histo_data_dc[tar]['ytar'][0].GetSize()-2,  histo_data_dc[tar]['ytar'][0].GetXaxis().GetXmin(), histo_data_dc[tar]['ytar'][0].GetXaxis().GetXmax())
histo_mc['hyprec'] = R.TH1F('hyptar','; Y\'tar [rad];      #epsilonQ (Counts / mC)', histo_data_dc[tar]['yptar'][0].GetSize()-2, histo_data_dc[tar]['yptar'][0].GetXaxis().GetXmin(),histo_data_dc[tar]['yptar'][0].GetXaxis().GetXmax())
histo_mc['hxprec'] = R.TH1F('hxptar','; X\'tar [rad];      #epsilonQ (Counts / mC)', histo_data_dc[tar]['xptar'][0].GetSize()-2, histo_data_dc[tar]['xptar'][0].GetXaxis().GetXmin(),histo_data_dc[tar]['xptar'][0].GetXaxis().GetXmax())
histo_mc['hw2']    = R.TH1F('hw2',   '; W^{2} [GeV^{2}];   #epsilonQ (Counts / mC)', histo_data_dc[tar]['w2'][0].GetSize()-2,    histo_data_dc[tar]['w2'][0].GetXaxis().GetXmin(),   histo_data_dc[tar]['w2'][0].GetXaxis().GetXmax())
histo_mc['hxfoc']  = R.TH1F('hxfoc', '; xfoc  ;            #epsilonQ (Counts / mC)', histo_data_dc[tar]['xfoc'][0].GetSize()-2,  histo_data_dc[tar]['xfoc'][0].GetXaxis().GetXmin(), histo_data_dc[tar]['xfoc'][0].GetXaxis().GetXmax())
histo_mc['hyfoc']  = R.TH1F('hyfoc', '; yfoc  ;            #epsilonQ (Counts / mC)', histo_data_dc[tar]['yfoc'][0].GetSize()-2,  histo_data_dc[tar]['yfoc'][0].GetXaxis().GetXmin(), histo_data_dc[tar]['yfoc'][0].GetXaxis().GetXmax())

#if tar == 'h2':
#histo_mc['hyrec']  = R.TH1F('hytar', '; Y-tar [cm] ;       #epsilonQ (Counts / mC)', histo_data_dc[tar]['ytar'][0].GetSize()-2, histo_data_dc[tar]['ytar'][0].GetXaxis().GetXmin(), histo_data_dc[tar]['ytar'][0].GetXaxis().GetXmax())
    
   
#Getting TTree of root file
t        = file.Get("tree")
nentries = t.GetEntries()


# ========================== Scale Factor obtainig from recon MC ========================
mc_scaleFactor = np.loadtxt('/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.txt' %(InFileName, str(mom_val).replace('.','p')),unpack=True)
print (mc_scaleFactor)

print ("My Monte Carlo file: ", file)

print (tar)

for entry in range(nentries):
    
    t.GetEntry(entry)
    #ldelta           = t.GetLeaf("dppr");            delta   = ldelta.GetValue(0)
    # Accessing leaf of interest

    delta   = getattr(t, 'dppr')
    yrec    = getattr(t, 'yrec')
    yprec   = getattr(t, 'yprec')
    xprec   = getattr(t, 'xprec')
    w2      = getattr(t, 'w2')

    xfocal  = getattr(t,  'xfoc')
    yfocal  = getattr(t,  'yfoc')

    born    = getattr(t, 'born')
    rci     = getattr(t, 'rci')
    fail_id = getattr(t, 'fail_id')

    # define Cut
    if fail_id ==0:
        if delta>-10 and delta < 22:
            
            histo_mc['hdp'].Fill(delta,     born*mc_scaleFactor/rci)
            histo_mc['hyrec'].Fill(yrec,    born*mc_scaleFactor/rci)
            histo_mc['hyprec'].Fill(yprec,  born*mc_scaleFactor/rci)
            histo_mc['hw2'].Fill(w2,        born*mc_scaleFactor/rci)
            histo_mc['hxfoc'].Fill(xfocal,  born*mc_scaleFactor/rci)
            histo_mc['hyfoc'].Fill(yfocal,  born*mc_scaleFactor/rci)
            histo_mc['hxprec'].Fill(xprec,  born*mc_scaleFactor/rci)

pprint (histo_data_dc['h2']['dp'][0].Integral())
pprint (histo_data['h2']['dp'][0].Integral())

print()
pprint (histo_data_dc['c12']['dp'][0].Integral())
pprint (histo_data['c12']['dp'][0].Integral())


# formatting histograms
for tar, tar_dict in histo_data_dc.items():

    for key, value in hdata.items():

        for index, mom_list in enumerate(dd[tar]['pcent_list']):

            histo_data_dc[tar][key][index].SetLineColor(4)
            histo_data_dc[tar][key][index].GetXaxis().SetTitleSize(0.06)
            histo_data_dc[tar][key][index].GetYaxis().SetTitleSize(0.06)
            histo_data_dc[tar][key][index].GetXaxis().SetLabelSize(0.06)
            histo_data_dc[tar][key][index].GetYaxis().SetLabelSize(0.06)
            histo_data_dc[tar][key][index].SetLineWidth(1)

            histo_data[tar][key][index].SetLineColor(2)
            histo_data[tar][key][index].SetLineWidth(1)

for histo in histo_mc:
    histo_mc[histo].SetFillStyle(3003)
    histo_mc[histo].SetFillColor(3)
    histo_mc[histo].SetLineColor(3)
    histo_mc[histo].SetLineWidth(1)

    histo_mc[histo].GetXaxis().SetTitleSize(0.06)
    histo_mc[histo].GetYaxis().SetTitleSize(0.06)

    histo_mc[histo].GetYaxis().SetLabelSize(0.06)
    histo_mc[histo].GetXaxis().SetLabelSize(0.06)

mom_list = [2.7, 3.3, 4.0, 5.1]

index = mom_list.index(mom_val)

#print (index)
c1    = R.TCanvas() 
c1.Divide(2,3)

c2    = R.TCanvas()
c2.Divide(2,3)

c3    = R.TCanvas()
c3.Divide(2,3)

tar = tar_name_dd[InFileName]

print (tar)

if tar == 'h2' or tar == 'h1':
    
    print (tar)
    
    c1.cd(1)
    histo_mc['hdp'].Draw("hist")
    histo_data[tar]['dp'][index].Draw("ep1 same")
    histo_data['al27']['dp'][index].Draw("ep1 same")
    histo_data['al27']['dp'][index].SetLineColor(5)
    histo_data_dc[tar]['dp'][index].Draw("ep1 same")
    histo_mc['hdp'].SetTitle("%s   %.1f GeV^{2}" %(tar, mom_val))
    
    legend = R.TLegend(0.6,0.6,0.75,0.8)
    legend.AddEntry(histo_mc['hdp'], 'MC', 'f')
    legend.AddEntry(histo_data[tar]['dp'][index],'Data + End Cap', 'l')
    legend.AddEntry(histo_data_dc[tar]['dp'][index],'Data', 'l')
    legend.AddEntry(histo_data['al27']['dp'][index],'End Cap', 'l')
    legend.Draw()

    factor = histo_data_dc[tar]['dp'][index].Integral()/histo_mc['hdp'].Integral()
    factor = round(1-factor, 2) * 100

    c1.cd(2)

    histo_ratio['hdp_ratio'] = histo_data_dc[tar]['dp'][index].Clone("hdp_ratio")
    histo_ratio['hdp_ratio'].Divide(histo_mc['hdp'])
    histo_ratio['hdp_ratio'].Draw("ep")
    histo_ratio['hdp_ratio'].SetTitle(";[data/MC]    #delta;ratio")
    

    text = R.TText(0.1, 1.15, "Diff in % : {}".format(factor))
    text.SetTextColor(2);
    text.SetTextFont(22)
    text.SetTextSize(0.07)
    text.Draw()


    c1.cd(3)
    histo_mc['hyrec'].Draw('hist')
    histo_data[tar]['ytar'][index].Draw("ep1 same")
    histo_data['al27']['ytar'][index].Draw("ep1 same")
    histo_data['al27']['ytar'][index].SetLineColor(5)
    histo_data_dc[tar]['ytar'][index].Draw("ep1 same")

    c1.cd(4)
    histo_ratio['hytar_ratio'] = histo_data_dc[tar]['ytar'][index].Clone("hytar_ratio")
    histo_ratio['hytar_ratio'].Divide(histo_mc['hyrec'])
    histo_ratio['hytar_ratio'].Draw("ep")
    histo_ratio['hytar_ratio'].SetTitle(";[data/MC]    Y-tar;ratio")

    
    c1.cd(5)
    histo_mc['hyprec'].Draw("hist")
    histo_data[tar]['yptar'][index].Draw("ep1 same")
    histo_data['al27']['yptar'][index].Draw("ep1 same")
    histo_data['al27']['yptar'][index].SetLineColor(5)
    histo_data_dc[tar]['yptar'][index].Draw("ep1 same")
    
    c1.cd(6)
    histo_ratio['hyptar_ratio'] = histo_data_dc[tar]['ytar'][index].Clone("hyptar_ratio")
    histo_ratio['hyptar_ratio'].Divide(histo_mc['hyprec'])
    histo_ratio['hyptar_ratio'].Draw("ep")
    histo_ratio['hyptar_ratio'].SetTitle(";[data/MC]    Y\'-tar;ratio")

    
    ##++++++++++++ Second Canvas+++++++++++++++++++++ 
    c2.cd(1)
    histo_mc['hxprec'].Draw("hist")
    histo_data[tar]['xptar'][index].Draw("ep1 same")
    histo_data['al27']['xptar'][index].Draw("ep1 same")
    histo_data['al27']['xptar'][index].SetLineColor(5)
    histo_data_dc[tar]['xptar'][index].Draw("ep1 same")
    

    c2.cd(2)
    histo_ratio['hxptar_ratio'] = histo_data_dc[tar]['xptar'][index].Clone("hxptar_ratio")
    histo_ratio['hxptar_ratio'].Divide(histo_mc['hxprec'])
    histo_ratio['hxptar_ratio'].Draw("ep")
    histo_ratio['hxptar_ratio'].SetTitle(";[data/MC]    X\'-tar;ratio")
       
    c2.cd(3)
    histo_mc['hxfoc'].Draw("hist")
    histo_data[tar]['xfoc'][index].Draw("ep1 same")
    histo_data['al27']['xfoc'][index].Draw("ep1 same")
    histo_data['al27']['xfoc'][index].SetLineColor(5)
    histo_data_dc[tar]['xfoc'][index].Draw("ep1 same")

    c2.cd(4)
    histo_ratio['hxfoc_ratio'] = histo_data_dc[tar]['xfoc'][index].Clone("hxfoc_ratio")
    histo_ratio['hxfoc_ratio'].Divide(histo_mc['hxfoc'])
    histo_ratio['hxfoc_ratio'].Draw("ep")
    histo_ratio['hxfoc_ratio'].SetTitle(";[data/MC]   xfoc;ratio")
    
    
    c2.cd(5)
    histo_mc['hyfoc'].Draw("hist")
    histo_data[tar]['yfoc'][index].Draw("ep1 same")
    histo_data['al27']['yfoc'][index].Draw("ep1 same")
    histo_data['al27']['yfoc'][index].SetLineColor(5)
    histo_data_dc[tar]['yfoc'][index].Draw("ep1 same")
    
    c2.cd(6)
    histo_ratio['hyfoc_ratio'] = histo_data_dc[tar]['yfoc'][index].Clone("hyfoc_ratio")
    histo_ratio['hyfoc_ratio'].Divide(histo_mc['hyfoc'])
    histo_ratio['hyfoc_ratio'].Draw("ep")
    histo_ratio['hyfoc_ratio'].SetTitle(";[data/MC]   yfoc;ratio")
       
    c3.cd(1)
    histo_mc['hw2'].Draw("hist")
    histo_data[tar]['w2'][index].Draw("ep1 same")
    histo_data['al27']['w2'][index].Draw("ep1 same")
    histo_data['al27']['w2'][index].SetLineColor(5)
    histo_data_dc[tar]['w2'][index].Draw("ep1 same")

    c3.cd(2)
    histo_ratio['hw2_ratio'] = histo_data_dc[tar]['w2'][index].Clone("hw2_ratio")
    histo_ratio['hw2_ratio'].Divide(histo_mc['hw2'])
    histo_ratio['hw2_ratio'].Draw("ep")
    histo_ratio['hw2_ratio'].SetTitle(";[data/MC]   W^{2};ratio")

    
else:
    print (tar)

    c1.cd(1)
    histo_mc['hdp'].Draw("hist")
    histo_data_dc[tar]['dp'][index].Draw("ep1 same")
    histo_mc['hdp'].SetTitle("%s   %.1f GeV^{2}" %(tar, mom_val))

    legend = R.TLegend(0.6,0.6,0.7,0.8)
    legend.AddEntry(histo_mc['hdp'], 'MC', 'f')
    legend.AddEntry(histo_data_dc[tar]['dp'][index],'Data', 'l')
    legend.Draw()

    factor = histo_data_dc[tar]['dp'][index].Integral()/histo_mc['hdp'].Integral()
    factor = round(1-factor, 2) * 100

    c1.cd(2)

    histo_ratio['hdp_ratio'] = histo_data_dc[tar]['dp'][index].Clone("hdp_ratio")
    histo_ratio['hdp_ratio'].Divide(histo_mc['hdp'])
    histo_ratio['hdp_ratio'].Draw("ep")
    histo_ratio['hdp_ratio'].SetTitle(";[data/MC]    #delta;ratio")

    text = R.TText(0.1, 1.15, "Diff in % : {}".format(factor))
    text.SetTextColor(2);
    text.SetTextFont(22)
    text.SetTextSize(0.07)
    text.Draw()

    c1.cd(3)
    histo_mc['hyrec'].Draw("hist")
    histo_data_dc[tar]['ytar'][index].Draw("ep1 same")

    c1.cd(4)
    histo_ratio['hytar_ratio'] = histo_data_dc[tar]['ytar'][index].Clone("hytar_ratio")
    histo_ratio['hytar_ratio'].Divide(histo_mc['hyrec'])
    histo_ratio['hytar_ratio'].Draw("ep")
    histo_ratio['hytar_ratio'].SetTitle(";[data/MC]    Ytar;ratio")
    
    c1.cd(5)
    histo_mc['hyprec'].Draw("hist")
    histo_data_dc[tar]['yptar'][index].Draw("ep1 same")

    c1.cd(6)
    histo_ratio['hyptar_ratio'] = histo_data_dc[tar]['yptar'][index].Clone("hyptar_ratio")
    histo_ratio['hyptar_ratio'].Divide(histo_mc['hyprec'])
    histo_ratio['hyptar_ratio'].Draw("ep")
    histo_ratio['hyptar_ratio'].SetTitle(";[data/MC]   Y \'tar;ratio")

    ##=============== Second Canvas ========================
    c2.cd(1)
    histo_mc['hxprec'].Draw("hist")
    histo_data_dc[tar]['xptar'][index].Draw("ep1 same")

    c2.cd(2)
    histo_ratio['hxptar_ratio'] = histo_data_dc[tar]['xptar'][index].Clone("hxptar_ratio")
    histo_ratio['hxptar_ratio'].Divide(histo_mc['hxprec'])
    histo_ratio['hxptar_ratio'].Draw("ep")
    histo_ratio['hxptar_ratio'].SetTitle(";[data/MC]    X\'tar;ratio")
    
    c2.cd(3)
    histo_mc['hxfoc'].Draw("hist")
    histo_data_dc[tar]['xfoc'][index].Draw("ep1 same")
    
    c2.cd(4)
    histo_ratio['hxfoc_ratio'] = histo_data_dc[tar]['xfoc'][index].Clone("hxfoc_ratio")
    histo_ratio['hxfoc_ratio'].Divide(histo_mc['hxfoc'])
    histo_ratio['hxfoc_ratio'].Draw("ep")
    histo_ratio['hxfoc_ratio'].SetTitle(";[data/MC]   xfoc;ratio")
    
    c2.cd(5)
    histo_mc['hyfoc'].Draw("hist")
    histo_data_dc[tar]['yfoc'][index].Draw("ep1 same")

    c2.cd(6)
    histo_ratio['hyfoc_ratio'] = histo_data_dc[tar]['yfoc'][index].Clone("hyfoc_ratio")
    histo_ratio['hyfoc_ratio'].Divide(histo_mc['hyfoc'])
    histo_ratio['hyfoc_ratio'].Draw("ep")
    histo_ratio['hyfoc_ratio'].SetTitle(";[data/MC]   yfoc;ratio")
    
    
    ##+++++++++++++++++++++++++ Third Canvas+++++++++++++++++++++++++++++++++=
    c3.cd(1)
    histo_mc['hw2'].Draw("hist")
    histo_data_dc[tar]['w2'][index].Draw("ep1 same")

    c3.cd(2)
    histo_ratio['hw2_ratio'] = histo_data_dc[tar]['w2'][index].Clone("hw2_ratio")
    histo_ratio['hw2_ratio'].Divide(histo_mc['hw2'])
    histo_ratio['hw2_ratio'].Draw("ep")
    histo_ratio['hw2_ratio'].SetTitle(";[data/MC]   W^{2};ratio")


c1.Draw()
c2.Draw()
c3.Draw()
    
for histo in histo_ratio:
    histo_ratio[histo].SetMaximum(1.2)
    histo_ratio[histo].SetMinimum(0.8)

    histo_ratio[histo].GetXaxis().SetTitleSize(0.05)
    histo_ratio[histo].GetYaxis().SetTitleSize(0.05)

    #histo_ratio[histo].GetXaxis().SetTitleFont(22)
    #histo_ratio[histo].GetYaxis().SetTitleFont(22)

c1.Print("c1.ps(", "pdf")
c2.Print("c1.ps(", 'pdf')
c3.Print("c1.ps)", 'pdf')

subprocess.call(["ps2pdf", "c1.ps", "%s_%s.pdf" %(InFileName, str(mom_val).replace('.','p'))])

histo_data.clear()
histo_data_dc.clear()
histo_ratio.clear()

#raw = input()

#Anlysis time
print ('\nThe analysis took %.3f minutes\n' % ((time.time() - startTime) / (60.))) 

