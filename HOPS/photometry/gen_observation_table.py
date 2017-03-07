import numpy as np
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy import units as u
import data_loader as dl


phot_tbl = dl.data_loader()
obsid_tbl = dl.obsid_from_old_table()
tex_tbl = pd.merge(phot_tbl, obsid_tbl, on="HOPS", how="left")


print("\\begin{longrotatetable}")
print("\\begin{deluxetable*}{lccccrcrcrccc}")
print("\\rotate")
print("\\tabletypesize{\\scriptsize}")
print("\\tablecolumns{13}")
print("\\tablewidth{0pt}")
print("\\tablecaption{The HOPS observation sample\\label{tbl:obs}}")
print("\\tablehead{")
print("\\colhead{HOPS} & ")
print("\\colhead{$\\alpha_{J2000}$} &")
print("\\colhead{$\\delta_{J2000}$} &")
print("\\colhead{Observation} &")
print("\\colhead{Group} &")
print("\\colhead{$70\\mu$m} &")
print("\\colhead{flag} &")
print("\\colhead{$100\\mu$m} &")
print("\\colhead{flag} &")
print("\\colhead{$160\\mu$m} &")
print("\\colhead{flag} &")
print("\\colhead{Field} &")
print("\\colhead{Observation Date} \\\\")
print("\\colhead{ID} & ")
print("\\colhead{h:m:s} &")
print("\\colhead{$^{\rm o}:^\\prime:^{\\prime\\prime}$} &")
print("\\colhead{Identifiers} &")
print("\\colhead{Number} &")
print("\\colhead{(mJy)} &")
print("\\colhead{} &")
print("\\colhead{(mJy)} &")
print("\\colhead{} &")
print("\\colhead{(mJy)} &")
print("\\colhead{} &")
print("\\colhead{} &")
print("\\colhead{(UT)}")
print("}")
print("\\startdata")

sep = " & "
for i, row in tex_tbl.iterrows():
    coo = SkyCoord(ra=row["RA"] * u.degree, dec=row["Dec"] * u.degree, frame="icrs")
    rastr = "%2.2i:%2.2i:%4.2f" % (coo.ra.hms[0], coo.ra.hms[1], coo.ra.hms[2])
    decstr = "%3.2i:%2.2i:%3.1f" % (coo.dec.dms[0], np.abs(coo.dec.dms[1]), np.abs(coo.dec.dms[2]))
    line = " "
    line = line + "%3.3i & " % (row["HOPS"])
    line = line + "%11s & " % (rastr)
    line = line + "%11s & " % (decstr)
    line = line + "%13s & " % (row["obsids"])
    if pd.isnull(row["group"]):
        line = line + " & "
    else:
        line = line + "%3.3i & " % (row["group"])
    line = line + "%8.3f & " % (row["F70"])
    line = line + "%8.3f & " % (row["f_F70"])
    line = line + "%8.3f & " % (row["F100"])
    line = line + "%8.3f & " % (row["f_F100"])
    line = line + "%8.3f & " % (row["F160"])
    line = line + "%8.3f & " % (row["f_F160"])
    line = line + "%-15s & " % (row["region_old"])
    line = line + "%-20s \\\\ " % (row["obs_date"])
    print(line)
print("\\enddata")
print("\\tablenotetext{a}{Taken with PACS in high dynamic range mode.}")
print("\\tablenotetext{b}{Taken during science demonstration phase.}")
print("\\end{deluxetable*}")
