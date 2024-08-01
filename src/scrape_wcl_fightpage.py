import pandas as pd
import re
from bs4 import BeautifulSoup
from typing import List, Dict

from .config.global_configs import GlobalConfigs
from .config.class_wcl_fight import WclFight
from .config.consts_file_paths import FilePathConsts
from .config.consts_wcl_columns import WclColumnConsts
from .config.wcl_zone_groups import WclZoneFactory
from src.utils import Utils


class WclFightpage:

    @staticmethod
    def quick_test_ignore_this() -> None:
        untrimmed_html_content = WclFightpage.read_html_file('test_html3.txt')
        html_content = WclFightpage.remove_unnecessary_html(untrimmed_html_content)
        log_guid = "123"
        fight_data = WclFightpage.parse_fight_data(html_content, log_guid)

        # Output the extracted data
        print("Boss Data:")
        for data in fight_data:
            print(data)

    @staticmethod
    def scrape_fightpages():
        wcl_boss_id = ""  # This means 'All bosses'
        log_guids = WclFightpage.read_log_guids(GlobalConfigs.WCL_ZONE_ID, wcl_boss_id)
        WclFightpage.scrape_fightpage(log_guids)


    @staticmethod
    def read_log_guids(wcl_zone_id: str, wcl_boss_id: str) -> List[str]:
        file_path = FilePathConsts.wcl_log_search_table_csv_path(wcl_zone_id, wcl_boss_id)
        df = pd.read_csv(file_path)
        log_guids = []
        for _, row in df.iterrows():
            guid = row[WclColumnConsts.SEARCHPAGE_GUID]
            log_guids.append(guid)
        return log_guids

    @staticmethod
    def scrape_fightpage(log_guids: List[str]) -> None:
        fights = []  #type: List[WclFight]
        driver = Utils.create_selenium_webdriver()
        try:
            counter = 0
            for log_guid in log_guids:
                counter += 1
                if counter > GlobalConfigs.WCL_FIGHTPAGE_TO_STOP_AT:
                    break
                print(f"scraping log {log_guid} ({counter} of {GlobalConfigs.WCL_FIGHTPAGE_TO_STOP_AT})")

                file_path = FilePathConsts.wcl_log_fights_webcache_path(log_guid)
                trimmed_html_content = Utils.try_read_file(file_path)
                if len(trimmed_html_content) == 0 or GlobalConfigs.WCL_FIGHTPAGES_RESCRAPE:
                    # Webscrape log instead of using the locally cached version
                    url = f"https://www.warcraftlogs.com/reports/{log_guid}#translate=true"
                    scraped_html = Utils.scrape_url_with_selenium(url, 10, driver)
                    if scraped_html:
                        trimmed_html_content = WclFightpage.remove_unnecessary_html(scraped_html)
                    else:
                        trimmed_html_content = ""
                    Utils.write_file(trimmed_html_content, file_path)
                fight_data = WclFightpage.parse_fight_data(trimmed_html_content, log_guid)
                for fight in fight_data:
                    fights.append(fight)
        finally:
            Utils.quit_selenium_webdriver(driver)
        WclFightpage.save_fight_data_csv(fights)

    @staticmethod
    def read_html_file(file_path: str) -> str:
        """Reads HTML content from a file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
            return html_content

    @staticmethod
    def get_log_guids(wcl_zone_id: str, wcl_boss_id: str) -> List[str]:
        csv_path = FilePathConsts.wcl_log_search_table_csv_path(wcl_zone_id, wcl_boss_id)
        df = Utils.read_pandas_df(csv_path)
        if not df.empty:
            return df[WclColumnConsts.SEARCHPAGE_GUID].tolist()
        return []

    @staticmethod
    def save_fight_data_csv(fight_data: List[WclFight]) -> None:
        wcl_boss_ids = {}  #type: Dict[str, List[WclFight]]
        all_fights = []  # List to store all fights

        # Iterate over each fight in fight_data and gather a list of each wcl_boss_id
        for fight in fight_data:
            if GlobalConfigs.WCL_ZONE_ID == WclZoneFactory.get_zone_id_from_boss_id(fight.wcl_boss_id):
                if fight.wcl_boss_id not in wcl_boss_ids:
                    wcl_boss_ids[fight.wcl_boss_id] = []
                wcl_boss_ids[fight.wcl_boss_id].append(fight)
                all_fights.append(fight)  # Add fight to all_fights list

        # Create pandas DataFrames for each wcl_boss_id
        for wcl_boss_id, fights in wcl_boss_ids.items():
            fight_dicts = [fight.__dict__ for fight in fights]
            df = pd.DataFrame(fight_dicts)
            path = FilePathConsts.wcl_log_fights_csv_path(GlobalConfigs.WCL_ZONE_ID, wcl_boss_id)
            Utils.write_pandas_df(df, path)
            print(f"Fights CSV saved at {path}")

        # Create pandas DataFrame for all fights
        all_fight_dicts = [fight.__dict__ for fight in all_fights]
        all_df = pd.DataFrame(all_fight_dicts)
        all_path = FilePathConsts.wcl_log_fights_csv_path(GlobalConfigs.WCL_ZONE_ID, "")
        Utils.write_pandas_df(all_df, all_path)
        print(f"All fights CSV saved at {all_path}")

    @staticmethod
    def parse_fight_data(html_content: str, log_guid: str) -> List[WclFight]:
        """Parses HTML content to extract fight data."""
        soup = BeautifulSoup(html_content, 'html.parser')
        boss_boxes = soup.find_all('div', class_='report-overview-boss-box')
        fight_data: List[WclFight] = []

        for box in boss_boxes:
            boss_caption = box.find('a', class_='report-overview-boss-caption')
            if not boss_caption:
                continue

            wcl_boss_id = ''
            boss_text = ''
            zone_name = ''

            boss_icon = boss_caption.find('img', class_='fight-selection-boss-icon')
            wcl_url_icon = WclFightpage.extract_wcl_boss_id_from_icon_url(boss_icon['src'] if boss_icon else '')
            wcl_boss_id = WclZoneFactory.convert_icon_url_to_boss_id(wcl_url_icon)

            boss_text_span = boss_caption.find('span', class_='report-overview-boss-text')
            boss_text = boss_text_span.text.strip() if boss_text_span else ''

            zone_name_span = boss_caption.find('span', class_='report-overview-zone-name')
            zone_name = zone_name_span.text.strip() if zone_name_span else ''

            fight_entries = box.find_all('a', class_='wipes-entry')

            if fight_entries:
                for entry in fight_entries:
                    fight = WclFightpage.parse_fight_entry(entry, log_guid, wcl_boss_id, boss_text, zone_name)
                    fight_data.append(fight)
            else:
                # If no fight entries, parse the boss data directly
                fight = WclFightpage.parse_boss_data_entry(boss_caption, log_guid, wcl_boss_id, boss_text, zone_name)
                fight_data.append(fight)

        return fight_data

    @staticmethod
    def parse_fight_entry(entry, log_guid, wcl_boss_id, boss_text, zone_name) -> WclFight:
        fight_id = ''
        outcome = ''
        duration = ''
        duration_in_sec = 0
        boss_level = ''
        affix_icon = ''
        fight_time = ''

        # Extract ID
        class_name = entry.get('class', [])
        id_match = re.search(r'fight-grid-cell-(\d+)-', ' '.join(class_name))
        if id_match:
            fight_id = id_match.group(1)

        # Extract outcome
        if 'kill' in class_name:
            outcome = WclColumnConsts.FIGHT_OUTCOME_KILL
        elif 'wipe' in class_name:
            outcome = WclColumnConsts.FIGHT_OUTCOME_WIPE

        # Extract duration
        duration_span = entry.find('span', class_='fight-grid-duration')
        if duration_span:
            duration = duration_span.text.strip('()').strip()
            duration = duration.rstrip(')')
            duration_in_sec = int(WclFightpage.convert_duration_to_seconds(duration))

        # Extract fight time
        fight_time_span = entry.find('span', class_='fight-grid-time')
        if fight_time_span:
            fight_time = fight_time_span.text.strip()

        return WclFight(
            log_guid=log_guid,
            fight_id=fight_id,
            outcome=outcome,
            duration=duration,
            duration_in_sec=duration_in_sec,
            wcl_boss_id=wcl_boss_id,
            boss_text=boss_text,
            zone_name=zone_name,
            boss_level=boss_level,
            affix_icon=affix_icon,
            fight_time=fight_time
        )

    @staticmethod
    def parse_boss_data_entry(boss_caption, log_guid, wcl_boss_id, boss_text, zone_name) -> WclFight:
        fight_id = ''
        outcome = ''
        duration = ''
        duration_in_sec = 0
        boss_level = ''
        affix_icon = ''
        fight_time = ''

        boss_kill = boss_caption.find('span', class_='report-overview-boss-kill')
        if boss_kill:
            kill_span = boss_kill.find('span', class_='kill')
            wipe_span = boss_kill.find('span', class_='wipe')
            if kill_span:
                outcome = WclColumnConsts.FIGHT_OUTCOME_KILL
                span = kill_span
            elif wipe_span:
                outcome = WclColumnConsts.FIGHT_OUTCOME_WIPE
                span = wipe_span
            else:
                span = None

            if span:
                text = span.text.strip().split()
                boss_level = text[1] if len(text) > 1 else ''

                affix_icon_img = span.find('img', class_='affix-icon')
                affix_icon = affix_icon_img['title'] if affix_icon_img else ''

                fight_duration = span.find('span', class_='fight-duration')
                if fight_duration:
                    duration = fight_duration.text.strip('()').strip()
                    duration = duration.rstrip(')')
                    duration_in_sec = int(WclFightpage.convert_duration_to_seconds(duration))

                fight_time_span = span.find('span', class_='fight-time')
                fight_time = fight_time_span.text.strip() if fight_time_span else ''

        return WclFight(
            log_guid=log_guid,
            fight_id=fight_id,
            outcome=outcome,
            duration=duration,
            duration_in_sec=duration_in_sec,
            wcl_boss_id=wcl_boss_id,
            boss_text=boss_text,
            zone_name=zone_name,
            boss_level=boss_level,
            affix_icon=affix_icon,
            fight_time=fight_time
        )

    @staticmethod
    def remove_unnecessary_html(html: str) -> str:
        start = 'id="report-top-bar"'
        start_pos = html.find(start)
        if start_pos == -1:
            return html

        end = 'id="report-view-contents"'
        end_pos = html.find(end, start_pos)
        if end_pos == -1:
            return html

        start_pos += len(start)
        return html[start_pos:end_pos]

    @staticmethod
    def extract_wcl_boss_id_from_icon_url(url: str) -> str:
        # Extract '42069' from 'https://assets.rpglogs.com/img/warcraft/bosses/42069-icon.jpg'
        pattern = r'/(\d+)-icon\.jpg$'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return "0"

    @staticmethod
    def convert_duration_to_seconds(duration: str) -> str:
        """Converts duration string to seconds."""
        if not duration:
            return ''

        # Remove parentheses
        duration = duration.strip('()')

        # Split the duration into hours, minutes, and seconds
        parts = duration.split(':')

        if len(parts) == 3:  # HH:MM:SS
            hours, minutes, seconds = map(int, parts)
            total_seconds = hours * 3600 + minutes * 60 + seconds
        elif len(parts) == 2:  # MM:SS
            minutes, seconds = map(int, parts)
            total_seconds = minutes * 60 + seconds
        else:
            return ''  # Invalid format

        return str(total_seconds)


if __name__ == "__main__":
    WclFightpage.quick_test_ignore_this()