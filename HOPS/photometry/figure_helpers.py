import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# basic pars

plot_dir = "figures/"
if not os.path.exists(plot_dir):
    os.mkdir(plot_dir)
blue = sns.xkcd_rgb["denim blue"]
red = sns.xkcd_rgb["pale red"]
grey = sns.xkcd_rgb["light grey"]
style = "ticks"

# LF pars

min_bin = -2.4
max_bin = +3.4
bin_step = 0.2
nbins = int((max_bin - min_bin) / bin_step) + 1
logbins = np.arange(nbins, dtype=np.float) * bin_step + min_bin


# plotting pars

lbl_70um = "70 $\mu$m"
lbl_160um = "160 $\mu$m"
lbl_logF70 = "Log$_{10}\ F_{\lambda}70\ $(Jy)"
lbl_logF160 = "Log$_{10}\ F_{\lambda}160\ $(Jy)"


# helper functions

def data_selector(df, col):
    return (df["f_{}".format(col)] == 1) & (df[col].isnull() == False)


def single_LF(y, ax, color=blue, ylim=[0, 39]):
    sns.set_style(style)
    sns.despine()
    sns.distplot(y, bins=logbins, kde=False, color=color, ax=ax, axlabel=False)
    ax.set_xlim(min_bin, max_bin)
    ax.set_ylim(ylim[0], ylim[1])
    ax.set_xticks(np.arange(min_bin, max_bin + 0.5, 0.5))


def LF_by_region(phot_tbl, region_df, wlbl, logbins, figname=None,
                 xlim=[-2.4, 3.4], ylim=[-0.5, 14.5],
                 color="purple", width=6, height=8,
                 hspace=0, wspace=0):
    # assign the subplot number
    # spi = [1, 3, 5, 2, 4, 6, 8, 10]
    rI = [2, 3, 4, 0, 1, 2, 3, 4]
    cI = [0, 0, 0, 1, 1, 1, 1, 1]
    #
    f, pTups = plt.subplots(nrows=5, ncols=2, sharex=True, sharey=True)
    f.set_figwidth(width)
    f.set_figheight(height)
    f.subplots_adjust(hspace=hspace)
    f.subplots_adjust(wspace=wspace)
    pTups[0][0].set_xlim(xlim[0], xlim[1])
    pTups[0][0].set_ylim(ylim[0], ylim[1])
    pTups[2][0].set_ylabel("Number")
    pTups[4][0].set_xlabel("Log$_{10}\ F_{\lambda}\ $" + wlbl.replace("F", "") + "$\mu$m (Jy)")
    pTups[4][1].set_xlabel("Log$_{10}\ F_{\lambda}\ $" + wlbl.replace("F", "") + "$\mu$m (Jy)")
    for i in range(len(region_df["name"])):
        p = pTups[rI[i]][cI[i]]
        regname = region_df["name"][i].strip()
        index = np.where((phot_tbl["f_" + wlbl] == 1) & (phot_tbl[wlbl] > 1.e-4) & (phot_tbl["Dec"] >= region_df["decLow"][i]) & (phot_tbl["Dec"] < region_df["decHigh"][i]))[0]
        y = np.log10(phot_tbl[wlbl][index])
        sns.distplot(y, logbins, color=color, kde=False, axlabel=False, ax=p)
        p.text(3, 12, regname, fontsize=10, horizontalalignment='right')
    pTups[0, 0].axis("off")
    pTups[1, 0].axis("off")
    plt.tight_layout()
    if figname is not None:
        f.savefig(figname, format="eps")


# Stats by region

def stats_by_region(phot_tbl):
    hops_grp = phot_tbl.groupby("region")
    res = pd.DataFrame()
    idx = 0
    for name, df in hops_grp:
        good_70 = (df["f_F70"] == 1) & (df["F70"] > 1.e-4)
        y_70 = df[good_70]["F70"]
        good_160 = (df["f_F160"] == 1) & (df["F160"] > 1.e-4)
        y_160 = df[good_160]["F160"]
        row = pd.DataFrame({
            "name": name,
            "avg_dec": np.mean(df[good_70]["Dec"]),
            "n_F70": len(y_70),
            "avg_F70": np.mean(y_70),
            "med_F70": np.median(y_70),
            "std_F70": np.std(y_70),
            "n_F160": len(y_160),
            "avg_F160": np.mean(y_160),
            "med_F160": np.median(y_160),
            "std_F160": np.std(y_160),
        }, index=[idx])
        res = pd.concat([res, row])
        idx = idx + 1
    return res


# clrclr plots by region

def clrclr_by_region(hops_df, hopsx, hopsy, figname=None,
                     xlims=[0.3, 3.7], ylims=[-0.3, 1.0],
                     color="purple", all_color="black", width=6, height=8,
                     hspace=0.02, wspace=0.02, style="ticks"):
    grp_df = hops_df.groupby('region')
    sns.set_style(style)
    sns.despine()
    f, pTups = plt.subplots(nrows=len(grp_df.groups.keys()), ncols=1, sharex=True, sharey=True)
    f.set_figwidth(width)
    f.set_figheight(height)
    f.subplots_adjust(hspace=hspace)
    f.subplots_adjust(wspace=wspace)
    kws1 = {'color': all_color, 'marker': '.'}
    kws2 = {'color': color, 'marker': 'o'}
    i = 0
    for name, df in grp_df:
        sns.regplot(x=hopsx, y=hopsy, ax=pTups[i], fit_reg=False, scatter_kws=kws1)
        sns.regplot(x=df['clr1'], y=df['clr2'], fit_reg=False, ax=pTups[i], scatter_kws=kws2)
        pTups[i].set_ylabel(" ")
        pTups[i].text(2.8, -0.1, name)
        i = i + 1
    pTups[-1].set_xlabel("Log$_{10}\ \lambda F_{\lambda}\ 70 / \lambda F_{\lambda}\ 24$")
    pTups[1].set_ylabel("Log$_{10}\ \lambda F_{\lambda}\ 160 /\lambda F_{\lambda}\ 100$")
    plt.xlim(xlims[0], xlims[1])
    plt.ylim(ylims[0], ylims[1])
    plt.tight_layout()
    if figname is not None:
        plt.savefig(figname)
    return
