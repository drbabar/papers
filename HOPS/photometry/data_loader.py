import os
import pandas as pd
from astroquery.vizier import Vizier


def obsid_reader():
    obs_tbl = pd.read_csv("data/obsid_table.txt", sep="|")
    col_ren = {}
    [col_ren.update({col: col.strip()}) for col in obs_tbl.columns]
    obs_tbl = obs_tbl.rename(columns=col_ren)
    hops_dict = {}
    for idx, row in obs_tbl.iterrows():
        try:
            hops_ids = row['hops_ids'].split(",")
            for hid in [ihid.strip() for ihid in hops_ids]:
                if hid in hops_dict:
                    hops_dict.update({hid['group']: "{}, {}".format(hops_dict[hid]['group'], row['group'])})
                    hops_dict.update({hid['obs_date']: "{}, {}".format(hops_dict[hid]['obs_date'], row['obs_date'].strip())})
                    hops_dict.update({hid['obsid']: "{}, {}".format(hops_dict[hid]['obsid'], row['obsid'].strip())})
                else:
                    hops_dict.update({hid: {
                        'group': row['group'],
                        'obs_date': row['obs_date'].strip(),
                        'obsid': row['obsid'].strip()
                    }})
        except:
            print("idx = {}, row = {}".format(idx, row))


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

        # Compute colors
        phot_tbl['clr1'] = np.log10((70. * phot_tbl["F70"]) / (24. * phot_tbl["F24"]))
        phot_tbl['clr2'] = np.log10((160. * phot_tbl["F160"]) / (100. * phot_tbl["F100"]))

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
