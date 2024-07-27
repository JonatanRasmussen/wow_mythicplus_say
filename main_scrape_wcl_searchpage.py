from src.scrape_wcl_searchpage import WclZone, WclLogSearch
from src.config.wcl_zone_groups import WclZoneFactory

#%%
if __name__ == "__main__":
    tww_m_plus_s1 = WclZone(WclZoneFactory.ZONE_ID_TWW_MYTHICPLUS_S1)
    scrape_warcraftlogs = WclLogSearch(tww_m_plus_s1)
    scrape_warcraftlogs.search_for_logs()