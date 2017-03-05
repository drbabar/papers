

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
