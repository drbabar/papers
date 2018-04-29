import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import data_loader as dl
import figure_helpers as fh


phot_tbl = dl.data_loader(verbose=False)

# Total Lum Functions
#
y70 = np.log10(phot_tbl[fh.data_selector(phot_tbl, "F70")]["F70"])
y160 = np.log10(phot_tbl[fh.data_selector(phot_tbl, "F160")]["F160"])
with sns.axes_style(fh.style):
    f, (p1, p2) = plt.subplots(2, sharex=True, sharey=True)
    fh.single_LF(y70, p1, color=fh.blue, ylim=[0, 80])
    fh.single_LF(y160, p2, color=fh.red, ylim=[0, 80])
    # fh.single_LF(y160, p2, color=fh.red, ylim=[0, 39])
    f.subplots_adjust(hspace=0)
    p1.text(-2, 30, fh.lbl_70um)
    p2.text(-2, 30, fh.lbl_160um)
    plt.xlabel("Log$_{10}\ F_{\\nu}\ $(Jy)")
    p1.set_ylabel("Number")
    p2.set_ylabel("Number")
    plt.tight_layout()
    sns.despine()
    plt.savefig("{}LFs.eps".format(fh.plot_dir))
plt.show()


# LFs by region

with sns.axes_style(fh.style):
    sns.set_context('paper')
    fh.two_panel_hist_by_region(phot_tbl, "F70", fh.logbins, color=fh.blue,
                                hspace=0.05, wspace=0.05,
                                xlabel=fh.lbl_logF70,
                                ylabel="Number",
                                filename="{}LF70_byregion.eps".format(fh.plot_dir))
    sns.despine()
plt.show()


with sns.axes_style(fh.style):
    sns.set_context('paper')
    fh.two_panel_hist_by_region(phot_tbl, "F160", fh.logbins, color=fh.red,
                                hspace=0.05, wspace=0.05,
                                xlabel=fh.lbl_logF160,
                                ylabel="Number",
                                filename="{}LF160_byregion.eps".format(fh.plot_dir))
    sns.despine()
plt.show()


# Flux vs declination

stat_df = fh.stats_by_region(phot_tbl)
stat_df = stat_df.sort_values(by="avg_dec").reset_index()

x_off = np.zeros(stat_df.shape[0])
y_off = np.zeros(stat_df.shape[0]) + 5
y_off[2] = +7
y_off[3] = +13
y_off[4] = +15
y_off[5] = +13
y_off[6] = +12
y_off[7] = 5
with sns.axes_style(fh.style):
    sns.set_context('paper')
    fh.plt_vs_dec(stat_df, y=['med_F70', 'med_F70', 'med_F160', 'med_F160'],
                  color=[fh.blue, fh.blue, fh.red, fh.red],
                  format=['o', '-', 'o', '-'],
                  ylabel="Median $F_{\\nu}$ (Jy)",
                  x_off=x_off, y_off=y_off,
                  xticks=np.arange(-8.5, 2.5, 1),
                  errors=False,
                  filename="{}mdFlux_v_dec.eps".format(fh.plot_dir))
    sns.despine()
plt.show()


# clr-clr plots

stat_70 = fh.data_selector(phot_tbl, "F70")
stat_100 = fh.data_selector(phot_tbl, "F100")
stat_160 = fh.data_selector(phot_tbl, "F160")
stat_24 = fh.data_selector(phot_tbl, "F24")
good_rows = stat_70 & stat_100 & stat_160 & stat_24
hops_good = phot_tbl[good_rows]
hops_good.loc[:, 'clr1'] = np.log10((70. * hops_good["F70"]) / (24. * hops_good["F24"]))
hops_good.loc[:, 'clr2'] = np.log10((160. * hops_good["F160"]) / (100. * hops_good["F100"]))

with sns.axes_style(fh.style):
    sns.set_context('paper')
    fh.two_panel_scatter_by_region(hops_good,
                                   filename="{}clrclr.eps".format(fh.plot_dir),
                                   scatter_args={'color': fh.red, 'marker': 'o'},
                                   scatter_all_args={'color': fh.grey, 'marker': '.'})
    sns.despine()
plt.show()


# clr vs dec

hops_stats = fh.stats_by_region(hops_good, add_clrs=True)
hops_stats = hops_stats.sort_values(by="avg_dec").reset_index()

x_off = np.zeros(hops_stats.shape[0])
y_off = x_off + hops_stats['std_clr1'] + 0.1
y_off[5] = 0
x_off[5] = 0.5
y_off[6] = 0
x_off[6] = 0.5
with sns.axes_style(fh.style):
    sns.set_context('paper')
    fh.plt_vs_dec(hops_stats, y=['clr1', 'med_clr1'], color=[fh.blue, fh.red],
                  ylabel="<{}>".format(fh.lbl_clr1),
                  x_off=x_off, y_off=y_off,
                  xticks=np.arange(-8.5, 2.5, 1),
                  filename="{}clr1_vs_dec.eps".format(fh.plot_dir))
    sns.despine()
