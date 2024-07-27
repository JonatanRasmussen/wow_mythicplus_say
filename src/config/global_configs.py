import os
from .wcl_zone_groups import WclZoneFactory

class GlobalConfigs:

    # Target data
    WCL_ZONE_ID = WclZoneFactory.ZONE_ID_TWW_MYTHICPLUS_S1

    # External constants
    WOWHEAD_PTR_VERSION = "ptr-2/"

    # Other
    WCL_SEARCHPAGE_TO_STOP_AT = 20
    WCL_LOG_COUNT_TO_STOP_AT = 99999

    # Rescrape everything or use cached html if available
    FORCE_RESCRAPE_ALL = False

    WOWHEAD_SPELL_IDS_RESCRAPE = FORCE_RESCRAPE_ALL
    WOWHEAD_ZONE_IDS_RESCRAPE = FORCE_RESCRAPE_ALL
    WCL_SEARCHPAGES_RESCRAPE = FORCE_RESCRAPE_ALL