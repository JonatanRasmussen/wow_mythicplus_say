from .consts_file_paths import FilePathConsts
from .global_configs import GlobalConfigs

class WowheadConsts:

    # PTR version (make sure to update this depending on current PTR version)
    PTR_VERSION = GlobalConfigs.WOWHEAD_PTR_VERSION

    # Paths
    SPELL_ID_CACHE = FilePathConsts.CACHED_HTML_WOWHEAD_SPELL_IDS
    ZONE_ID_CACHE = FilePathConsts.CACHED_HTML_WOWHEAD_ZONE_IDS

    # Wowhead configs feature flags
    RESCRAPE_SPELL_IDS = GlobalConfigs.WOWHEAD_SPELL_IDS_RESCRAPE
    RESCRAPE_ZONE_IDS = GlobalConfigs.WOWHEAD_ZONE_IDS_RESCRAPE
