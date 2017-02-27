good_rows = (hopsphot["F70"] > 1.e-4) & (hopsphot["f_F70"] == 1) &\
            (hopsphot["F100"] > 1.e-4) & (hopsphot["f_F100"] == 1) &\
            (hopsphot["F160"] > 1.e-4) & (hopsphot["f_F160"] == 1) &\
            (hopsphot["f_F24"] == 1)

hops_good = hopsphot[good_rows]
hops_good['clr1'] = np.log10((70. * hops_good["F70"]) / (24. * hops_good["F24"]))
hops_good['clr2'] = np.log10((160. * hops_good["F160"]) / (100. * hops_good["F100"]))
#

# test, not really any good.

sns.set_style(style)
sns.despine()
g = sns.FacetGrid(hops_good[hops_good['cloud'] == 'A'], row="region",
                  sharex=True, sharey=True, xlim=xlims, ylim=ylims)
g.map(plt.scatter, "clr1", "clr2", edgecolor="w")
plt.xlabel("Log$_{10} \lambda F_{\lambda}\ 70 / \lambda F_{\lambda}\ 24$")
plt.ylabel("Log$_{10} \lambda F_{\lambda}\ 160 /\lambda F_{\lambda}\ 100$")
plt.xlim(xlims[0], xlims[1])
plt.ylim(ylims[0], ylims[1])
plt.show()


# Generate color-color plots.

def gen_clrclr_by_region(hops_df, hopsx, hopsy, figname=None,
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
    sns.despine()
    if figname is not None:
        plt.savefig(figname)
    return

gen_clrclr_by_region(hops_good[hops_good['cloud'] == 'A'], hops_good['clr1'], hops_good['clr2'],
                     figname="{}{}OrionA_clrclr.eps".format(top_dir, plot_dir),
                     hspace=0.05,
                     color=red, all_color=grey)
plt.show()

gen_clrclr_by_region(hops_good[hops_good['cloud'] == 'B'], hops_good['clr1'], hops_good['clr2'],
                     figname="{}{}OrionB_clrclr.eps".format(top_dir, plot_dir),
                     hspace=0.05,
                     color=red, all_color=grey)
plt.show()


#
# Mean X vs dec.

yr = [0, 4.0]
reg_order = stat_df['name'][np.argsort(stat_df['avg_dec'])]
sns.boxplot(data=hops_good, x="region", y="clr1", color=blue, order=reg_order)
plt.ylabel("<Log$_{10}\ F_{\lambda}\ 70 / F_{\lambda}\ 24$>")
plt.xlabel("<$\delta$> (degrees)")
plt.ylim(yr[0], yr[1])
plt.plot([-3.83, -3.83], yr, 'k--')
plt.text(-4.1, yr[0]+0.05, 'Orion A', ha='right', va='bottom')
plt.text(-3.6, yr[0]+0.05, 'Orion B', ha='left', va='bottom')
plt.show()


def clr_vs_dec(hops_df, style='ticks', filename=None, clrcol='clr1', color="blue"):
    y_lbl = "<Log$_{10}\ F_{\lambda}\ 70 / F_{\lambda}\ 24$>"
    if clrcol == 'clr2':
        "<Log$_{10}\ F_{\lambda}\ 160 / F_{\lambda}\ 100$>"
    sns.set_style(style)
    kws2 = {'color': color, 'marker': 'o', 's': 100}
    grp_df = hops_df.groupby('region')
    for name, df in grp_df:
        avg_dec = np.mean(df['Dec'])
        avg_clr = np.mean(df[clrcol])
        med_clr = np.
        sns.regplot(x=avg_dec, y=avg_clr, fit_reg=False, scatter_kws=kws2)
        plt.text(avg_dec, avg_clr, name, rotation=90)
    sns.despine()
    if filename is not None:
        plt.savefit(filename)
    return

clr_vs_dec(hops_good, color=red)

indA = np.where(regData["decLow"]<-3.9)
indB = np.where(regData["decLow"]>=-3.9)
#
PL.figure()
PL.errorbar(mnDec,mnX,sdX,c='black',capsize=0,marker='o',markersize=10,fmt='ro')
PL.scatter(mnDec,mdX,c='red',s=100)
PL.xlim(-9.5,3.0)
yr = [0.4,2.8]
PL.ylim(yr[0],yr[1])
PL.xlabel("<$\delta$> (degrees)")
PL.ylabel("<Log$_{10}\ F_{\lambda}\ 70 / F_{\lambda}\ 24$>")
for j in indA[0]:
   PL.text(mnDec[j],mnX[j]+sdX[j]+0.05,regData["name"][j].strip(),rotation=90,color='blue',ha='center',va='bottom')
for j in indB[0]:
   PL.text(mnDec[j]+0.3,mnX[j]+0.05,regData["name"][j].strip(),rotation=90,color='blue',ha='center',va='bottom')
PL.plot([-3.83,-3.83],yr,'k--')
PL.text(-4.1,yr[0]+0.05,'Orion A',ha='right',va='bottom')
PL.text(-3.6,yr[0]+0.05,'Orion B',ha='left',va='bottom')
PL.savefig(topdir+"clr1_vs_dec.png")
PL.close()
#
PL.figure()
PL.errorbar(mnDec,mnY,sdY,c='black',capsize=0,marker='o',markersize=10,fmt='ro')
PL.scatter(mnDec,mdY,c='red',s=100)
PL.xlim(-9.5,3.0)
yr = [0.0,0.55]
PL.ylim(yr[0],yr[1])
PL.xlabel("<$\delta$> (degrees)")
PL.ylabel("<Log$_{10}\ F_{\lambda}\ 160 / F_{\lambda}\ 100$>")
for i in indA[0]:
   PL.text(mnDec[i]+0.2,mnY[i]+0.04,regData["name"][i].strip(),rotation=90,color='blue',ha='center',va='bottom')
for i in indB[0]:
   PL.text(mnDec[i]+0.2,mnY[i]+0.04,regData["name"][i].strip(),rotation=90,color='blue',ha='center',va='bottom')
PL.plot([-3.83,-3.83],yr,'k--')
PL.text(-4.1,yr[0]+0.05,'Orion A',ha='right',va='bottom')
PL.text(-3.6,yr[0]+0.05,'Orion B',ha='left',va='bottom')
PL.savefig(topdir+"clr2_vs_dec.png")
PL.close()
#
#PL.show()
