import ROOT as R
import numpy as np
import pickle, string , os, time, sys
import subprocess
from pprint import pprint


# if os.path.exists('rootlogon.C'):
#     R.gROOT.Macro('rootlogon.C')
# elif os.path.exists(os.path.expanduser('~/rootlogon.C')):
#     R.gROOT.Macro(os.path.expanduser('~/rootlogon.C'))

R.gROOT.SetStyle("Plain")
R.gStyle.SetOptStat(0)
R.gStyle.SetTitleX(0.45)
# R.gStyle.SetTitleW(0.1)
#R.gStyle.SetTitleStyle(1)
#R.gStyle->SetStatFont(42);
#R.gStyle.SetLabelFont(22,  "XYZ");
#R.gROOT.ForceStyle();



if len (sys.argv) != 2:
    print (" USAGE : <output file >")
    sys.exit(1)

startTime = time.time()

# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#         Reading Yield from DATA RootFiles generated from other script 
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  

dFactor_hydrogen  = 0.262 # correction factor from dummy 
dFactor_deuterium = 0.244

# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#dataFile = R.TFile("/w/hallc-scifs17exp/xem2/abishek/xem/scripts/new_shms_yield.root")
dataFile = R.TFile("/w/hallc-scifs17exp/xem2/abishek/xem/%s/shms_yield_ytar_p_m10.root" %sys.argv[1])

dd       = pickle.load(open('/w/hallc-scifs17exp/xem2/abishek/xem/%s/dataDict.pkl' %sys.argv[1], 'rb'))

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

# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
# Reading histo from rootfile and storing in dictionary
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
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

# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#                Dummy Substaction                                       
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
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


tar_name_dd ={'carbon': 'c12',
              'ld2'   : 'h2',
              'lh2'   : 'h1'}

tar = tar_name_dd[InFileName]

print (tar)

fileN = R.TFile("/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.root" %(InFileName, str(mom_val).replace('.','p')))

print (fileN)

histo_mc    = {}
histo_ratio = {} 

mom_list = [2.7, 3.3, 4.0, 5.1]

index    = mom_list.index(mom_val)

print (index)
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#              Defining histograms for MC Leaf
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  

histo_mc['hdp']    = R.TH1F('hdp',   '; #delta [%];      #epsilonQ (Counts / mC)', histo_data_dc[tar]['dp']   [index].GetSize()-2,  histo_data_dc[tar]['dp']   [index].GetXaxis().GetXmin(), histo_data_dc[tar]['dp']   [index].GetXaxis().GetXmax())
histo_mc['hyrec']  = R.TH1F('hytar', '; Y-tar [cm] ;     #epsilonQ (Counts / mC)', histo_data_dc[tar]['ytar'] [index].GetSize()-2,  histo_data_dc[tar]['ytar'] [index].GetXaxis().GetXmin(), histo_data_dc[tar]['ytar'] [index].GetXaxis().GetXmax())
histo_mc['hyprec'] = R.TH1F('hyptar','; Y\'tar [rad];    #epsilonQ (Counts / mC)', histo_data_dc[tar]['yptar'][index].GetSize()-2,  histo_data_dc[tar]['yptar'][index].GetXaxis().GetXmin(), histo_data_dc[tar]['yptar'][index].GetXaxis().GetXmax())
histo_mc['hxprec'] = R.TH1F('hxptar','; X\'tar [rad];    #epsilonQ (Counts / mC)', histo_data_dc[tar]['xptar'][index].GetSize()-2,  histo_data_dc[tar]['xptar'][index].GetXaxis().GetXmin(), histo_data_dc[tar]['xptar'][index].GetXaxis().GetXmax())
histo_mc['hw2']    = R.TH1F('hw2',   '; W^{2} [GeV^{2}]; #epsilonQ (Counts / mC)', histo_data_dc[tar]['w2']   [index].GetSize()-2,  histo_data_dc[tar]['w2']   [index].GetXaxis().GetXmin(), histo_data_dc[tar]['w2']   [index].GetXaxis().GetXmax())
histo_mc['hxfoc']  = R.TH1F('hxfoc', '; xfoc  ;          #epsilonQ (Counts / mC)', histo_data_dc[tar]['xfoc'] [index].GetSize()-2,  histo_data_dc[tar]['xfoc'] [index].GetXaxis().GetXmin(), histo_data_dc[tar]['xfoc'] [index].GetXaxis().GetXmax())
histo_mc['hyfoc']  = R.TH1F('hyfoc', '; yfoc  ;          #epsilonQ (Counts / mC)', histo_data_dc[tar]['yfoc'] [index].GetSize()-2,  histo_data_dc[tar]['yfoc'] [index].GetXaxis().GetXmin(), histo_data_dc[tar]['yfoc'] [index].GetXaxis().GetXmax()) 

# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#       Getting TTree of root file
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  

t        = fileN.Get("tree")
nentries = t.GetEntries()
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#       Scale Factor obtainig from recon MC 
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
mc_scaleFactor = np.loadtxt('/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.txt' %(InFileName, str(mom_val).replace('.','p')),unpack=True)
print (mc_scaleFactor)

print ("My Monte Carlo file: ", fileN)

print (tar)

for entry in range(nentries):
    
    t.GetEntry(entry)
   
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
        if delta >-10 and delta <22 and yrec >-10 and yrec <10:
            
            histo_mc['hdp'].Fill(delta,     born*mc_scaleFactor/rci)
            histo_mc['hyrec'].Fill(yrec,    born*mc_scaleFactor/rci)
            histo_mc['hyprec'].Fill(yprec,  born*mc_scaleFactor/rci)
            histo_mc['hw2'].Fill(w2,        born*mc_scaleFactor/rci)
            histo_mc['hxfoc'].Fill(xfocal,  born*mc_scaleFactor/rci)
            histo_mc['hyfoc'].Fill(yfocal,  born*mc_scaleFactor/rci)
            histo_mc['hxprec'].Fill(xprec,  born*mc_scaleFactor/rci)

# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#              Formatting histograms
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  

for tar, tar_dict in histo_data_dc.items():

    for key, value in hdata.items():

        for index, mom_list in enumerate(dd[tar]['pcent_list']):

            histo_data_dc[tar][key][index].SetLineColor(4)
            # histo_data_dc[tar][key][index].GetXaxis().SetTitleSize(0.06)
            # histo_data_dc[tar][key][index].GetYaxis().SetTitleSize(0.06)
            # histo_data_dc[tar][key][index].GetXaxis().SetLabelSize(0.06)
            # histo_data_dc[tar][key][index].GetYaxis().SetLabelSize(0.06)
            histo_data_dc[tar][key][index].SetLineWidth(1)

            histo_data_dc[tar][key][index].SetTitle("")
            

            histo_data[tar][key][index].SetLineColor(2)
            histo_data[tar][key][index].SetLineWidth(1)
            histo_data[tar][key][index].GetYaxis().SetTitleOffset(0.3)
            

for histo in histo_mc:
    histo_mc[histo].SetFillStyle(3003)
    histo_mc[histo].SetFillColor(3)
    histo_mc[histo].SetLineColor(3)
    histo_mc[histo].SetLineWidth(1)

    histo_mc[histo].GetXaxis().SetTitleSize(0.0)
    histo_mc[histo].GetXaxis().SetLabelSize(0.)

    histo_mc[histo].GetYaxis().SetTitleSize(0.05)
    histo_mc[histo].GetYaxis().SetLabelSize(0.05)
    
    #histo_mc[histo].GetYaxis().SetTitleOffset(0.8)

    histo_mc[histo].SetLabelFont(22, "XY")
    histo_mc[histo].SetTitleFont(22, "XYZ")

    #histo_mc[histo].GetYaxis().SetNdivisions (510)

# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  
#                 For Plotting 
# :=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=:=  



c1    = R.TCanvas() 
c1.Divide(2,2)

c2    = R.TCanvas()
c2.Divide(2,2)

tar = tar_name_dd[InFileName]

mom_list = [2.7, 3.3, 4.0, 5.1]

index    = mom_list.index(mom_val)

print (tar)


pad1  = R.TPad (" pad1 "," pad1 " ,0 ,0.3 ,1 ,1)
pad11 = R.TPad (" pad11 "," pad2 " ,0 ,0.0 ,1 ,0.3)

pad2  = R.TPad (" pad2 "," pad2 "  ,0 ,0.3 ,1 ,1)
pad22 = R.TPad (" pad22 "," pad22 " ,0 ,0.0 ,1 ,0.3)

pad3  = R.TPad (" pad3 "," pad3 "  ,0 ,0.3 ,1 ,1)
pad33 = R.TPad (" pad33 "," pad33 " ,0 ,0.0 ,1 ,0.3)

pad4  = R.TPad (" pad4 "," pad4 "  ,0 ,0.3 ,1 ,1)
pad44 = R.TPad (" pad44 "," pad44 " ,0 ,0.0 ,1 ,0.3)

pad5  = R.TPad (" pad5 "," pad5 "  ,0 ,0.3 ,1 ,1)
pad55 = R.TPad (" pad55 "," pad55 " ,0 ,0.0 ,1 ,0.3)

pad6  = R.TPad (" pad6 "," pad5 "  ,0 ,0.3 ,1 ,1)
pad66 = R.TPad (" pad66 "," pad55 " ,0 ,0.0 ,1 ,0.3)

pad7  = R.TPad (" pad7 "," pad5 "  ,0 ,0.3 ,1 ,1)
pad77 = R.TPad (" pad77 "," pad55 " ,0 ,0.0 ,1 ,0.3)

linedp    = R.TLine (histo_data_dc[tar]['dp']   [index].GetXaxis().GetXmin() ,1 , histo_data_dc[tar]['dp']   [index].GetXaxis().GetXmax()  ,1)
lineytar  = R.TLine (histo_data_dc[tar]['ytar'] [index].GetXaxis().GetXmin() ,1 , histo_data_dc[tar]['ytar'] [index].GetXaxis().GetXmax()  ,1)
lineyptar = R.TLine (histo_data_dc[tar]['yptar'][index].GetXaxis().GetXmin() ,1 , histo_data_dc[tar]['yptar'][index].GetXaxis().GetXmax()  ,1)
linexptar = R.TLine (histo_data_dc[tar]['xptar'][index].GetXaxis().GetXmin() ,1 , histo_data_dc[tar]['xptar'][index].GetXaxis().GetXmax()  ,1)
linew2    = R.TLine (histo_data_dc[tar]['w2']   [index].GetXaxis().GetXmin() ,1 , histo_data_dc[tar]['w2']   [index].GetXaxis().GetXmax()  ,1)
linexfoc  = R.TLine (histo_data_dc[tar]['xfoc'] [index].GetXaxis().GetXmin() ,1 , histo_data_dc[tar]['xfoc'] [index].GetXaxis().GetXmax()  ,1)
lineyfoc  = R.TLine (histo_data_dc[tar]['yfoc'] [index].GetXaxis().GetXmin() ,1 , histo_data_dc[tar]['yfoc'] [index].GetXaxis().GetXmax()  ,1)

linePeak  = R.TLine (histo_data_dc[tar]['ytar'] [index].GetXaxis().GetBinCenter(histo_data_dc[tar]['ytar'] [index].GetMaximumBin()),0,histo_data_dc[tar]['ytar'] [index].GetXaxis().GetBinCenter(histo_data_dc[tar]['ytar'] [index].GetMaximumBin()), histo_mc['hyrec'].GetBinContent(histo_mc['hyrec'].GetMaximumBin()))

