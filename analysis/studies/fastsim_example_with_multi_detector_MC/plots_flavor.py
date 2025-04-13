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
plotStatUnc = True

colors = {}
colors["ZH_IDEA"] = ROOT.kRed
colors["ZH_IDEA_lighterVXD_35pc"] = ROOT.kGreen + 2
colors["ZH_IDEA_lighterVXD_50pc"] = ROOT.kBlue + 2

procs = {}
procs["signal"] = {"ZH_IDEA": ["p8_ee_ZH_Zmumu_ecm240_card_IDEA"]}
procs["backgrounds"] = {
    "ZH_IDEA_lighterVXD_35pc": ["p8_ee_ZH_Zmumu_ecm240_card_IDEA_lighterVXD_35pc"],
    "ZH_IDEA_lighterVXD_50pc": ["p8_ee_ZH_Zmumu_ecm240_card_IDEA_lighterVXD_50pc"],    
}

legend = {}
legend["ZH_IDEA"] = "ZH_IDEA"
legend["ZH_IDEA_lighterVXD_35pc"] = "ZH_IDEA_lighterVXD_35pc"
legend["ZH_IDEA_lighterVXD_50pc"] = "ZH_IDEA_lighterVXD_50pc"

hists = {}

hists["zmumu_recoil_m"] = {
    "output": "zmumu_recoil_m",
    "logy": False,
    "stack": True,
    "rebin": 100,
    "xmin": 120,
    "xmax": 140,
    "ymin": 0,
    "ymax": 200,
    "xtitle": "Recoil (GeV)",
    "ytitle": "Events / 100 MeV",
}

hists["jj_m"] = {
    "output": "jj_m",
    "logy": False,
    "stack": True,
    "rebin": 2,
    "xmin": 50,
    "xmax": 150,
    "ymin": 0,
    "ymax": 4000,
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