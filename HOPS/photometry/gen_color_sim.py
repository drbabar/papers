import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import data_loader as dl
import figure_helpers as fh


phot_tbl = dl.data_loader()


#
# As a function of flux limit.

# Declination ranges for the two target regions.
# L 1641, and
# OMC 2/3 and ONC-S

decs = {
    'L1641': [-8.3333, -6.5],
    'OMC': [-6.50, -3.83]
}

stat_70 = fh.data_selector(phot_tbl, "F70")
stat_100 = fh.data_selector(phot_tbl, "F100")
stat_160 = fh.data_selector(phot_tbl, "F160")
stat_24 = fh.data_selector(phot_tbl, "F24")

decs1 = (phot_tbl['Dec'] > decs['L1641'][0]) & (phot_tbl['Dec'] <= decs["L1641"][1])
decs2 = (phot_tbl['Dec'] > decs['OMC'][0]) & (phot_tbl['Dec'] <= decs["OMC"][1])

flux_range = np.arange(0.1, 1.1, 0.05)
clr1_1641 = flux_range * 0
clr2_1641 = flux_range * 0
for i, flux in enumerate(flux_range):
    q1 = (phot_tbl["F70"] > flux) & stat_24 & stat_70 & decs1
    clr1_1641[i] = np.mean(phot_tbl[q1]['clr1'])
    q2 = (phot_tbl["F70"] > flux) & stat_100 & stat_160 & stat_70 & decs1
    clr2_1641[i] = np.mean(phot_tbl[q2]['clr2'])

q1_omc = stat_24 & stat_70 & decs2
clr1_omc = np.mean(phot_tbl[q1_omc]["clr1"])

q2_omc = stat_70 & stat_100 & stat_160 & decs2
clr2_omc = np.mean(phot_tbl[q2_omc]["clr2"])

# Figure

with sns.axes_style(fh.style):
    sns.set_context('paper')
    sns.despine()
    plt.plot(flux_range, clr1_1641, '-', color=fh.blue)
    plt.plot(flux_range, clr2_1641, '-', color=fh.red)
    plt.axhline(y=clr1_omc, linestyle='--', color=fh.blue)
    plt.axhline(y=clr2_omc, linestyle='--', color=fh.red)
    plt.xlim(0.08, 1.08)
    plt.ylim(0.2, 1.6)
    plt.text(0.1, clr1_omc + 0.05, "{} Orion A North".format(fh.lbl_clr1))
    plt.text(0.1, clr2_omc + 0.05, "{} Orion A North".format(fh.lbl_clr2))
    plt.xlabel("Flux Limit (Jy)")
    plt.ylabel("Mean Value of Flux Density Ratio")
    plt.savefig("{}clr_vs_flimit.eps".format(fh.plot_dir))
plt.show()