# print ("*****************************")
# print (histo_data_dc[tar]['ytar'] [index].GetMaximumBin())
# print (histo_data_dc[tar]['ytar'] [index].GetXaxis().GetBinCenter(histo_data_dc[tar]['ytar'] [index].GetMaximumBin()))

# #print (histo_data_dc[tar]['ytar'][index].GetXaxis().FindBin(histo_data_dc[tar]['ytar'] [index].GetMaximumBin()))
# #print (histo_data_dc[tar]['ytar'] [index].GetXaxis().GetBinCenter(histo_data_dc[tar]['ytar'][index].GetXaxis().FindBin(histo_data_dc[tar]['ytar'] [index].GetMaximumBin())))


# print ("*****************************")



print (index)

if tar == 'h2' or tar == 'h1': 
    
    print (tar)
    
    c1.cd(1)
    pad1.SetBottomMargin (0)
    pad1.Draw()
    pad1.cd()
    histo_mc['hdp'].Draw("hist")
    histo_data[tar]['dp'][index].Draw("ep1 same")
    histo_data['al27']['dp'][index].Draw("ep1 same")
    histo_data['al27']['dp'][index].SetLineColor(5)
    histo_data_dc[tar]['dp'][index].Draw("ep1 same")
    histo_mc['hdp'].SetTitle("%s   %.1f GeV" %(tar, mom_val))
    
    legend = R.TLegend(0.6,0.6,0.75,0.8)
    legend.AddEntry(histo_mc['hdp'], 'MC', 'f')
    legend.AddEntry(histo_data[tar]['dp'][index],'Data + End Cap', 'l')
    legend.AddEntry(histo_data_dc[tar]['dp'][index],'Data', 'l')
    legend.AddEntry(histo_data['al27']['dp'][index],'End Cap', 'l')
    legend.Draw()

    factor = histo_data_dc[tar]['dp'][index].Integral()/histo_mc['hdp'].Integral()
    factor = round(1-factor, 2) * 100

    c1.cd(1)
    pad11.SetTopMargin (0)
    pad11.SetBottomMargin (0.35)
    pad11.Draw()
    pad11.cd()
    histo_ratio['hdp_ratio'] = histo_data_dc[tar]['dp'][index].Clone("hdp_ratio")
    histo_ratio['hdp_ratio'].Divide(histo_mc['hdp'])
    histo_ratio['hdp_ratio'].Draw("ep")
    histo_ratio['hdp_ratio'].SetTitle("; #delta;")
    

    text = R.TText(1.1, 1.10, "Diff in % : {}".format(factor))
    text.SetTextColor(2);
    text.SetTextFont(22)
    text.SetTextSize(0.14)
    text.Draw()

    linedp.SetLineColor ( R.kBlack )
    linedp.SetLineWidth (1)
    linedp.SetLineStyle (2)
    linedp.Draw ("same")

    c1.cd(2)
    pad2.SetGridx(1)
    pad2.Draw()
    pad2.SetBottomMargin (0)
    pad2.cd()
    histo_mc['hyrec'].Draw('hist')
    histo_data[tar]['ytar'][index].Draw("ep1 same")
    histo_data['al27']['ytar'][index].Draw("ep1 same")
    histo_data['al27']['ytar'][index].SetLineColor(5)
    histo_data_dc[tar]['ytar'][index].Draw("ep1 same")

    c1.cd(2)
    pad22.SetTopMargin (0)
    pad22.SetBottomMargin (0.35)
    pad22.Draw()
    pad22.cd()
    histo_ratio['hytar_ratio'] = histo_data_dc[tar]['ytar'][index].Clone("hytar_ratio")
    histo_ratio['hytar_ratio'].Divide(histo_mc['hyrec'])
    histo_ratio['hytar_ratio'].Draw("ep")
    histo_ratio['hytar_ratio'].SetTitle("; Y_{tar};")

    lineytar.SetLineColor ( R.kBlack )
    lineytar.SetLineWidth (1)
    lineytar.SetLineStyle (2)
    lineytar.Draw ("same")
    
    c1.cd(3)
    pad3.Draw()
    pad3.cd()
    pad3.SetBottomMargin (0)
    histo_mc['hyprec'].Draw("hist")
    histo_data[tar]['yptar'][index].Draw("ep1 same")
    histo_data['al27']['yptar'][index].Draw("ep1 same")
    histo_data['al27']['yptar'][index].SetLineColor(5)
    histo_data_dc[tar]['yptar'][index].Draw("ep1 same")
    
    c1.cd(3)
    pad33.SetTopMargin (0)
    pad33.SetBottomMargin (0.35)
    pad33.Draw()
    pad33.cd()
    histo_ratio['hyptar_ratio'] = histo_data_dc[tar]['yptar'][index].Clone("hyptar_ratio")
    histo_ratio['hyptar_ratio'].Divide(histo_mc['hyprec'])
    histo_ratio['hyptar_ratio'].Draw("ep")
    histo_ratio['hyptar_ratio'].SetTitle("; Y\'_{tar};")

    lineyptar.SetLineColor ( R.kBlack )
    lineyptar.SetLineWidth (1)
    lineyptar.SetLineStyle (2)
    lineyptar.Draw ("same")

    c1.cd(4)
    pad4.Draw()
    pad4.cd()
    pad4.SetBottomMargin (0)
    histo_mc['hxprec'].Draw("hist")
    histo_data[tar]['xptar'][index].Draw("ep1 same")
    histo_data['al27']['xptar'][index].Draw("ep1 same")
    histo_data['al27']['xptar'][index].SetLineColor(5)
    histo_data_dc[tar]['xptar'][index].Draw("ep1 same")
    

    c1.cd(4)
    pad44.SetTopMargin (0)
    pad44.SetBottomMargin (0.35)
    pad44.Draw()
    pad44.cd() 
    histo_ratio['hxptar_ratio'] = histo_data_dc[tar]['xptar'][index].Clone("hxptar_ratio")
    histo_ratio['hxptar_ratio'].Divide(histo_mc['hxprec'])
    histo_ratio['hxptar_ratio'].Draw("ep")
    histo_ratio['hxptar_ratio'].SetTitle("; X\'_{tar};")

    linexptar.SetLineColor ( R.kBlack )
    linexptar.SetLineWidth (1)
    linexptar.SetLineStyle (2)
    linexptar.Draw ("same")

    #-------------------------------Second Canvas ------------------------------------------

    c2.cd(1)
    pad5.Draw()
    pad5.cd()
    pad5.SetBottomMargin (0)
    histo_mc['hxfoc'].Draw("hist")
    histo_data[tar]['xfoc'][index].Draw("ep1 same")
    histo_data['al27']['xfoc'][index].Draw("ep1 same")
    histo_data['al27']['xfoc'][index].SetLineColor(5)
    histo_data_dc[tar]['xfoc'][index].Draw("ep1 same")

    c2.cd(1)
    pad55.SetTopMargin (0)
    pad55.SetBottomMargin (0.35)
    pad55.Draw()
    pad55.cd()
    histo_ratio['hxfoc_ratio'] = histo_data_dc[tar]['xfoc'][index].Clone("hxfoc_ratio")
    histo_ratio['hxfoc_ratio'].Divide(histo_mc['hxfoc'])
    histo_ratio['hxfoc_ratio'].Draw("ep")
    histo_ratio['hxfoc_ratio'].SetTitle("; xfoc; ")

    linexfoc.SetLineColor ( R.kBlack )
    linexfoc.SetLineWidth (1)
    linexfoc.SetLineStyle (2)
    linexfoc.Draw ("same")
    
    c2.cd(2)
    pad6.Draw()
    pad6.cd()
    pad6.SetBottomMargin (0)
    histo_mc['hyfoc'].Draw("hist")
    histo_data[tar]['yfoc'][index].Draw("ep1 same")
    histo_data['al27']['yfoc'][index].Draw("ep1 same")
    histo_data['al27']['yfoc'][index].SetLineColor(5)
    histo_data_dc[tar]['yfoc'][index].Draw("ep1 same")
    
    c2.cd(2)
    pad66.SetTopMargin (0)
    pad66.SetBottomMargin (0.35)
    pad66.Draw()
    pad66.cd()
    histo_ratio['hyfoc_ratio'] = histo_data_dc[tar]['yfoc'][index].Clone("hyfoc_ratio")
    histo_ratio['hyfoc_ratio'].Divide(histo_mc['hyfoc'])
    histo_ratio['hyfoc_ratio'].Draw("ep")
    histo_ratio['hyfoc_ratio'].SetTitle("; yfoc; ")

    lineyfoc.SetLineColor ( R.kBlack )
    lineyfoc.SetLineWidth (1)
    lineyfoc.SetLineStyle (2)
    lineyfoc.Draw ("same")

    c2.cd(3)
    pad7.Draw()
    pad7.cd()
    pad7.SetBottomMargin (0)
    histo_mc['hw2'].Draw("hist")
    histo_data[tar]['w2'][index].Draw("ep1 same")
    histo_data['al27']['w2'][index].Draw("ep1 same")
    histo_data['al27']['w2'][index].SetLineColor(5)
    histo_data_dc[tar]['w2'][index].Draw("ep1 same")

    c2.cd(3)
    pad77.SetTopMargin (0)
    pad77.SetBottomMargin (0.35)
    pad77.Draw()
    pad77.cd()
    histo_ratio['hw2_ratio'] = histo_data_dc[tar]['w2'][index].Clone("hw2_ratio")
    histo_ratio['hw2_ratio'].Divide(histo_mc['hw2'])
    histo_ratio['hw2_ratio'].Draw("ep")
    histo_ratio['hw2_ratio'].SetTitle(";[data/MC]   W^{2};ratio")

    linew2.SetLineColor ( R.kBlack )
    linew2.SetLineWidth (1)
    linew2.SetLineStyle (2)
    linew2.Draw ("same")
    
