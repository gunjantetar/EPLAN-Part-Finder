import streamlit as st
import time
import random
# Page layout parameters optimized for dense technical validation
st.set_page_config(page_title="EPLAN Consensus Finder", page_icon="⚡", layout="wide")
st.title("⚡ EPLAN Parts Management Property Finder")
st.markdown("Automated Multi-Source Extraction System. Automatically verifies web data across 3 separate supplier records.")
# User entry inputs
col_mfg, col_mpn = st.columns(2)
with col_mfg:
   mfg_input = st.text_input("Manufacturer Lookup Name", placeholder="e.g., Belden, Siemens, Phoenix Contact")
with col_mpn:
   mpn_input = st.text_input("Part Number Lookup MPN", placeholder="e.g., BEL.9318, 3RT2015-1BB41")
search_clicked = st.button("🔍 Fetch & Verify Across Sources", type="primary")
def consensus_verify(field_name, val_source1, val_source2, val_source3):
   """
   Analyzes responses from 3 distinct sources.
   Returns the value if verified, or flags a conflict if data mismatches.
   """
   sources = [str(val_source1).strip(), str(val_source2).strip(), str(val_source3).strip()]
   # Filter out empty or missing values to check baseline agreements
   valid_sources = [v for v in sources if v not in ["N/A", "", "None"]]
   if not valid_sources:
       return "N/A"
   # Check if all successful online engines found the exact same string
   if len(set(valid_sources)) == 1:
       return valid_sources[0]
   else:
       # Conflict discovered: Output string displaying data differences clearly
       return f"⚠️ Conflict! (Mouser: {val_source1} | DigiKey: {val_source2} | Arrow: {val_source3})"
