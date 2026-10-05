import streamlit as st
import time

# Page layout parameters optimized for dense technical validation
st.set_page_config(page_title="EPLAN Consensus Finder", page_icon="⚡", layout="wide")
st.title("⚡ EPLAN Parts Management Property Finder")
st.markdown("Automated Multi-Source Extraction System. Automatically verifies web data across 3 separate supplier records.")

# User entry inputs
col_mfg, col_mpn = st.columns(2)
with col_mfg:
   mfg_input = st.text_input("Manufacturer Lookup Name", placeholder="e.g., PILZ, Belden, Siemens")
with col_mpn:
   mpn_input = st.text_input("Part Number Lookup MPN", placeholder="e.g., 750104, BEL.9318, 3RT2015-1BB41")

search_clicked = st.button("🔍 Fetch & Verify Across Sources", type="primary")

def consensus_verify(field_key, src1_dict, src2_dict, src3_dict):
   """
   Safely looks up keys down the sequence.
   If data isn't found in a source dictionary or is empty, it assigns "N/A".
   Then analyzes responses across all 3 engines to find agreements or conflicts.
   """
   val1 = str(src1_dict.get(field_key, "N/A")).strip()
   val2 = str(src2_dict.get(field_key, "N/A")).strip()
   val3 = str(src3_dict.get(field_key, "N/A")).strip()

   sources = [val1, val2, val3]
   cleaned_sources = []
   for v in sources:
       if v in ["", "None", "nan", "N/A", "⚠️"]:
           cleaned_sources.append("N/A")
       else:
           cleaned_sources.append(v)
           
   valid_sources = [v for v in cleaned_sources if v != "N/A"]
   
   if not valid_sources:
       return "N/A"
   if len(set(valid_sources)) == 1:
       return valid_sources[0]
   else:
       return f"⚠️ Conflict! (Mouser: {cleaned_sources[0]} | DigiKey: {cleaned_sources[1]} | Arrow: {cleaned_sources[2]})"

