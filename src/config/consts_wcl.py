import os
from .consts_file_paths import FilePathConsts
from .global_configs import GlobalConfigs
from .wcl_zone_groups import WclZoneFactory

class WclConsts:

    ZONE_ID = GlobalConfigs.WCL_ZONE_ID

    # Scrape limit
    SEARCHPAGE_TO_STOP_AT = GlobalConfigs.WCL_SEARCHPAGE_TO_STOP_AT
    FIGHTPAGE_TO_STOP_AT = GlobalConfigs.WCL_FIGHTPAGE_TO_STOP_AT
    LOG_TO_STOP_AT = GlobalConfigs.WCL_LOG_TO_STOP_AT
    ENCOUNTER_TO_STOP_AT = GlobalConfigs.WCL_ENCOUNTER_TO_STOP_AT

    # Feature flags
    SCRAPE_WIPES = GlobalConfigs.SCRAPE_WIPES
    SCRAPE_MISSING_FIGHT_IDS = GlobalConfigs.SCRAPE_MISSING_FIGHT_IDS
    RESCRAPE_SEARCHPAGES = GlobalConfigs.WCL_SEARCHPAGES_RESCRAPE
    RESCRAPE_FIGHTPAGES = GlobalConfigs.WCL_FIGHTPAGES_RESCRAPE
    RESCRAPE_ENCOUNTERS = GlobalConfigs.WCL_ENCOUNTERS_RESCRAPE


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
    def wcl_log_encounter_setup_webcache_path(log_guid: str) -> str:
        file_name = f"log_encounter_setup_{log_guid}.txt"
        return os.path.join(FilePathConsts.CACHED_HTML_WCL_ENCOUNTER_SETUP, file_name)

    @staticmethod
    def wcl_log_encounter_csv_path(wcl_zone_id: str, wcl_boss_id: str) -> str:
        file_name = f"log_encounter_{wcl_zone_id}_{wcl_boss_id}.csv"
        if not wcl_boss_id:
            file_name = f"log_encounter_{wcl_zone_id}.csv"
        return os.path.join(FilePathConsts.DATA_RAW_WCL_ENCOUNTER, file_name)
