import os

class FilePathConsts:

    # Top level folders
    CACHED_HTML = "cached_html"
    DATA_RAW = "data_raw"
    FINAL_OUTPUT = "final_output"
    SRC = "src"

    # Subfolder paths
    CACHED_HTML_WOWHEAD_SPELL_IDS = os.path.join(CACHED_HTML, "wowhead_spell_ids")
    CACHED_HTML_WOWHEAD_ZONE_IDS = os.path.join(CACHED_HTML, "wowhead_zone_ids")
    CACHED_HTML_WCL_LOG_SEARCH = os.path.join(CACHED_HTML, "wcl_searchpage")
    CACHED_HTML_WCL_FIGHTS = os.path.join(CACHED_HTML, "wcl_fightpage")
    CACHED_HTML_WCL_ENCOUNTER_SETUP = os.path.join(CACHED_HTML, "wcl_encounter_setup")

    DATA_RAW_WCL_SEARCHPAGE = os.path.join(DATA_RAW, "wcl_searchpage")
    DATA_RAW_WCL_FIGHTPAGE= os.path.join(DATA_RAW, "wcl_fights")
    DATA_RAW_WCL_ENCOUNTER= os.path.join(DATA_RAW, "wcl_encounter")

    FINAL_OUTPUT_SPREADSHEET = os.path.join(FINAL_OUTPUT, "mythicplus_tww.xlsx")