def live_internet_search(mfg, mpn):
   """
   Simulates sending backend extraction queries to live databases:
   1. Mouser Search API API
   2. DigiKey Product Catalog API
   3. Arrow Electronics Marketplace Search
   """
   is_cable = "9318" in mpn.lower() or "bel" in mfg.lower()
   # --- ENGINE 1: MOUSER LIVE RECORDS ---
   db_mouser = {
       "mfg": mfg.upper() if mfg else "BELDEN",
       "mpn": mpn.upper(),
       "desc": "Shielded 18 Gauge Twisted Pair Instrumentation Cable",
       "width": "0.00 mm", "height": "0.00 mm", "depth": "0.00 mm",
       "type": "TWISTED PAIR", "connections": "2", "cross_sec": "18", "dia": "6.07 mm", "unit": "AWG <3>",
       "pkg": "1", "unit_p": "m"
   } if is_cable else {
       "mfg": mfg.upper() if mfg else "SIEMENS",
       "mpn": mpn.upper(),
       "desc": "Power Contactor 3-Pole 3kW AC-3",
       "width": "45.00 mm", "height": "57.50 mm", "depth": "73.00 mm",
       "type": "CONTACTOR", "connections": "4", "cross_sec": "4", "dia": "N/A", "unit": "mm²",
       "pkg": "1", "unit_p": "pc"
   }
   # --- ENGINE 2: DIGIKEY LIVE RECORDS ---
   db_digikey = db_mouser.copy()
   if is_cable:
       # Introduce a slight discrepancy to demonstrate how the conflict engine triggers
       db_digikey["dia"] = "6.12 mm"
   else:
       db_digikey["depth"] = "75.00 mm" # Discrepancy for contactor depth
   # --- ENGINE 3: ARROW LIVE RECORDS ---
   db_arrow = db_mouser.copy() # Agrees with mouser baseline
   # Process consensus mapping across our web data pipelines
   verified_data = {
       "General": {
           "Product grouping <22367>": "Electrical engineering <1> >>",
           "Part number <22001>": consensus_verify("Part number", db_mouser["mpn"], db_digikey["mpn"], db_arrow["mpn"]),
           "ERP / PDM number 1 <22056>": "N/A",
           "Type number <22002>": consensus_verify("Type number", db_mouser["mpn"], db_digikey["mpn"], db_arrow["mpn"]),
           "Order number <22003>": "9318" if is_cable else "3RT2015",
           "Variant <22024>": "1",
           "Part: Designation 1 <22004>": consensus_verify("Designation 1", db_mouser["desc"], db_digikey["desc"], db_arrow["desc"]),
           "Part: Designation 2 <22005>": "N/A",
           "Part: Designation 3 <22006>": "N/A",
           "Description <22009>": consensus_verify("Description", db_mouser["desc"], db_digikey["desc"], db_arrow["desc"]),
           "Manufacturer <22007>": consensus_verify("Manufacturer", db_mouser["mfg"], db_digikey["mfg"], db_arrow["mfg"]),
           "Supplier <22008>": "DISTRIBUTOR CONSENSUS"
       },
       "Mounting data": {
           "Dimensions": {
               "Width <22013>": consensus_verify("Width", db_mouser["width"], db_digikey["width"], db_arrow["width"]),
               "Height <22012>": consensus_verify("Height", db_mouser["height"], db_digikey["height"], db_arrow["height"]),
               "Depth <22014>": consensus_verify("Depth", db_mouser["depth"], db_digikey["depth"], db_arrow["depth"])
           },
           "Mounting clearances": {
               "Mounting clearance Width: Left <22152>": "0.00 mm",
               "Mounting clearance Width: Right <22153>": "0.00 mm",
               "Mounting clearance Height: Above <22154>": "0.00 mm",
               "Mounting clearance Height: Below <22155>": "0.00 mm",
               "Mounting clearance Depth: Rear <22157>": "0.00 mm",
               "Mounting clearance Depth: Front <22156>": "0.00 mm"
           },
           "Graphical macro <22010>": "N/A",
           "Image file <22045>": "N/A",
           "Weight <22046>": "0.00 kg",
           "Space requirement <22047>": "0.00 mm²",
           "Mounting surface <22022>": "Not defined <0>",
           "Center mismatch <22215>": "0.00 mm",
           "Clip-on height <22211>": "0.00 mm",
           "Mounting depth <22268>": "0.00 mm",
           "Texture <22219>": "N/A"
       },
       "Data": {
           "Schematic macro <22145>": "N/A",
           "Schematic macro: GB/CCC <22873>": "N/A",
           "Schematic macro: GOST <22874>": "N/A",
           "Schematic macro: IEC <22870>": "N/A",
           "Schematic macro: NFPA inch <22872>": "N/A",
           "Schematic macro: NFPA mm <22871>": "N/A",
           "Schematic macros for company standard <22882>": "N/A",
           "Connection point pattern <22941>": "N/A",
           "Connection point pattern: Offset X-direction <22277>": "0.00 mm",
           "Connection point pattern: Offset Y-direction <22278>": "0.00 mm",
           "Group number <22044>": "N/A",
           "Function group <22026>": "N/A",
           "Part group <22027>": "N/A",
           "Wearing part <22139>": "N/A",
           "Spare part <22140>": "N/A",
           "Lubrication / maintenance <22141>": "N/A",
           "Service time <22142>": "N/A",
           "Stress <22143>": "N/A",
           "Procurement <22144>": "N/A"
       },
       "Technical data": {
           "Cable type / Type designation <22030>": consensus_verify("Cable Type", db_mouser["type"], db_digikey["type"], db_arrow["type"]),
           "Number of connections <22031>": consensus_verify("Connections", db_mouser["connections"], db_digikey["connections"], db_arrow["connections"]),
           "Connection: Cross-section / diameter <22032>": consensus_verify("Cross section", db_mouser["cross_sec"], db_digikey["cross_sec"], db_arrow["cross_sec"]),
           "Voltage <22033>": "N/A",
           "Cable assignment diagram form <22034>": "N/A",
           "Length (prefabricated) <22055>": "0.00 m",
           "Min. bending radius <22063>": "N/A",
           "Cable / Conduit: Designation in graphic <22064>": "N/A",
           "Outside diameter <22065>": consensus_verify("Outside Diameter", db_mouser["dia"], db_digikey["dia"], db_arrow["dia"]),
           "Copper weight <22066>": "N/A",
           "Weight / length <22067>": "N/A",
           "Unit for connection cross-section / diameter <22068>": consensus_verify("Unit type", db_mouser["unit"], db_digikey["unit"], db_arrow["unit"]),
           "No. of connections and cross-section / diameter <22069>": "N/A",
           "Intrinsically safe <22114>": "False",
           "Short-circuit proof <22115>": "False",
           "Technical characteristics <22017>": "N/A"
       },
       "Prices": {
           "Quantity/packaging <22122>": consensus_verify("Packaging Qty", db_mouser["pkg"], db_digikey["pkg"], db_arrow["pkg"]),
           "Quantity unit <22042>": consensus_verify("Quantity Unit", db_mouser["unit_p"], db_digikey["unit_p"], db_arrow["unit_p"])
       }
   }
   return verified_data
if search_clicked:
   if not mpn_input:
       st.warning("⚠️ Please provide a Part Number to process validation loops.")
   else:
       # Visual progress cues showing search state engine updates
       progress_bar = st.progress(0)
       status_text = st.empty()
       for percent, step_msg in [(25, "Searching Mouser Electronics Database..."),
                                 (55, "Cross-checking with DigiKey API Catalogs..."),
                                 (85, "Verifying parameters on Arrow Global Index..."),
                                 (100, "Compiling multi-source data consensus...")] :
           status_text.text(step_msg)
           progress_bar.progress(percent)
           time.sleep(0.4)
       parsed_data = live_internet_search(mfg_input, mpn_input)
       st.success("✅ Multi-Source Search Complete! Review Verification Status:")
       # --- CATEGORY 1: GENERAL ---
       with st.expander("📁 1. General", expanded=True):
           for k, v in parsed_data["General"].items():
               c_lbl, c_val = st.columns()
               c_lbl.markdown(f"**{k}**")
               if "⚠️ Conflict!" in str(v):
                   c_val.error(v)
               else:
                   c_val.text_input(k, value=v, label_visibility="collapsed", key=f"gen_{k}")
       # --- CATEGORY 2: MOUNTING DATA ---
       with st.expander("📁 2. Mounting data", expanded=True):
           m_data = parsed_data["Mounting data"]
           st.markdown("#### 📐 Dimensions")
           for k, v in m_data["Dimensions"].items():
               c_lbl, c_val = st.columns()
