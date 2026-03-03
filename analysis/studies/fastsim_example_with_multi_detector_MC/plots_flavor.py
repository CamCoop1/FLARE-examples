""" 
Steering script taken from https://github.com/HEP-FCC/FCCAnalyses/tree/master/examples/FCCee/higgs/mH-recoil
"""

import ROOT

# global parameters
intLumi = 1
intLumiLabel = "L = 5 ab^{-1}"
ana_tex = "e^{+}e^{-} #rightarrow ZH #rightarrow #mu^{+}#mu^{-} b b"
delphesVersion = "3.4.2"
energy = 240.0
collider = "FCC-ee"
formats = ["png", "pdf"]
plotStatUnc = False
customLabel = 'Hello'

colors = {}
colors["IDEA"] =ROOT.kGreen - 10
colors["lighterVXD_35pc"] = ROOT.kGreen + 2
colors["lighterVXD_50pc"] = ROOT.kBlue + 2
colors["3T"] = ROOT.kRed+3
colors["SiTracking"] =  ROOT.kRed

procs ={} # {"backgrounds" : None}
procs["backgrounds"] = {
    "IDEA": ["p8_ee_ZH_Zmumu_ecm240_card_IDEA"],   
}

procs['signal'] = {
    "lighterVXD_35pc": ["p8_ee_ZH_Zmumu_ecm240_card_IDEA_lighterVXD_35pc"],
    "lighterVXD_50pc": ["p8_ee_ZH_Zmumu_ecm240_card_IDEA_lighterVXD_50pc"],    
    "3T": ["p8_ee_ZH_Zmumu_ecm240_card_IDEA_3T"],    
    "SiTracking" : ["p8_ee_ZH_Zmumu_ecm240_card_IDEA_SiTracking"],    
}



#legendTextSize =  0.015
legendCoord = [0.60,0.45,0.75,0.85]

legend = {key: key for samples in procs.values() for key in samples}



hists = {}

hists["zmumu_recoil_m"] = {
    "output": "zmumu_recoil_m",
    "logy": False,
    "stack": False,
    # "rebin": 100,
    "xmin": 120,
    "xmax": 140,
    "ymin": 0,
    "ymax": 300,
    "xtitle": "Recoil (GeV)",
    "ytitle": "Events",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": False,
    "rebin": 2,
    "xmin": 100,
    "xmax": 130,
    "ymin": 0,
    "ymax": 150,
    "xtitle": "m_{jj} (GeV)",
    "ytitle": "Events / 2 GeV",
}

hists["scoresum_B"] = {
    "output": "scoresum_B",
    "logy": True,
    "stack": False,
    "rebin": 1,
    "xmin": 0,
    "xmax": 2.0,
    "ymin": 1,
    "ymax": 100000,
    "xtitle": "p_{1}(B) + p_{2}(B)",
    "ytitle": "Events",
}