def is_cell_site_consistent(lncel_name, mrbts):
    derived_site = lncel_name[4:8]
    mrbts_formatted = f"{mrbts:04d}"
    return derived_site == mrbts_formatted