else:
    print (tar)

    c1.cd(1)
    pad1.SetBottomMargin (0)
    pad1.Draw()
    pad1.cd()
    histo_mc['hdp'].Draw("hist")
    histo_data_dc[tar]['dp'][index].Draw("ep1 same")
    histo_mc['hdp'].SetTitle("%s  %.1f GeV" %(tar, mom_val))

    legend = R.TLegend(0.6,0.6,0.7,0.8)
    legend.AddEntry(histo_mc['hdp'], 'MC', 'f')
    legend.AddEntry(histo_data_dc[tar]['dp'][index],'Data', 'l')
    legend.Draw()

    factor = histo_data_dc[tar]['dp'][index].Integral()/histo_mc['hdp'].Integral()
    factor = round(1-factor, 2) * 100
    
    c1.cd(1)
    pad11.SetTopMargin (0)
    pad11.SetBottomMargin (0.35)
    pad11.Draw()
    pad11.cd()
    histo_ratio['hdp_ratio'] = histo_data_dc[tar]['dp'][index].Clone("hdp_ratio")
    histo_ratio['hdp_ratio'].Divide(histo_mc['hdp'])
    histo_ratio['hdp_ratio'].Draw("ep")
    histo_ratio['hdp_ratio'].SetTitle("; #delta;")

    text = R.TText(1.1, 1.10, "Diff in % : {}".format(factor))
    text.SetTextColor(2);
    text.SetTextFont(22)
    text.SetTextSize(0.14)
    text.Draw()
    
    linedp.SetLineColor ( R.kBlack )
    linedp.SetLineWidth (1)
    linedp.SetLineStyle (2)
    linedp.Draw ("same")


    #-------------------------------------------------------------------------------
    c1.cd(2)
    pad2.SetGridx(1)
    pad2.Draw()
    pad2.SetBottomMargin (0)
    pad2.cd()
    histo_mc['hyrec'].Draw("hist")
    histo_data_dc[tar]['ytar'][index].Draw("ep1 same")

    linePeak.SetLineColor(R.kRed)
    linePeak.Draw("same")

    c1.cd(2)
    pad22.SetTopMargin (0)
    pad22.SetBottomMargin (0.35)
    pad22.Draw()
    pad22.cd()
    histo_ratio['hytar_ratio'] = histo_data_dc[tar]['ytar'][index].Clone("hytar_ratio")
    histo_ratio['hytar_ratio'].Divide(histo_mc['hyrec'])
    histo_ratio['hytar_ratio'].Draw("ep")
    histo_ratio['hytar_ratio'].SetTitle(";Y_{tar};")

    lineytar.SetLineColor ( R.kBlack )
    lineytar.SetLineWidth (1)
    lineytar.SetLineStyle (2)
    lineytar.Draw ("same")

    
    #-----------------------------------------------------------------------------------
    c1.cd(3)
    pad3.Draw()
    pad3.cd()
    pad3.SetBottomMargin (0)
    histo_mc['hyprec'].Draw("hist")
    histo_data_dc[tar]['yptar'][index].Draw("ep1 same")

    c1.cd(3) 
    pad33.SetTopMargin (0)
    pad33.SetBottomMargin (0.35)
    pad33.Draw()
    pad33.cd()
    histo_ratio['hyptar_ratio'] = histo_data_dc[tar]['yptar'][index].Clone("hyptar_ratio")
    histo_ratio['hyptar_ratio'].Divide(histo_mc['hyprec'])
    histo_ratio['hyptar_ratio'].Draw("ep")
    histo_ratio['hyptar_ratio'].SetTitle(";Y \'_{tar};")

    lineyptar.SetLineColor ( R.kBlack )
    lineyptar.SetLineWidth (1)
    lineyptar.SetLineStyle (2)
    lineyptar.Draw ("same")
    #-----------------------------------------------------------------------------------
    c1.cd(4)
    pad4.Draw()
    pad4.cd()
    pad4.SetBottomMargin (0)
    histo_mc['hxprec'].Draw("hist")
    histo_data_dc[tar]['xptar'][index].Draw("ep1 same")

    c1.cd(4)
    pad44.SetTopMargin (0)
    pad44.SetBottomMargin (0.35)
    pad44.Draw()
    pad44.cd()
    histo_ratio['hxptar_ratio'] = histo_data_dc[tar]['xptar'][index].Clone("hxptar_ratio")
    histo_ratio['hxptar_ratio'].Divide(histo_mc['hxprec'])
    histo_ratio['hxptar_ratio'].Draw("ep")
    histo_ratio['hxptar_ratio'].SetTitle(";  X\'_{tar};")
    
    linexptar.SetLineColor ( R.kBlack )
    linexptar.SetLineWidth (1)
    linexptar.SetLineStyle (2)
    linexptar.Draw ("same")

    #-------------------------------Second Canvas ------------------------------------------
    c2.cd(1)
    pad5.Draw()
    pad5.cd()
    pad5.SetBottomMargin (0)
    histo_mc['hxfoc'].Draw("hist")
    histo_data_dc[tar]['xfoc'][index].Draw("ep1 same")
    
    c2.cd(1)
    pad55.SetTopMargin (0)
    pad55.SetBottomMargin (0.35)
    pad55.Draw()
    pad55.cd()
    histo_ratio['hxfoc_ratio'] = histo_data_dc[tar]['xfoc'][index].Clone("hxfoc_ratio")
    histo_ratio['hxfoc_ratio'].Divide(histo_mc['hxfoc'])
    histo_ratio['hxfoc_ratio'].Draw("ep")
    histo_ratio['hxfoc_ratio'].SetTitle("; xfoc;")

    linexfoc.SetLineColor ( R.kBlack )
    linexfoc.SetLineWidth (1)
    linexfoc.SetLineStyle (2)
    linexfoc.Draw ("same")

    c2.cd(2)
    pad6.Draw()
    pad6.cd()
    pad6.SetBottomMargin (0)
    histo_mc['hyfoc'].Draw("hist")
    histo_data_dc[tar]['yfoc'][index].Draw("ep1 same")

    c2.cd(2)
    pad66.SetTopMargin (0)
    pad66.SetBottomMargin (0.35)
    pad66.Draw()
    pad66.cd()
    histo_ratio['hyfoc_ratio'] = histo_data_dc[tar]['yfoc'][index].Clone("hyfoc_ratio")
    histo_ratio['hyfoc_ratio'].Divide(histo_mc['hyfoc'])
    histo_ratio['hyfoc_ratio'].Draw("ep")
    histo_ratio['hyfoc_ratio'].SetTitle("; yfoc;")
    
    lineyfoc.SetLineColor ( R.kBlack )
    lineyfoc.SetLineWidth (1)
    lineyfoc.SetLineStyle (2)
    lineyfoc.Draw ("same")
    
    c2.cd(3)
    pad7.Draw()
    pad7.cd()
    pad7.SetBottomMargin (0)
    histo_mc['hw2'].Draw("hist")
    histo_data_dc[tar]['w2'][index].Draw("ep1 same")

    c2.cd(3)
    pad77.SetTopMargin (0)
    pad77.SetBottomMargin (0.35)
    pad77.Draw()
    pad77.cd()
    histo_ratio['hw2_ratio'] = histo_data_dc[tar]['w2'][index].Clone("hw2_ratio")
    histo_ratio['hw2_ratio'].Divide(histo_mc['hw2'])
    histo_ratio['hw2_ratio'].SetTitle("; W^{2};Data/MC")
    histo_ratio['hw2_ratio'].Draw("ep")
   
    linew2.SetLineColor ( R.kBlack )
    linew2.SetLineWidth (1)
    linew2.SetLineStyle (2)
    linew2.Draw ("same")
