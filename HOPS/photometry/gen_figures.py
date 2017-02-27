import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import data_loader as dl
import figure_helpers as fh


phot_tbl = dl.data_loader()


# Total Lum Functions
#
y70 = np.log10(phot_tbl[fh.data_selector(phot_tbl, "F70")]["F70"])
y160 = np.log10(phot_tbl[fh.data_selector(phot_tbl, "F160")]["F160"])
sns.set_style(fh.style)
sns.despine()
f, (p1, p2) = plt.subplots(2, sharex=True, sharey=True)
fh.single_LF(y70, p1, color=fh.blue, ylim=[0, 39])
fh.single_LF(y160, p2, color=fh.red, ylim=[0, 39])
f.subplots_adjust(hspace=0)
p1.text(-2, 30, fh.lbl_70um)
p2.text(-2, 30, fh.lbl_160um)
plt.xlabel("Log$_{10}\ F_{\lambda}\ $(Jy)")
p1.set_ylabel("Number")
p2.set_ylabel("Number")
plt.tight_layout()
plt.savefig("{}LFs.eps".format(fh.plot_dir))
plt.show()


# LFs by region

reg_df = dl.regions()

sns.set_style(fh.style)
sns.despine()
fh.LF_by_region(phot_tbl, reg_df, "F70", fh.logbins, color=fh.blue,
                hspace=0.05, wspace=0.05,
                figname="{}LF70_byregion.eps".format(fh.plot_dir))
plt.show()

sns.set_style(fh.style)
sns.despine()
fh.LF_by_region(phot_tbl, reg_df, "F160", fh.logbins, color=fh.red,
                hspace=0.05, wspace=0.05,
                figname="{}LF160_byregion.eps".format(fh.plot_dir))
plt.show()


# Flux vs declination

stat_df = fh.stats_by_region(phot_tbl)
stat_df = stat_df.sort_values(by="avg_dec")

sns.set(style=fh.style)
sns.despine()
plt.scatter(stat_df['avg_dec'], stat_df['med_F70'], color=fh.blue, marker="o", s=100)
plt.plot(stat_df['avg_dec'], stat_df['med_F70'], color=fh.blue)
plt.scatter(stat_df['avg_dec'], stat_df['med_F160'], color=fh.red, marker="o", s=100)
plt.plot(stat_df['avg_dec'], stat_df['med_F160'], color=fh.red)
plt.xlim(-9., 2.5)
yr = [-2., 45.]
plt.ylim(yr[0], yr[1])
x_offset = np.zeros(stat_df.shape[0]) + 3
y_offset = np.zeros(stat_df.shape[0]) + 15
x_offset[4] = -10
y_offset[4] = -60
x_offset[5] = 5
x_offset[7] = 5
for label, x, y, x_off, y_off in zip(stat_df['name'], stat_df['avg_dec'], stat_df['med_F160'], x_offset, y_offset):
    plt.annotate(
        label,
        xy=(x, y), xytext=(x_off, y_off), rotation=90,
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round, pad=0.5', fc=fh.grey, alpha=0.5))
plt.plot([-3.83, -3.83], yr, 'k--')
plt.text(-4.1, yr[0] + 1, 'Orion A', ha='right', va='bottom')
plt.text(-3.6, yr[0] + 1, 'Orion B', ha='left', va='bottom')
plt.xlabel("<$\delta$> (degrees)")
plt.ylabel("Median $F_{\lambda}$ (Jy)")
plt.tight_layout()
plt.savefig("{}mdFlux_v_dec.eps".format(fh.plot_dir))
