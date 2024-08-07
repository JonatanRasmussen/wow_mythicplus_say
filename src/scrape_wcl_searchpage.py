from typing import List

import pandas as pd
from bs4 import BeautifulSoup, NavigableString

from .config.consts_file_paths import FilePathConsts
from .config.global_configs import GlobalConfigs
from .config.consts_wcl_columns import WclColumnConsts
from .config.wcl_zone_groups import WclZoneFactory
from src.utils import Utils

class WowEncounter:
    def __init__(self, wcl_boss_id: str, icon_url: str, name: str, abbreviation: str):
        self.wcl_boss_id = wcl_boss_id
        self.icon_url = wcl_boss_id if (icon_url == "") else icon_url
        self.name = name
        self.abbreviation = abbreviation
        self.serialized_html_table = ""
        self.df = pd.DataFrame()

class WclZone:
    def __init__(self, wcl_zone_id: str):
        zone_data = WclZoneFactory.WCL_ZONES.get(wcl_zone_id)
        if not zone_data:
            raise ValueError(f"Invalid zone ID: {wcl_zone_id}")

        self.wcl_zone_id = wcl_zone_id
        self.name = zone_data[WclZoneFactory.NAME_KEY]
        self.wcl_bosses = []  # type: List[WowEncounter]
        for boss_id, icon_url, name, abbreviation in zone_data[WclZoneFactory.BOSSES_KEY]:
            self.wcl_bosses.append(WowEncounter(boss_id, icon_url, name, abbreviation))