for histo in histo_ratio:

    histo_ratio[histo].SetMaximum(1.2)
    histo_ratio[histo].SetMinimum(0.8)
    
    histo_ratio[histo].SetLineColor(R.kMagenta)

    histo_ratio[histo].GetXaxis().SetTitleSize(0.16)
    histo_ratio[histo].GetYaxis().SetTitleSize(0.11)

    histo_ratio[histo].GetYaxis().SetTitle("Data/MC")
    histo_ratio[histo].GetYaxis().CenterTitle()

    
    histo_ratio[histo].GetXaxis().SetLabelSize(0.115)
    histo_ratio[histo].GetYaxis().SetLabelSize(0.115)

    histo_ratio[histo].GetYaxis().SetNdivisions (207)

    histo_ratio[histo].GetYaxis().SetTitleOffset(0.4)
    # histo_ratio[histo].GetXaxis().SetTitleOffset(0.9)

    histo_ratio[histo].SetLabelFont(22, "XY")
    histo_ratio[histo].SetTitleFont(22, "XY")
    
    #histo_ratio[histo].GetXaxis().SetTitleFont(22)
    histo_ratio[histo].SetLabelOffset(0.03, "X")
#c1.Draw()
#c2.Draw()
#raw = input ()    
c1.Print("c1.ps(", "pdf")
c2.Print("c1.ps)", 'pdf')

subprocess.call(["ps2pdf", "c1.ps", "%s_%s_data_MC_%s.pdf" %(InFileName, str(mom_val).replace('.','p'), sys.argv[1])])

histo_data.clear()
histo_data_dc.clear()
histo_ratio.clear()

#Anlysis time
print ('\nThe analysis took %.3f minutes\n' % ((time.time() - startTime) / (60.))) 

