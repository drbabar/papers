import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# basic pars

AB_dec_boundary = -3.83
plot_dir = "figures/"
if not os.path.exists(plot_dir):
    os.mkdir(plot_dir)
blue = sns.xkcd_rgb["denim blue"]
red = sns.xkcd_rgb["pale red"]
grey = sns.xkcd_rgb["light grey"]
style = "ticks"

# LF pars

min_bin = -2.5
max_bin = +3.5
bin_step = 0.5
nbins = int((max_bin - min_bin) / bin_step) + 1
logbins = np.arange(nbins, dtype=np.float) * bin_step + min_bin


# plotting pars

lbl_70um = "70 $\mu$m"
lbl_160um = "160 $\mu$m"
lbl_F70um = "$F_{\lambda}70\ $(Jy)"
lbl_F160um = "$F_{\lambda}160\ $(Jy)"
lbl_logF70 = "Log$_{10}\ F_{\lambda}70\ $(Jy)"
lbl_logF160 = "Log$_{10}\ F_{\lambda}160\ $(Jy)"
lbl_clr1 = "Log$_{10}\ F_{\lambda}70 / F_{\lambda}24$"
lbl_clr2 = "Log$_{10}\ F_{\lambda}160 / F_{\lambda}100$"

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


def set_cloud_order():
    return {
        'A': {
            'col': 1,
            'reg': [
                {'name': 'OMC 2-3', 'row': 0},
                {'name': 'ONC-S', 'row': 1},
                {'name': 'LDN 1641-N', 'row': 2},
                {'name': 'LDN 1641-C', 'row': 3},
                {'name': 'LDN 1641-S', 'row': 4}
            ]
        },
        'B': {
            'col': 0,
            'reg': [
                {'name': 'NGC 2023/4', 'row': 2},
                {'name': 'NGC 2068', 'row': 3},
                {'name': 'LDN 1622', 'row': 4}
            ]
        }
    }


def set_figure_layout(hspace=0, wspace=0, width=6, height=8, xlim=None, ylim=None):
    f, pTups = plt.subplots(nrows=5, ncols=2, sharex=True, sharey=True)
    f.set_figwidth(width)
    f.set_figheight(height)
    f.subplots_adjust(hspace=hspace)
    f.subplots_adjust(wspace=wspace)
    if xlim is not None:
        pTups[0][0].set_xlim(xlim[0], xlim[1])
    if ylim is not None:
        pTups[0][0].set_ylim(ylim[0], ylim[1])
    return f, pTups


def two_panel_hist_by_region(df, wlbl, logbins, filename=None,
                             color="red",
                             xlim=None, ylim=None,
                             width=6, height=8,
                             hspace=0, wspace=0,
                             xlabel=None,
                             ylabel=None):
    cloud_order = set_cloud_order()
    f, pTups = set_figure_layout(hspace=hspace, wspace=wspace, xlim=xlim, ylim=ylim, width=width, height=height)
    for cloud, cdict in cloud_order.items():
        for reg in cdict['reg']:
            p = pTups[reg['row']][cdict['col']]
            index = (df["f_" + wlbl] == 1) & (df[wlbl] > 1.e-4) & (df["region"] == reg['name'])
            y = np.log10(df[index][wlbl])
            sns.distplot(y, logbins, color=color, kde=False, axlabel=False, ax=p)
            p.set_ylabel(" ")
            p.text(3, 12, reg['name'], fontsize=10, horizontalalignment='right')
    if ylabel is not None:
        pTups[2][0].set_ylabel(ylabel)
    if xlabel is not None:
        pTups[4][0].set_xlabel(xlabel)
        pTups[4][1].set_xlabel(xlabel)
    pTups[0, 0].axis("off")
    pTups[1, 0].axis("off")
    plt.tight_layout()
    if filename is not None:
        f.savefig(filename, format="eps")
    return


def two_panel_scatter_by_region(df, xcol='clr1', ycol='clr2', filename=None,
                                xlim=None, ylim=None,
                                width=6, height=8,
                                hspace=0, wspace=0,
                                show_all=True,
                                ylabel="Log$_{10}\ \lambda F_{\lambda}\ 160 /\lambda F_{\lambda}\ 100$",
                                xlabel="Log$_{10}\ \lambda F_{\lambda}\ 70 / \lambda F_{\lambda}\ 24$",
                                scatter_all_args={'color': 'black', 'marker': '.'},
                                scatter_args={'color': 'blue', 'marker': 'o'}):
    # assign the subplot number
    cloud_order = set_cloud_order()
    f, pTups = set_figure_layout(hspace=hspace, wspace=wspace, xlim=xlim, ylim=ylim, width=width, height=height)
    for cloud, cdict in cloud_order.items():
        for reg in cdict['reg']:
            p = pTups[reg['row']][cdict['col']]
            idx = (df['cloud'] == cloud) & (df['region'] == reg['name'])
            if show_all:
                p.scatter(df[xcol], df[ycol], **scatter_all_args)
            p.scatter(df[idx][xcol], df[idx][ycol], **scatter_args)
            p.set_ylabel(" ")
            p.text(3.5, -0.1, reg['name'], fontsize=10, horizontalalignment='right')
    if ylabel is not None:
        pTups[2][0].set_ylabel(ylabel)
    if xlabel is not None:
        pTups[4][0].set_xlabel(xlabel)
        pTups[4][1].set_xlabel(xlabel)
    pTups[0, 0].axis("off")
    pTups[1, 0].axis("off")
    plt.tight_layout()
    if filename is not None:
        f.savefig(filename, format="eps")


