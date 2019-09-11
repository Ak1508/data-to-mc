import ROOT as R
import numpy as np
import pprint, pickle, string, time
import os, sys

if os.path.exists('rootlogon.C'):
    R.gROOT.Macro('rootlogon.C')
elif os.path.exists(os.path.expanduser('~/rootlogon.C')):
    R.gROOT.Macro(os.path.expanduser('~/rootlogon.C'))

startTime = time.time()

# defining empty dictonary to store histogram
histo_mc    = {}
histo_data  = {}
histo_ratio = {}



# ====================== Opening MC file =======================================

InFileName = input("What is the Target Name? ")

mom_val    = float(input("Which Momentum Setting? "))

file = R.TFile("/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.root" %(InFileName, str(mom_val).replace('.','p')))

#=============  Defining histograms for MC Leaf ================================

histo_mc['hdp']    = R.TH1F('hdp',   '; #delta [%];        #epsilonQ (Counts / mC)', 32, -10.0, 22.0)
histo_mc['hyrec']  = R.TH1F('hytar', '; Y-tar [cm] ;       #epsilonQ (Counts / mC)', 100, -3.0,  3.0)
histo_mc['hyprec'] = R.TH1F('hyptar','; Y\'tar [rad] ;     #epsilonQ (Counts / mC)', 100, -0.1,  0.1)
histo_mc['hxprec'] = R.TH1F('hxptar','; X\'tar [rad] ;     #epsilonQ (Counts / mC)', 100, -0.1,  0.1)
histo_mc['hw2']    = R.TH1F('hw2',   '; W^{2} [GeV^{2}] ;  #epsilonQ (Counts / mC)', 100,  0.5, 19.5)
histo_mc['hxfoc']  = R.TH1F('hxfoc', '; xfoc  ;            #epsilonQ (Counts / mC)', 100, -40.0,40.0)
histo_mc['hyfoc']  = R.TH1F('hyfoc', '; yfoc  ;            #epsilonQ (Counts / mC)', 100, -40.0,40.0)


#Getting TTree of root file
t = file.Get("tree")
nentries = t.GetEntries()


# ================= Scale Factor obtainig from recon MC ========================
mc_scaleFactor = np.loadtxt('/w/hallc-scifs17exp/xem2/abishek/monte-carlo/x-section/%s_%s.txt' %(InFileName, str(mom_val).replace('.','p')),unpack=True)
print (mc_scaleFactor)
#print (type(mc_scaleFactor))

print ("My Monte Carlo file: ", file)


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
    if fail_id ==0 and delta>-10 and delta < 22:

        histo_mc['hdp'].Fill(delta,     born*mc_scaleFactor/rci)
        histo_mc['hyrec'].Fill(yrec,    born*mc_scaleFactor/rci)
        histo_mc['hyprec'].Fill(yprec,  born*mc_scaleFactor/rci)
        histo_mc['hxprec'].Fill(xprec,  born*mc_scaleFactor/rci)
        histo_mc['hw2'].Fill(w2,        born*mc_scaleFactor/rci)
        histo_mc['hxfoc'].Fill(xfocal,  born*mc_scaleFactor/rci)
        histo_mc['hyfoc'].Fill(yfocal,  born*mc_scaleFactor/rci)
    

dataFile = R.TFile("/w/hallc-scifs17exp/xem2/abishek/xem/scripts/check.root")

print ("My DataFile: " , dataFile)

dd = pickle.load(open('/w/hallc-scifs17exp/xem2/abishek/xem/dataDict/test.pkl', 'rb'))

