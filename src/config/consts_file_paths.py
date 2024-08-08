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
    CACHED_HTML_WCL_ENCOUNTER = os.path.join(CACHED_HTML, "wcl_encounter")

    DATA_RAW_WOWHEAD_SPELL_IDS = os.path.join(DATA_RAW, "wowhead_spell_ids")
    DATA_RAW_WCL_SEARCHPAGE = os.path.join(DATA_RAW, "wcl_searchpage")
    DATA_RAW_WCL_FIGHTPAGE= os.path.join(DATA_RAW, "wcl_fights")
    DATA_RAW_WCL_ENCOUNTER= os.path.join(DATA_RAW, "wcl_encounter")

    FINAL_OUTPUT_SPELL_LIST = os.path.join(FINAL_OUTPUT, "spell_list")
    FINAL_OUTPUT_SPREADSHEET = os.path.join(FINAL_OUTPUT, "mythicplus_tww.xlsx")

    @staticmethod
    def wowhead_spell_ids_csv_path(wcl_zone_id: str) -> str:
        file_name = f"wowhead_spell_ids_{wcl_zone_id}.csv"
        return os.path.join(FilePathConsts.DATA_RAW_WOWHEAD_SPELL_IDS, file_name)

    @staticmethod
    def wcl_log_search_table_webcache_path(wcl_zone_id: str, wcl_boss_id: str) -> str:
        file_name = f"log_search_{wcl_zone_id}_{wcl_boss_id}.txt"
        return os.path.join(FilePathConsts.CACHED_HTML_WCL_LOG_SEARCH, file_name)

    @staticmethod
    def wcl_log_search_table_csv_path(wcl_zone_id: str, wcl_boss_id: str) -> str:
        file_name = f"log_search_{wcl_zone_id}_{wcl_boss_id}.csv"
        if not wcl_boss_id:
            file_name = f"log_search_{wcl_zone_id}.csv"
        return os.path.join(FilePathConsts.DATA_RAW_WCL_SEARCHPAGE, file_name)

    @staticmethod
    def wcl_log_fights_webcache_path(log_guid: str) -> str:
        file_name = f"log_fights_{log_guid}.txt"
        return os.path.join(FilePathConsts.CACHED_HTML_WCL_FIGHTS, file_name)

    @staticmethod
    def wcl_log_fights_csv_path(wcl_zone_id: str, wcl_boss_id: str) -> str:
        file_name = f"log_fights_{wcl_zone_id}_{wcl_boss_id}.csv"
        if not wcl_boss_id:
            file_name = f"log_fights_{wcl_zone_id}.csv"
        return os.path.join(FilePathConsts.DATA_RAW_WCL_FIGHTPAGE, file_name)

    @staticmethod
    def wcl_log_encounter_webcache_path(log_guid: str, fight_id: str) -> str:
        file_name = f"log_encounter_{log_guid}_{fight_id}.txt"
        return os.path.join(FilePathConsts.CACHED_HTML_WCL_ENCOUNTER, file_name)

    @staticmethod
    def wcl_log_encounter_csv_path(wcl_zone_id: str) -> str:
        file_name = f"log_encounter_{wcl_zone_id}.csv"
        return os.path.join(FilePathConsts.DATA_RAW_WCL_ENCOUNTER, file_name)

    @staticmethod
    def wcl_spell_list_csv_path(wcl_zone_id: str, wcl_encounter_name: str) -> str:
        file_name = f"log_spell_list_{wcl_zone_id}_{wcl_encounter_name}.csv"
        if not wcl_encounter_name:
            file_name = f"log_spell_list_{wcl_zone_id}.csv"
        return os.path.join(FilePathConsts.FINAL_OUTPUT_SPELL_LIST, file_name)