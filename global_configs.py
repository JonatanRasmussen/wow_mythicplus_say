import os

class GlobalConfigs:

    # Wowhead data
    PTR_VERSION = "ptr-2/" # Ensure this matches the url used on wowhead

    # Folders and file names
    EXCEL_SHEET_NAME = "mythicplus_tww.xlsx"
    CACHED_WOWHEAD_PAGES = "wowhead_cache"
    CACHED_WOWHEAD_SPELL_ID_PAGES = os.path.join(CACHED_WOWHEAD_PAGES, "wowhead_spell_ids")
    CACHED_WOWHEAD_ZONE_ID_PAGES = os.path.join(CACHED_WOWHEAD_PAGES, "wowhead_zone_ids")


    ### Webcache and scraped data
    WEBCACHE_FOLDER = "webcache"
    SCRAPED_DATA_FOLDER = "scraped_data"
    # Wowhead and Wcl folders
    WOWHEAD_FOLDER = os.path.join(WEBCACHE_FOLDER, "wowhead")
    WCL_FOLDER = os.path.join(WEBCACHE_FOLDER, "wcl")
    # Wowhead

    # Wcl
    WCL_LOG_SEARCH_CACHE = os.path.join(WCL_FOLDER, "wcl_log_search")
    WCL_LOG_SEARCH_DATA = os.path.join(SCRAPED_DATA_FOLDER, "wcl_log_search")

    # Feature flags
    SAVE_WOWHEAD_SPELL_ID_PAGES_LOCALLY = True
    SAVE_WOWHEAD_ZONE_ID_PAGES_LOCALLY = True
    USE_CACHED_WOWHEAD_SPELL_ID_PAGES = True
    USE_CACHED_WOWHEAD_ZONE_ID_PAGES = True

    USE_CACHED_WARCRAFTLOGS_SEARCH = True

    @staticmethod
    def wcl_log_search_txtfile(wcl_zone_id: str, wcl_boss_id: str) -> str:
        file_name = f"log_search_{wcl_zone_id}_{wcl_boss_id}.txt"
        return os.path.join(GlobalConfigs.WCL_LOG_SEARCH_CACHE, file_name)

    @staticmethod
    def wcl_log_search_csvfile(wcl_zone_id: str, wcl_boss_id: str) -> str:
        file_name = f"log_search_{wcl_zone_id}_{wcl_boss_id}.csv"
        if len(wcl_boss_id) == 0:
            file_name = f"log_search_{wcl_zone_id}.csv"
        return os.path.join(GlobalConfigs.WCL_LOG_SEARCH_DATA, file_name)