class WclLogSearch:

    def __init__(self, wcl_zone: WclZone):
        self.wcl_zone = wcl_zone
        self.scrape_progress_boss_number = 0
        self.scrape_progress_total_bosses = len(wcl_zone.wcl_bosses)
        self.scrape_progress_searchpage_number = 0

    def merge_csvs(self) -> None:
        bosses = [] #type: List[WowEncounter]
        for wcl_boss in self.wcl_zone.wcl_bosses:
            bosses.append(wcl_boss)

        merged_df = pd.DataFrame()
        log_guids = {}

        row_guid = WclColumnConsts.SEARCHPAGE_GUID
        for i, boss in enumerate(bosses):
            file_path = FilePathConsts.wcl_log_search_table_csv_path(self.wcl_zone.wcl_zone_id, boss.wcl_boss_id)
            df = pd.read_csv(file_path)
            for _, row in df.iterrows():
                guid = row[row_guid]
                if guid not in log_guids:  # If GUID not in combined df, add it
                    log_guids[guid] = [0] * len(bosses)
                    log_guids[guid][i] = 1
                    merged_df = pd.concat([merged_df, pd.DataFrame([row])], ignore_index=True)
                else:  # If GUID already in combined df, update row
                    log_guids[guid][i] = 1

        for i, boss in enumerate(bosses):
            merged_df[boss.abbreviation] = merged_df[row_guid].map(lambda x: log_guids[x][i])

        output_file = file_path = FilePathConsts.wcl_log_search_table_csv_path(self.wcl_zone.wcl_zone_id, "")
        merged_df.to_csv(output_file, index=False)
        print(f"Combined CSV saved as {output_file}")

    @staticmethod
    def html_table_to_pandas_df(html_table: str) -> pd.DataFrame:
        soup = BeautifulSoup(html_table, 'lxml')
        table = soup.find('table', id='reports-table')
        if not table:
            print("BudoError: Could not locate table with id 'reports-table'.")
            return pd.DataFrame()
        if isinstance(table, NavigableString):
            print("BudoError: Table cannot .find_all() due to being a NavigableString")
            return pd.DataFrame()

        headers = [WclColumnConsts.SEARCHPAGE_GUID]
        for th in table.find_all('th'): # Extract header
            url = th.get_text(strip=True)
            log_guid = url.replace("/reports/", "")
            headers.append(log_guid)
        rows = []
        for tr in table.find_all('tr')[1:]: # Extract rows
            cells = tr.find_all('td')
            row = []

            # Extract URL from the first cell (assuming it contains the link)
            url_cell = cells[0].find('a')
            url = url_cell['href'] if url_cell else ''
            log_guid = url.replace("/reports/", "")
            row.append(log_guid)

            # Extract text from all cells
            for cell in cells:
                row.append(cell.get_text(strip=True))
            rows.append(row)

        df = pd.DataFrame(rows, columns=headers)
        return df

    def scrape_search_table(self, wcl_boss: WowEncounter) -> List[str]:
        html_tables = []  # type: List[str]
        driver = Utils.create_selenium_webdriver()
        try:
            page_to_stop_at = GlobalConfigs.WCL_SEARCHPAGE_TO_STOP_AT
            self.scrape_progress_searchpage_number = 0
            for page in range(0, page_to_stop_at):
                self.scrape_progress_searchpage_number += 1
                self.print_scrape_progress()
                url = f"https://www.warcraftlogs.com/zone/reports?zone={self.wcl_zone.wcl_zone_id}&boss={wcl_boss.wcl_boss_id}&page={page+1}"
                scraped_html = Utils.scrape_url_with_selenium(url, 10, driver)
                if scraped_html:
                    table_html = Utils.locate_html_with_bs4(scraped_html, "reports-table")
                    try:
                        _ = WclLogSearch.html_table_to_pandas_df(table_html)
                    except (AssertionError, ValueError): # Trying to parse empty table
                        break # End of search results reached
                    html_tables.append(table_html)
        finally:
            Utils.quit_selenium_webdriver(driver)
        return html_tables

    def fetch_search_table(self, wcl_boss: WowEncounter) -> List[str]:
        file_path = FilePathConsts.wcl_log_search_table_webcache_path(self.wcl_zone.wcl_zone_id, wcl_boss.wcl_boss_id)
        serialized_html_tables = Utils.try_read_file(file_path)
        delimiter = "█"

        if len(serialized_html_tables) != 0 and not GlobalConfigs.WCL_SEARCHPAGES_RESCRAPE:
            return serialized_html_tables.split(delimiter)

        html_tables = self.scrape_search_table(wcl_boss)

        for table in html_tables:
            assert delimiter not in table, f"BudoError: The html contains {delimiter}. Use another character to split list."
        serialized_html_tables = delimiter.join(html_tables)
        Utils.write_file(serialized_html_tables, file_path)
        return html_tables

    def search_for_logs(self) -> None:
        for wcl_boss in self.wcl_zone.wcl_bosses:
            self.scrape_progress_boss_number += 1
            html_tables = self.fetch_search_table(wcl_boss)
            dfs = []
            for table in html_tables:
                df = self.html_table_to_pandas_df(table)
                dfs.append(df)

            wcl_boss.df = pd.concat(dfs, ignore_index=True)

            uploaded = WclColumnConsts.SEARCHPAGE_UPLOADED
            uploaded_epoch = WclColumnConsts.UPLOADED_AS_EPOCH
            uploaded_datetime = WclColumnConsts.UPLOADED_AS_DATETIME
            duration = WclColumnConsts.SEARCHPAGE_DURATION
            duration_epoch = WclColumnConsts.DURATION_AS_EPOCH
            duration_time = WclColumnConsts.DURATION_AS_TIME
            wcl_boss.df[[uploaded_epoch, uploaded_datetime]] = wcl_boss.df[uploaded].str.split('$', expand=True)
            wcl_boss.df[[duration_epoch, duration_time]] = wcl_boss.df[duration].str.split('$', expand=True)
            wcl_boss.df.drop(columns=[uploaded, duration], inplace=True)

            zone_id = self.wcl_zone.wcl_zone_id
            boss_id = wcl_boss.wcl_boss_id
            file_path = FilePathConsts.wcl_log_search_table_csv_path(zone_id, boss_id)
            Utils.write_pandas_df(wcl_boss.df, file_path)
        self.merge_csvs()

    def print_scrape_progress(self):
        print(f"scraping wcl_zone {self.scrape_progress_boss_number} of {self.scrape_progress_total_bosses}: Page {self.scrape_progress_searchpage_number}")