# Stats by region

def stats_by_region(phot_tbl, add_clrs=False):
    hops_grp = phot_tbl.groupby("region")
    res = pd.DataFrame()
    idx = 0
    for name, df in hops_grp:
        good_70 = (df["f_F70"] == 1) & (df["F70"] > 1.e-4)
        y_70 = df[good_70]["F70"]
        good_160 = (df["f_F160"] == 1) & (df["F160"] > 1.e-4)
        y_160 = df[good_160]["F160"]
        clr1 = clr2 = med_clr1 = med_clr2 = std_clr1 = std_clr2 = None
        if add_clrs is True:
            clr1 = np.mean(df["clr1"])
            clr2 = np.mean(df["clr2"])
            med_clr1 = np.median(df["clr1"])
            med_clr2 = np.median(df["clr2"])
            std_clr1 = np.std(df["clr1"])
            std_clr2 = np.std(df["clr2"])
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
            "clr1": clr1,
            "clr2": clr2,
            "med_clr1": med_clr1,
            "med_clr2": med_clr2,
            "std_clr1": std_clr1,
            "std_clr2": std_clr2
        }, index=[idx])
        res = pd.concat([res, row])
        idx = idx + 1
    return res


# clrclr plots by region

def clrclr_by_region(hops_df, filename=None,
                     xlims=[0.3, 3.7], ylims=[-0.3, 1.0],
                     color="purple", all_color="black", width=6, height=8,
                     hspace=0, wspace=0):
    grp_df = hops_df.groupby('region')
    n_grps = len(grp_df.groups)
    f, pTups = plt.subplots(nrows=n_grps, ncols=1, sharex=True, sharey=True)
    f.set_figwidth(width)
    f.set_figheight(height)
    kws1 = {'color': all_color, 'marker': '.'}
    kws2 = {'color': color, 'marker': 'o'}
    i = 0
    for name, df in grp_df:
        pTups[i].scatter(x=hops_df['clr1'], y=hops_df['clr2'], **kws1)
        pTups[i].scatter(x=df['clr1'], y=df['clr2'], **kws2)
        pTups[i].set_ylabel(" ")
        pTups[i].text(2.8, -0.1, name)
        i = i + 1
    pTups[-1].set_xlabel("Log$_{10}\ \lambda F_{\lambda}\ 70 / \lambda F_{\lambda}\ 24$")
    pTups[int(n_grps / 2)].set_ylabel("Log$_{10}\ \lambda F_{\lambda}\ 160 /\lambda F_{\lambda}\ 100$")
    plt.xlim(xlims[0], xlims[1])
    plt.ylim(ylims[0], ylims[1])
    plt.subplots_adjust(wspace=wspace, hspace=hspace)
    plt.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    return


# clr vs decLow

def plt_vs_dec(hops_stats, filename=None, y=['clr1', 'med_clr1'],
               color=[blue, red], format=['o', 'o'], errors=True,
               ylabel="<Log$_{10}\ F_{\lambda}\ 70 / F_{\lambda}\ 24$>",
               x_off=None, y_off=None,
               label_bkd=grey, label_size=None,
               xticks=None, yticks=None,
               AB_dec_boundary=AB_dec_boundary):
    plt.figure()
    if isinstance(y, list):
        y0 = y[0]
        ncols = len(y)
    else:
        y0 = y
        ncols = 1
    # no checking/validation of color and formats against columns supplied
    # be careful.
    if errors:
        plt.errorbar(x=hops_stats['avg_dec'], y=hops_stats[y0], yerr=hops_stats["std_{}".format(y0)], fmt=format[0], color=color[0])
    else:
        plt.plot(hops_stats['avg_dec'], hops_stats[y0], format[0], color=color[0])
    if ncols > 1:
        for i, icol in enumerate(y[1:]):
            plt.plot(hops_stats['avg_dec'], hops_stats[icol], format[i + 1], color=color[i + 1])
    plt.xlabel("<$\delta$> (degrees)")
    if xticks is not None:
        plt.xticks(xticks)
    plt.ylabel(ylabel)
    if yticks is not None:
        plt.yticks(yticks)
    plt.axvline(x=AB_dec_boundary, ymin=0, ymax=1, linestyle='--', color='black')
    ylow, ytop = plt.ylim()
    plt.text(-4.1, ylow + 0.05 * (ytop - ylow), 'Orion A', ha='right', va='bottom')
    plt.text(-3.6, ylow + 0.05 * (ytop - ylow), 'Orion B', ha='left', va='bottom')  # , transform = ax.transAxes)
    if x_off is None:
        x_off = np.zeros(hops_stats.shape[0])
    if y_off is None:
        y_off = x_off
    for label, x, y, dx, dy in zip(hops_stats['name'], hops_stats['avg_dec'], hops_stats[y0], x_off, y_off):
        plt.annotate(label, xy=(x, y), xytext=(x + dx, y + dy),
                     rotation=90, size=label_size,
                     textcoords='data', ha='center', va='bottom',
                     bbox=dict(boxstyle='round, pad=0.5', fc=label_bkd, alpha=0.5))
    if filename is not None:
        print("Saved to file {}".format(filename))
        plt.savefig(filename)
    return
