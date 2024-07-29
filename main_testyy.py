from src.scrape_wcl_encounter import WclEncounter
from src.utils import Utils

#%%
if __name__ == "__main__":
    log_guid = "hA3zJr19qwgFaQDN"
    fight_id = "last"
    driver = Utils.create_selenium_webdriver()
    base_url = f"https://www.warcraftlogs.com/reports/{log_guid}#fight={fight_id}&translate=true"
    setup_url = base_url + "&view=events"
    untrimmed_setup_html = Utils.scrape_url_with_selenium(setup_url, 10, driver)
    html = WclEncounter.trim_setup_html(untrimmed_setup_html)
    Utils.write_file(html, "test_html5.txt")


