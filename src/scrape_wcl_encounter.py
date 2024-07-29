import pandas as pd
import re
import csv
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import List, Dict
from dataclasses import dataclass
from selenium import webdriver

from.scrape_wcl_fightpage import WclFight
from .config.consts_wcl import WclConsts
from .config.consts_wcl_columns import WclColumnConsts
from .config.wcl_zone_groups import WclZoneFactory
from src.utils import Utils

@dataclass
class WclStartOfLog:
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

class WclEncounter:

    @staticmethod
    def load_fights_df() -> pd.DataFrame:
        csv_path = WclConsts.wcl_log_fights_csv_path(WclConsts.ZONE_ID, "")
        df = Utils.read_pandas_df(csv_path)
        if df.empty:
            print("Error: Pandas dataframe is empty! Run the scrape_wcl_fightpage script first!")
        return df

    @staticmethod
    def read_log_upload_dates() -> List[str]:
        file_path = WclConsts.wcl_log_search_table_csv_path(WclConsts.ZONE_ID, "")
        df = pd.read_csv(file_path)
        guid_upload_epoch = {}  #type: Dict[str, int]
        for _, row in df.iterrows():
            guid = row[WclColumnConsts.SEARCHPAGE_GUID]
            upload = int(row[WclColumnConsts.UPLOADED_AS_EPOCH])
            guid_upload_epoch[guid] = upload
        # Create sorted list with newest guids first and oldest guids last
        return sorted(guid_upload_epoch.keys(), key=lambda x: guid_upload_epoch[x], reverse=True)

    @staticmethod
    def create_wcl_fight_instances(df: pd.DataFrame) -> list[WclFight]:
        fight_instances = []
        for _, row in df.iterrows():
            # Convert duration_in_sec to int, handle NaN values
            row_name = WclColumnConsts.FIGHT_DURATION_IN_SEC
            duration_in_sec = int(row[row_name]) if pd.notna(row[row_name]) else 0

            # Create WclFight instance
            fight = WclFight(
                log_guid=str(row[WclColumnConsts.FIGHT_LOG_GUID]),
                fight_id=str(row[WclColumnConsts.FIGHT_ID]),
                outcome=str(row[WclColumnConsts.FIGHT_OUTCOME]),
                duration=str(row[WclColumnConsts.FIGHT_DURATION]),
                duration_in_sec=duration_in_sec,
                wcl_boss_id=str(row[WclColumnConsts.FIGHT_WCL_BOSS_ID]),
                boss_text=str(row[WclColumnConsts.FIGHT_BOSS_TEXT]),
                zone_name=str(row[WclColumnConsts.FIGHT_ZONE_NAME]),
                boss_level=str(row[WclColumnConsts.FIGHT_BOSS_LEVEL]),
                affix_icon=str(row[WclColumnConsts.FIGHT_AFFIX_ICON]),
                fight_time=str(row[WclColumnConsts.FIGHT_TIME])
            )
            fight_instances.append(fight)
        return fight_instances

    @staticmethod
    def scrape_encounters_for_all_logs() -> None:
        df = WclEncounter.load_fights_df()
        logs_sorted_by_upload = WclEncounter.read_log_upload_dates()
        log_counter = 0
        log_count_to_stop_at = WclConsts.LOG_TO_STOP_AT
        for log_guid in logs_sorted_by_upload:
            if log_counter >= log_count_to_stop_at:
                break
            log_counter += 1
            print(f"scraping log {log_guid} ({log_counter} of {log_count_to_stop_at})")
            WclEncounter.scrape_all_encounters_in_log(log_guid, df)

    @staticmethod
    def scrape_all_encounters_in_log(log_guid: str, df: pd.DataFrame) -> None:
        filtered_df = df[df[WclColumnConsts.FIGHT_LOG_GUID] == log_guid]
        encounters = WclEncounter.create_wcl_fight_instances(filtered_df)
        driver = Utils.create_selenium_webdriver()
        scraped_fight_ids = []  # type: List[str]
        encounters_with_missing_fight_ids = []  # type: List[WclFight]
        counter = 0
        for encounter in encounters:
            counter += 1
            if encounter.fight_id == "":
                encounters_with_missing_fight_ids.append(encounter)
            else:
                if counter > WclConsts.ENCOUNTER_TO_STOP_AT:
                    break
                scraped_fight_ids.append(encounter.fight_id)
                print(f"scraping encounter {encounter.fight_id} for {log_guid}")
                WclEncounter.scrape_encounter(encounter, driver)
        if WclConsts.SCRAPE_MISSING_FIGHT_IDS:
            for i, encounter in enumerate(encounters):
                fight_id = str(i + 1)
                counter += 1
                if fight_id not in scraped_fight_ids:
                    if counter > WclConsts.ENCOUNTER_TO_STOP_AT:
                        break
                    print(f"scraping encounter {fight_id} for {log_guid}")
                    WclEncounter.scrape_encounter(encounter, driver)


    @staticmethod
    def scrape_encounter(encounter: WclFight, driver: webdriver.Chrome) -> None:
        is_wipe = encounter.outcome == WclColumnConsts.FIGHT_OUTCOME_WIPE
        if not is_wipe or is_wipe and WclConsts.SCRAPE_WIPES:
            base_url = f"https://www.warcraftlogs.com/reports/{encounter.log_guid}#fight={encounter.fight_id}&translate=true"
            setup_url = base_url + "&view=events"
            untrimmed_setup_html = Utils.scrape_url_with_selenium(setup_url, 10, driver)
            fight_info_html = WclEncounter.extract_fight_info(untrimmed_setup_html)
            setup_html = WclEncounter.trim_setup_html(untrimmed_setup_html)
            print(len(fight_info_html))
            print(len(setup_html))

    @staticmethod
    def trim_setup_html(html_content: str) -> str:
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the table
        table = soup.find('table', id='DataTables_Table_0')

        if not table or isinstance(table, NavigableString):
            return "Table not found"

        # Find all rows with id matching the pattern "event-row-X-0"
        rows: List[Tag] = table.find_all('tr', id=re.compile(r'event-row-(\d+)-0'))

        # Filter rows to keep only those with id up to event-row-50-0
        stop_at_row = 50

        rows = [row for row in rows if int(re.search(r'event-row-(\d+)-0', row['id']).group(1)) <= stop_at_row] # type: ignore[union-attr,arg-type]

        # Filter rows to keep only those containing "engaged" or "Spec ID"
        rows = [row for row in rows if "engaged" in row.text or "Spec ID" in row.text]

        # Convert the processed rows back to HTML
        processed_html = ''.join(str(row) for row in rows)

        print(f"len before: {len(processed_html)}")

        #Remove content between target_start and target_end
        target_start = '<td style="border:none;'
        target_end = '" id="event-row-'

        processed_html = processed_html + target_end  # Fix for remaining rows being filtered out
        while True:
            start_index = processed_html.find(target_start)
            if start_index == -1:
                break
            end_index = processed_html.find(target_end, start_index)
            if end_index == -1:
                break
            processed_html = processed_html[:start_index] + processed_html[end_index:]

        print(f"len after: {len(processed_html)}")

        return processed_html

    @staticmethod
    def extract_fight_info(html: str) -> str:
        div_id = "filter-fight-boss-wrapper"
        pattern = rf'<div id="{div_id}".*?>(.*?)</div>'
        match = re.search(pattern, html, re.DOTALL)

        if not match:
            return ""
        # Find the opening <div> tag
        div_start = html.rfind('<div', 0, match.start())

        # Find the corresponding closing </div> tag
        div_end = match.end()
        open_tags = 1
        while open_tags > 0 and div_end < len(html):
            if html[div_end:].startswith('<div'):
                open_tags += 1
            elif html[div_end:].startswith('</div>'):
                open_tags -= 1
            div_end += 1

        # Extract the full div content
        return html[div_start:div_end].strip()