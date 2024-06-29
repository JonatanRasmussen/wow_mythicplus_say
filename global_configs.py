import os

class GlobalConfigs:

    # Wowhead data
    PTR_VERSION = "ptr-2/" # Ensure this matches the url used on wowhead

    # Folders and file names
    EXCEL_SHEET_NAME = "mythicplus_tww.xlsx"
    CACHED_WOWHEAD_PAGES = "wowhead_cache"
    CACHED_WOWHEAD_SPELL_ID_PAGES = os.path.join(CACHED_WOWHEAD_PAGES, "wowhead_spell_ids")
    CACHED_WOWHEAD_ZONE_ID_PAGES = os.path.join(CACHED_WOWHEAD_PAGES, "wowhead_zone_ids")

    # Feature flags
    SAVE_WOWHEAD_SPELL_ID_PAGES_LOCALLY = True
    SAVE_WOWHEAD_ZONE_ID_PAGES_LOCALLY = True
    USE_CACHED_WOWHEAD_SPELL_ID_PAGES = True
    USE_CACHED_WOWHEAD_ZONE_ID_PAGES = True