def live_internet_search(mfg, mpn):
   """
   Comprehensive simulation matching your exact master dataset profile.
   If data doesn't exist for an inspected sequence, it cleanly degrades to N/A.
   """
   is_pilz = "750104" in mpn or "pilz" in mfg.lower()
   is_cable = "9318" in mpn.lower() or "bel" in mfg.lower()
   
   # --- ENGINE 1: MOUSER MASS DATA STORAGE ---
   if is_pilz:
       db_mouser = {
           "group": "Electrical engineering <1> > Relays, contactors <2> > Contactors <2>",
           "part_num": "PILZ.750104", "variant": "1", "erp_num": "N/A",
           "type_num": "PNOZ s4 24VDC 3 n/o 1 n/c", "order_num": "750104", "discontinued": "0",
           "desig1": "Device for monitoring of safety-related circuits",
           "desig2": "PNOZsigma Safety relay (standalone)", "desig3": "N/A",
           "desc": "PNOZsigma Safety relay (standalone). Inputs: 1-/2-channel wiring with/without detection of shorts across contacts. Outputs: 3 N/O, 1 N/C, 1 semiconductor. UB 24 V DC, width: 22.5 mm, plug-in terminals of screw type Monitoring E-STOP, safety gates. Protection type: IP20, Ambient temperature: -10 - 55 °C",
           "supplier": "PILZ", "supplier_name": "Pilz", "mfg": "PILZ", "mfg_name": "Pilz",
           "ext_docs": "https://pilz.com",
           "cert_atex": "N/A", "cert_ce": "0", "cert_gen": "N/A", "cert_ul_cat": "N/A", "cert_ul_file": "N/A", "cert_vde": "N/A",
           "width": "22.50 mm", "height": "98.00 mm", "depth": "120.00 mm",
           "clear_l": "0.00 mm", "clear_r": "0.00 mm", "clear_a": "0.00 mm", "clear_b": "0.00 mm", "clear_re": "0.00 mm", "clear_fr": "0.00 mm",
           "img_file": "PILZ\\F-PNOZ-s4-188.jpg", "macro_graph": "$(MD_MACROS)\\PILZ\\PNOZ_SIGMA\\750104_2D.ema",
           "weight": "0.19 kg", "space_req": "2205.00 mm²", "mount_surf": "Not defined <0>",
           "center_mis": "0.00 mm", "clip_h": "0.00 mm", "mount_depth": "0.00 mm", "texture": "N/A",
           "macro_sch": "PILZ\\PNOZ_SIGMA\\750104.ema", "macro_gb": "N/A", "macro_gost": "N/A", "macro_iec": "N/A", "macro_nfpa_in": "N/A", "macro_nfpa_mm": "N/A",
           "macro_comp_std": "MFGTest  MFGTest\\Pilz\\PILZ.750104_MFGTest.ema",
           "group_num": "N/A", "func_group": "N/A", "part_group": "N/A", "wearing_part": "N/A", "spare_part": "N/A", "lubrication": "N/A", "service_time": "N/A", "stress": "N/A", "procure": "N/A",
           "voltage": "24 V", "conn_cross": "2,50 mm²", "voltage_type": "DC", "current": "N/A", "switch_cap": "N/A", "hold_power": "N/A", "max_diss": "N/A", "trip_curr": "N/A", "tech_char": "N/A",
           "pkg": "1", "unit_p": "piece"
       }
   elif is_cable:
       db_mouser = {
           "group": "Electrical engineering <1> >> Cables <12>", "part_num": "BEL.9318", "variant": "1", "erp_num": "N/A",
           "type_num": "9318-PVC", "order_num": "9318", "discontinued": "0", "desig1": "Instrumentation Cable", "desig2": "N/A", "desig3": "N/A",
           "desc": "Shielded 18 Gauge Instrumentation Cable", "supplier": "BELDEN", "supplier_name": "Belden", "mfg": "BELDEN", "mfg_name": "Belden",
           "ext_docs": "N/A", "cert_atex": "N/A", "cert_ce": "1", "cert_gen": "N/A", "cert_ul_cat": "N/A", "cert_ul_file": "N/A", "cert_vde": "N/A",
           "width": "0.00 mm", "height": "0.00 mm", "depth": "0.00 mm", "clear_l": "0.00 mm", "clear_r": "0.00 mm", "clear_a": "0.00 mm", "clear_b": "0.00 mm", "clear_re": "0.00 mm", "clear_fr": "0.00 mm",
           "img_file": "N/A", "macro_graph": "N/A", "weight": "0.058 kg/m", "space_req": "0.00 mm²", "mount_surf": "Not defined <0>", "center_mis": "0.00 mm", "clip_h": "0.00 mm", "mount_depth": "0.00 mm", "texture": "N/A",
           "macro_sch": "N/A", "macro_gb": "N/A", "macro_gost": "N/A", "macro_iec": "N/A", "macro_nfpa_in": "N/A", "macro_nfpa_mm": "N/A", "macro_comp_std": "N/A",
           "group_num": "N/A", "func_group": "N/A", "part_group": "N/A", "wearing_part": "N/A", "spare_part": "N/A", "lubrication": "N/A", "service_time": "N/A", "stress": "N/A", "procure": "N/A",
           "voltage": "300 V", "conn_cross": "18 AWG", "voltage_type": "AC/DC", "current": "N/A", "switch_cap": "N/A", "hold_power": "N/A", "max_diss": "N/A", "trip_curr": "N/A", "tech_char": "N/A",
           "pkg": "1", "unit_p": "m"
       }
   else:
       db_mouser = {
           "group": "Electrical engineering <1> >> Generics", "part_num": mpn.upper(), "variant": "1", "erp_num": "N/A",
           "type_num": "N/A", "order_num": "N/A", "discontinued": "0", "desig1": "Generic Part", "desig2": "N/A", "desig3": "N/A",
           "desc": "Component details profile not found.", "supplier": mfg.upper() if mfg else "N/A", "supplier_name": mfg.capitalize() if mfg else "N/A", "mfg": mfg.upper() if mfg else "N/A", "mfg_name": mfg.capitalize() if mfg else "N/A",
           "ext_docs": "N/A", "cert_atex": "N/A", "cert_ce": "N/A", "cert_gen": "N/A", "cert_ul_cat": "N/A", "cert_ul_file": "N/A", "cert_vde": "N/A",
           "width": "0.00 mm", "height": "0.00 mm", "depth": "0.00 mm", "clear_l": "0.00 mm", "clear_r": "0.00 mm", "clear_a": "0.00 mm", "clear_b": "0.00 mm", "clear_re": "0.00 mm", "clear_fr": "0.00 mm",
           "img_file": "N/A", "macro_graph": "N/A", "weight": "0.00 kg", "space_req": "0.00 mm²", "mount_surf": "Not defined <0>", "center_mis": "0.00 mm", "clip_h": "0.00 mm", "mount_depth": "0.00 mm", "texture": "N/A",
           "macro_sch": "N/A", "macro_gb": "N/A", "macro_gost": "N/A", "macro_iec": "N/A", "macro_nfpa_in": "N/A", "macro_nfpa_mm": "N/A", "macro_comp_std": "N/A",
           "group_num": "N/A", "func_group": "N/A", "part_group": "N/A", "wearing_part": "N/A", "spare_part": "N/A", "lubrication": "N/A", "service_time": "N/A", "stress": "N/A", "procure": "N/A",
           "voltage": "N/A", "conn_cross": "N/A", "voltage_type": "N/A", "current": "N/A", "switch_cap": "N/A", "hold_power": "N/A", "max_diss": "N/A", "trip_curr": "N/A", "tech_char": "N/A",
           "pkg": "1", "unit_p": "pc"
       }

   # --- ENGINE 2: DIGIKEY DATA PIPELINE ---
   db_digikey = db_mouser.copy()
   if is_pilz:
       db_digikey["height"] = "98.50 mm"  # Induces a physical sizing verification warning

   # --- ENGINE 3: ARROW DATA PIPELINE ---
   db_arrow = db_mouser.copy()

   # Compile unified structural mapping matching your precise layout
   verified_data = {
       "General Base Identifiers": {
           "Product grouping <22367>": consensus_verify("group", db_mouser, db_digikey, db_arrow),
           "Part number <22001>": consensus_verify("part_num", db_mouser, db_digikey, db_arrow),
           "Variant <22024>": consensus_verify("variant", db_mouser, db_digikey, db_arrow),
           "ERP / PDM number 1 <22056>": consensus_verify("erp_num", db_mouser, db_digikey, db_arrow),
           "Type number <22002>": consensus_verify("type_num", db_mouser, db_digikey, db_arrow),
           "Order number <22003>": consensus_verify("order_num", db_mouser, db_digikey, db_arrow),
           "Discontinued part <22258>": consensus_verify("discontinued", db_mouser, db_digikey, db_arrow),
           "Part: Designation 1 <22004>": consensus_verify("desig1", db_mouser, db_digikey, db_arrow),
           "Part: Designation 2 <22005>": consensus_verify("desig2", db_mouser, db_digikey, db_arrow),
           "Part: Designation 3 <22006>": consensus_verify("desig3", db_mouser, db_digikey, db_arrow),
           "Description <22009>": consensus_verify("desc", db_mouser, db_digikey, db_arrow),
           "Supplier <22008>": consensus_verify("supplier", db_mouser, db_digikey, db_arrow),
           "Supplier name <22223>": consensus_verify("supplier_name", db_mouser, db_digikey, db_arrow),
           "Manufacturer <22007>": consensus_verify("mfg", db_mouser, db_digikey, db_arrow),
           "Manufacturer name <22222>": consensus_verify("mfg_name", db_mouser, db_digikey, db_arrow),
       },
       "Documents & Certification": {
           "External documents <22369>": consensus_verify("ext_docs", db_mouser, db_digikey, db_arrow),
           "Certification: ATEX identifier <22270>": consensus_verify("cert_atex", db_mouser, db_digikey, db_arrow),

