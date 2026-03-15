from src.parsers.xml_parser import extract_selected_objects_stream
from src.db.cells_repository import ingest_cells_to_db
from src.db.sites_repository import ingest_sites_to_db, select_mrbts_site_id
from src.config.db_config import db_config
from src.validation.cell_validations import is_cell_site_consistent

def ingest_xml_topology(xml_path):  
    selected_classes = {"MRBTS", "LNBTS", "LNCEL"}
    obj_p = {"name","enbName"}
    conflicted_cell_site={}
    cells_rows=[]
    sites_dict={}
    seen_lncel = set()
    duplicate_lncel = {}
    for obj in extract_selected_objects_stream(xml_path,selected_classes,obj_p):
        if obj["class"] == "MRBTS":
            mrbts= int(obj["MRBTS"])
            mrbts_name = obj["name"]
            site_distname = obj["distName"]
            if mrbts not in sites_dict:
                sites_dict[mrbts] = {}
            sites_dict[mrbts].update({
                'mrbts':mrbts,
                'mrbts_name': mrbts_name,
                'distname':site_distname
            })
        elif obj["class"] == "LNBTS":
            lnbts=int(obj["LNBTS"])
            lnbts_name=obj["name"]
            enb_name=obj["enbName"]
            lnbts_mrbts=int(obj["MRBTS"])
            if lnbts_mrbts not in sites_dict:
                sites_dict[lnbts_mrbts] = {"mrbts":lnbts_mrbts}
            sites_dict[lnbts_mrbts].update({
                'lnbts':lnbts,
                'lnbts_name':lnbts_name,
                'enb_name':enb_name
                })
        elif obj["class"] == "LNCEL":
            lncel=int(obj["LNCEL"])
            if lncel in seen_lncel:
                duplicate_lncel.setdefault(lncel, []).append(obj)
                continue
            seen_lncel.add(lncel)
            cell_mrbts=int(obj["MRBTS"])
            lncel_name = obj["name"]
            cell_distname = obj["distName"]
            
            if not is_cell_site_consistent(lncel_name,cell_mrbts):
                if lncel not in conflicted_cell_site:
                    conflicted_cell_site[lncel]=[{"mrbts":cell_mrbts,"name":lncel_name}]
                else:
                    conflicted_cell_site[lncel].append({"mrbts":cell_mrbts,"name":lncel_name})
                continue
            cell_data = {
                "lncel":lncel,
                "lncel_name":lncel_name,
                "distname":cell_distname,
                "mrbts":cell_mrbts
            }
            cells_rows.append(cell_data)          
    sites_rows = list(sites_dict.values())   
    #print(cells_rows[:4])
    ingest_sites_to_db(db_config,sites_rows)
    sites_id_mrbts = select_mrbts_site_id(db_config) #add site_id to cells_rows from DB
    for cell in cells_rows:
        mrbts = cell["mrbts"]
        cell["site_id"] = sites_id_mrbts.get(mrbts)
    print(f"{len(conflicted_cell_site)} are conflected cells | {len(duplicate_lncel)} are duplicated with same LNCEL")
    ingest_cells_to_db(db_config,cells_rows)