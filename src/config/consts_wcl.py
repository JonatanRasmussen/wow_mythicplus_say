import os
from dataclasses import dataclass
from .consts_file_paths import FilePathConsts
from .global_configs import GlobalConfigs
from .wcl_zone_groups import WclZoneFactory

@dataclass
class WclFight:
    log_guid: str
    fight_id: str
    outcome: str
    duration: str
    duration_in_sec: int
    wcl_boss_id: str
    boss_text: str
    zone_name: str
    boss_level: str
    affix_icon: str
    fight_time: str


@dataclass
class WclDeath:
    name_of_player: str
    killing_blow_name: str
    killing_blow_id: str
    over: str
    last_three_hits: str
    hit_1_name: str
    hit_1_id: str
    hit_2_name: str
    hit_2_id: str
    hit_3_name: str
    hit_3_id: str
    damage_taken: str
    healing_received: str

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
    SCRAPE_SHORT_FIGHTS = GlobalConfigs.SCRAPE_SHORT_FIGHTS
    SHORT_FIGHT_THRESHOLD = GlobalConfigs.SHORT_FIGHT_THRESHHOLD_IN_SEC
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
    def wcl_log_encounter_webcache_path(log_guid: str, fight_id: str) -> str:
        file_name = f"log_encounter_{log_guid}_{fight_id}.txt"
        return os.path.join(FilePathConsts.CACHED_HTML_WCL_ENCOUNTER, file_name)

    @staticmethod
    def wcl_log_encounter_csv_path(wcl_zone_id: str, wcl_boss_id: str) -> str:
        file_name = f"log_encounter_{wcl_zone_id}_{wcl_boss_id}.csv"
        if not wcl_boss_id:
            file_name = f"log_encounter_{wcl_zone_id}.csv"
        return os.path.join(FilePathConsts.DATA_RAW_WCL_ENCOUNTER, file_name)