plt.show()


x_off = np.zeros(hops_stats.shape[0])
y_off = x_off
x_off = x_off + 0.4
with sns.axes_style(fh.style):
    sns.set_context('paper')
    fh.plt_vs_dec(hops_stats, y=['clr2', 'med_clr2'], color=[fh.blue, fh.red],
                  ylabel="<{}>".format(fh.lbl_clr2),
                  x_off=x_off, y_off=y_off, label_size=8,
                  xticks=np.arange(-8.5, 2.5, 1),
                  filename="{}clr2_vs_dec.eps".format(fh.plot_dir))
    sns.despine()
plt.show()


# Number vs dec

x_off = np.zeros(stat_df.shape[0])
y_off = x_off + 3
y_off[0] = y_off[0] - 20
with sns.axes_style(fh.style):
    sns.set_context('paper')
    fh.plt_vs_dec(stat_df, y=["n_F70", "n_F70"],
                  color=[fh.blue, fh.blue], format=['o', '-'],
                  ylabel="Number of Protostars at {}".format(fh.lbl_70um),
                  xticks=np.arange(-8.5, 2.5, 1),
                  x_off=x_off, y_off=y_off, label_size=8,
                  errors=False,
                  filename="{}num_vs_dec.eps".format(fh.plot_dir))
    sns.despine()
plt.show()


# Flux vs color plots

with sns.axes_style(fh.style):
    sns.set_context('paper')
    f, axs = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=True)
    f.set_figwidth(8)
    f.set_figheight(6)
    f.subplots_adjust(hspace=0)
    f.subplots_adjust(wspace=0)
    g0 = sns.regplot(y="F70", x="clr1", data=phot_tbl, fit_reg=False, color=fh.blue, ax=axs[0])
    g0.set_yscale('log')
    g0.set_xlabel(fh.lbl_clr1)
    g0.set_ylabel(fh.lbl_F70um)
    g1 = sns.regplot(y="F70", x="clr2", data=phot_tbl, fit_reg=False, color=fh.red, ax=axs[1])
    g1.set_xlabel(fh.lbl_clr2)
    g1.set_ylabel(" ")
    sns.despine()
    plt.savefig("{}f70_v_clr2.eps".format(fh.plot_dir))
plt.show()


# Aperture and Photometry comparison

s_df = dl.load_psf_aper_phot_comparison_table()
wm_grid = [tuple([w, m]) for m in ["aper", "PSF"] for w in [160, 70]]
phots = [dl.read_phot_file(w, m) for w, m in wm_grid]
phots_df = phots[0]
for df in phots[1:]:
    phots_df = pd.merge(phots_df, df, on="HOPS", how="outer")
df = pd.merge(s_df, phots_df[["HOPS", "P70", "PSF_70", "P160", "PSF_160"]],
              on="HOPS", how="left")

codes = ['s', 'c', 'b']
lbls = ['Isolated', 'Nearby companion(s)', 'Strong background emission']
clrs = [fh.grey2, fh.blue, fh.red]

with sns.axes_style(fh.style):
    sns.set_context('paper')
    f, axs = plt.subplots(nrows=1, ncols=2, figsize=(10, 8), sharex=False, sharey=False)
    for code, lbl, clr in zip(codes, lbls, clrs):
        sdf = df[df['clustering_code'] == code]
        axs[0].scatter(sdf['P70'], sdf['PSF_70'], color=clr, label=lbl)
        axs[1].scatter(sdf['P160'], sdf['PSF_160'], color=clr, label=lbl)
    xym = [min(min(df['P70']), min(df['PSF_70'])),
           max(max(df['P70']), max(df['PSF_70']))]
    axs[0].plot(xym, xym, linestyle='--', color="black")
    axs[0].set_xscale("log")
    axs[0].set_yscale("log")
    xym = [min(min(df['P160']), min(df['PSF_160'])),
           max(max(df['P160']), max(df['PSF_160']))]
    axs[1].plot(xym, xym, linestyle='--', color="black")
    axs[1].set_xscale("log")
    axs[1].set_yscale("log")
    axs[0].set_xlabel("using aperture photometry", size=16)
    axs[1].set_xlabel("using aperture photometry", size=16)
    axs[0].set_ylabel("using PSF photometry", size=16)
    axs[0].set_title("{}".format(fh.lbl_F70um), size=18)
    axs[1].set_title("{}".format(fh.lbl_F160um), size=18)
    axs[0].legend(loc="upper left", frameon=True)
    sns.despine()
    plt.savefig("{}aper_vs_psf.eps".format(fh.plot_dir))
plt.show()