for tar, tar_dict in dd.items():
    
    if tar == 'c12':
        
        for index, mom_list in enumerate(dd[tar]['pcent_list']):
            
            if mom_list == mom_val:
                
                dataFile.cd('%s_%s' % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
                
                histo_data['tmp_hdp']    = dataFile.FindObjectAny('hdp_qNorm_%s_%s'    % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
                histo_data['tmp_hytar']  = dataFile.FindObjectAny('hytar_qNorm_%s_%s'  % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
                histo_data['tmp_hyptar'] = dataFile.FindObjectAny('hyptar_qNorm_%s_%s' % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
                histo_data['tmp_hxptar'] = dataFile.FindObjectAny('hxptar_qNorm_%s_%s' % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
                histo_data['tmp_hw2']    = dataFile.FindObjectAny('hw2_qNorm_%s_%s'    % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
                histo_data['tmp_hxfoc']  = dataFile.FindObjectAny('hxfoc_qNorm_%s_%s'  % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
                histo_data['tmp_hyfoc']  = dataFile.FindObjectAny('hyfoc_qNorm_%s_%s'  % (tar, str(dd[tar]['pcent_list'][index]).replace('.', 'p')))
#Anlysis time
print ('\nThe analysis took %.3f minutes\n' % ((time.time() - startTime) / (60.))) 

# format histograms based on our needs
for histo in histo_mc:
    histo_mc[histo].SetLineColor(4)
    histo_mc[histo].SetLineWidth(2)

    histo_mc[histo].GetXaxis().SetTitleSize(0.05)
    histo_mc[histo].GetYaxis().SetTitleSize(0.05)
    

for histo in histo_data:
    histo_data[histo].SetFillStyle(3003)
    histo_data[histo].SetFillColor(3)
    histo_data[histo].SetLineColor(3)

    histo_data[histo].GetXaxis().SetTitleSize(0.05)
    histo_data[histo].GetYaxis().SetTitleSize(0.05)

#=======================Plot=====================================

c1    = R.TCanvas() 
c1.Divide(2,3)

c1.cd(1)
histo_mc['hdp'].Draw()
histo_data['tmp_hdp'].Draw("hist same")

legend = R.TLegend(0.6,0.6,0.7,0.8)
legend.AddEntry(histo_mc['hdp'], 'MC', 'l')
legend.AddEntry(histo_data['tmp_hdp'],'Data', 'f')
legend.Draw()

factor = histo_data['tmp_hdp'].Integral()/histo_mc['hdp'].Integral()
factor = round(1-factor, 2) * 100

c1.cd(2)
histo_ratio['hdp_ratio'] = histo_data['tmp_hdp'].Clone("hdp_ratio")
histo_ratio['hdp_ratio'].Divide(histo_mc['hdp'])
histo_ratio['hdp_ratio'].Draw("ep")
histo_ratio['hdp_ratio'].SetTitle(";[data/MC]    #delta;ratio")

text = R.TText(0.1, 1.15, "Diff in % : {}".format(factor))
text.SetTextColor(2);
text.SetTextFont(22)
text.SetTextSize(0.07)
text.Draw()

c1.cd(3)
histo_mc['hyprec'].Draw()
histo_data['tmp_hyptar'].Draw('hist same')

c1.cd(4)
histo_ratio['hyptar_ratio'] = histo_data['tmp_hyptar'].Clone('yptar_ratio')
histo_ratio['hyptar_ratio'].Divide(histo_mc['hyprec'])
histo_ratio['hyptar_ratio'].Draw("ep")
histo_ratio['hyptar_ratio'].SetTitle("; [data/MC]   yptar; ratio")

c1.cd(5)
histo_mc['hw2'].Draw()
histo_data['tmp_hw2'].Draw('hist same')


c1.cd(6)
histo_ratio['hw2_ratio'] = histo_data['tmp_hw2'].Clone('hw2_ratio')
histo_ratio['hw2_ratio'].Divide(histo_mc['hw2'])
histo_ratio['hw2_ratio'].Draw("ep")
histo_ratio['hw2_ratio'].SetTitle("; [data/MC]   W^{2}; ratio")



c2 = R.TCanvas()
c2.Divide(2,3)

c2.cd(1)
histo_mc['hxprec'].Draw()
histo_data['tmp_hxptar'].Draw('hist same')

legend1 = R.TLegend(0.7,0.6,0.79,0.8)
legend1.AddEntry(histo_mc['hyfoc'], 'MC', 'l')
legend1.AddEntry(histo_data['tmp_hyfoc'],'Data', 'f')
legend1.Draw()


c2.cd(2)
histo_ratio['hxptar_ratio'] =  histo_data['tmp_hxptar'].Clone('xptar_ratio')
histo_ratio['hxptar_ratio'].Divide(histo_mc['hxprec'])
histo_ratio['hxptar_ratio'].Draw("ep")
histo_ratio['hxptar_ratio'].SetTitle(";[data/MC]   xptar ; ratio") 

c2.cd(3)
histo_mc['hyrec'].Draw()
histo_data['tmp_hytar'].Draw('hist same')



c2.cd(4)
histo_ratio['hytar_ratio'] =  histo_data['tmp_hytar'].Clone('ytar_ratio')
histo_ratio['hytar_ratio'].Divide(histo_mc['hyrec'])
histo_ratio['hytar_ratio'].Draw("ep")
histo_ratio['hytar_ratio'].SetTitle(";[data/MC]   ytar ; ratio") 

c2.cd(5)
histo_mc['hxfoc'].Draw()
histo_data['tmp_hxfoc'].Draw('hist same')


c2.cd(6)
histo_ratio['hxfoc_ratio'] =  histo_data['tmp_hxfoc'].Clone('xfoc_ratio')
histo_ratio['hxfoc_ratio'].Divide(histo_mc['hxfoc'])
histo_ratio['hxfoc_ratio'].Draw("ep")
histo_ratio['hxfoc_ratio'].SetTitle(";[data/MC]   xfoc ; ratio") 


c3 = R.TCanvas()
c3.Divide(2,3)


c3.cd(1)
histo_mc['hyfoc'].Draw()
histo_data['tmp_hyfoc'].Draw('hist same')

legend3 = R.TLegend(0.6,0.6,0.7,0.8)
legend3.AddEntry(histo_mc['hdp'], 'MC', 'l')
legend3.AddEntry(histo_data['tmp_hdp'],'Data', 'f')
legend3.Draw()

c3.cd(2)
histo_ratio['hyfoc_ratio'] =  histo_data['tmp_hyfoc'].Clone('yfoc_ratio')
histo_ratio['hyfoc_ratio'].Divide(histo_mc['hyfoc'])
histo_ratio['hyfoc_ratio'].Draw("ep")
histo_ratio['hyfoc_ratio'].SetTitle(";[data/MC]   yfoc ; ratio") 



for histo in histo_ratio:
    histo_ratio[histo].SetMaximum(1.2)
    histo_ratio[histo].SetMinimum(0.8)

    histo_ratio[histo].GetXaxis().SetTitleSize(0.05)
    histo_ratio[histo].GetYaxis().SetTitleSize(0.05)

    #histo_ratio[histo].GetXaxis().SetTitleFont(22)
    #histo_ratio[histo].GetYaxis().SetTitleFont(22)
'''
c1.Draw()
c2.Draw()
c3.Draw()
'''

#c1.SaveAs("carbon_%s_dataToMC.pdf"    %(str(mom_val).replace('.','p')))
#c2.SaveAs("carbon_%s_fp_dataToMC.pdf" %(str(mom_val).replace('.','p')))
#c3.SaveAs("carbon_%s_ratio.pdf"       %(str(mom_val).replace('.','p')))

c1.Print("c1.ps(", "pdf")
c2.Print("c1.ps(", 'pdf')
c3.Print("c1.ps)", 'pdf')
# this will create c1.ps file. You should run "ps2pdf c1.ps outfileName" command to get output in pdf 

