import os
import pandas as pd
from astroquery.vizier import Vizier


def regions():
    reg_df = pd.read_csv("data/HOPS_region_definitions.txt", comment='#', sep="|")
    cols = reg_df.columns
    cols_renamer = {}
    [cols_renamer.update({col: col.strip()}) for col in cols]
    return reg_df.rename(columns=cols_renamer)


def data_loader(photometry_file="data/photometry_table.csv", use_the_force=False, verbose=True):
    exists = os.path.exists(photometry_file)

    if not exists or use_the_force is True:
        if verbose:
            print("Generating final data table ... ", end='', flush=True)
        # SED catalog from Vizier
        # catalog_list = Vizier.find_catalogs('The Herschel Orion Protostar Survey (HOPS): SEDs')
        Vizier.ROW_LIMIT = -1
        catalogs = Vizier.get_catalogs('J/ApJS/224/5')
        sed_tbl = catalogs[1].to_pandas()
        sed_tbl.loc[:, "HOPS"] = sed_tbl["HOPS"].astype('int')

        # Pick up coordinates and the remaining photometry.
        hops_old = pd.read_csv("data/HOPS_2MASS_IRAC_MIPS_photometry_03Mar2015.txt", delim_whitespace=True, comment="#")

        # Start building the final table.

        # (1) Merge all photometry and coordinates.
        phot_tbl = pd.merge(sed_tbl, hops_old, on="HOPS", how="left")

        # (2) Define regions
        reg_df = regions()
        reg_cuts = pd.Series(reg_df['decHigh'].iloc[0]).append(reg_df['decLow'])[::-1]
        reg_lbls = [reg.strip() for reg in pd.Series(reg_df['name'])[::-1]]
        phot_tbl['region'] = pd.cut(phot_tbl['Dec'], bins=reg_cuts, labels=reg_lbls)
        phot_tbl['cloud'] = pd.cut(phot_tbl['Dec'], bins=[-10, -4, 10], labels=['A', 'B'])

        # (3) Find out if the final photometry in the Vizier table
        #     PSF or Aperture

        def read_phot_file(wavelength, method):
            suff = 'final'
            if method == 'aper':
                suff = 'summary'
            fname = "data/HOPS_PACS{}_{}_photometry_{}_083016.txt".format(wavelength, method, suff)
            return pd.read_csv(fname, comment="#", skiprows=1, delim_whitespace=True, header=1)

        wm_grid = [tuple([w, m]) for m in ["aper", "PSF"] for w in [160, 70]]
        # phots = {}
        # [phots.update({"{}_{}".format(w, m): read_phot_file(w, m)}) for w, m in wm_grid]
        phots = [read_phot_file(w, m) for w, m in wm_grid]
        phots_df = phots[0]
        for df in phots[1:]:
            phots_df = pd.merge(phots_df, df, on="HOPS", how="outer")

        meth_df = pd.merge(phot_tbl[["HOPS", "F70", "F160"]],
                           phots_df[["HOPS", "P70", "PSF_70", "P160", "PSF_160"]],
                           on="HOPS", how="left")
        meth_df['m_F70'] = ["P" if res == True else "A" for res in abs(meth_df['F70'] - meth_df['P70']) > abs(meth_df['F70'] - meth_df['PSF_70'])]
        meth_df['m_F160'] = ["P" if res == True else "A" for res in abs(meth_df['F160'] - meth_df['P160']) > abs(meth_df['F160'] - meth_df['PSF_160'])]

        phot_tbl = pd.merge(phot_tbl, meth_df[["HOPS", "m_F70", "m_F160"]], on="HOPS", how="left")
        if verbose:
            print("done.")
        phot_tbl.to_csv(photometry_file)
        if verbose:
            print("Final prepared data table written to {} in CSV format.".format(photometry_file))

    else:
        if verbose:
            print("Reading prepared data table {}".format(photometry_file))
        phot_tbl = pd.read_csv(photometry_file)

    return phot_tbl
