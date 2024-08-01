import pandas as pd
import re
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import List, Dict, Callable, NamedTuple
from selenium import webdriver

from.scrape_wcl_fightpage import WclFight
from.format_wcl_encounter import FormatWclEncounter
from .config.consts_file_paths import FilePathConsts
from .config.global_configs import GlobalConfigs
from .config.consts_wcl_columns import WclColumnConsts
from src.utils import Utils

class WclEncounter:

    @staticmethod
    def load_fights_df() -> pd.DataFrame:
        csv_path = FilePathConsts.wcl_log_fights_csv_path(GlobalConfigs.WCL_ZONE_ID, "")
        df = Utils.read_pandas_df(csv_path)
        if df.empty:
            print("Error: Pandas dataframe is empty! Run the scrape_wcl_fightpage script first!")
        return df

    @staticmethod
    def read_log_upload_dates() -> List[str]:
        file_path = FilePathConsts.wcl_log_search_table_csv_path(GlobalConfigs.WCL_ZONE_ID, "")
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

            # Check if fight_id is numeric and convert appropriately
            fight_id = row[WclColumnConsts.FIGHT_ID]
            if isinstance(fight_id, float) and fight_id.is_integer():
                fight_id = str(int(fight_id))
            else:
                fight_id = str(fight_id)

            # Create WclFight instance
            fight = WclFight(
                log_guid=str(row[WclColumnConsts.FIGHT_LOG_GUID]),
                fight_id=fight_id,
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
        all_wcl_encounters = []  # type: List[FormatWclEncounter]
        df = WclEncounter.load_fights_df()
        driver = Utils.create_selenium_webdriver()
        logs_sorted_by_upload = WclEncounter.read_log_upload_dates()
        log_counter = 0
        log_count_to_stop_at = GlobalConfigs.WCL_LOG_TO_STOP_AT
        for log_guid in logs_sorted_by_upload:
            if log_counter >= log_count_to_stop_at:
                break
            log_counter += 1
            filtered_df = df[df[WclColumnConsts.FIGHT_LOG_GUID] == log_guid]
            encounters = WclEncounter.create_wcl_fight_instances(filtered_df)
            if not WclEncounter.is_there_something_to_scrape(encounters):
                continue
            print(f"scraping encounters for log {log_guid} ({log_counter} of {log_count_to_stop_at})")
            wcl_encounters = WclEncounter.scrape_all_encounters_in_log(log_guid, encounters, driver)
            all_wcl_encounters.extend(wcl_encounters)
        Utils.quit_selenium_webdriver(driver)
        FormatWclEncounter.write_encounters_to_csv(all_wcl_encounters)

    @staticmethod
    def scrape_all_encounters_in_log(log_guid: str, encounters: List[WclFight], driver: webdriver.Chrome) -> List[FormatWclEncounter]:
        wcl_encounters = []  # type: List[FormatWclEncounter]
        scraped_fight_ids = []  # type: List[str]
        encounters_with_missing_fight_ids = []  # type: List[WclFight]
        counter = 0
        for encounter in encounters:
            counter += 1
            if not encounter.fight_id or encounter.fight_id == "nan":
                encounters_with_missing_fight_ids.append(encounter)
            else:
                if counter > GlobalConfigs.WCL_ENCOUNTER_TO_STOP_AT:
                    break
                scraped_fight_ids.append(encounter.fight_id)
                if GlobalConfigs.SCRAPE_WIPES or encounter.outcome == WclColumnConsts.FIGHT_OUTCOME_KILL:
                    if GlobalConfigs.SCRAPE_SHORT_FIGHTS or encounter.duration_in_sec >= GlobalConfigs.SHORT_FIGHT_THRESHHOLD_IN_SEC:
                        print(f"scraping fight_id={encounter.fight_id} for log {log_guid} (fight {encounter.fight_id})")
                        wcl_encounter = WclEncounter.scrape_encounter(encounter, encounter.fight_id, driver)
                        wcl_encounters.append(wcl_encounter)
        if GlobalConfigs.SCRAPE_MISSING_FIGHT_IDS:
            for i, encounter in enumerate(encounters):
                fight_id = str(i + 1)
                counter += 1
                if fight_id not in scraped_fight_ids:
                    if counter > GlobalConfigs.WCL_ENCOUNTER_TO_STOP_AT:
                        break
                    if GlobalConfigs.SCRAPE_WIPES or encounter.outcome == WclColumnConsts.FIGHT_OUTCOME_KILL:
                        if GlobalConfigs.SCRAPE_SHORT_FIGHTS or encounter.duration_in_sec >= GlobalConfigs.SHORT_FIGHT_THRESHHOLD_IN_SEC:
                            print(f"scraping fight_id={fight_id} for log {log_guid}")
                            wcl_encounter = WclEncounter.scrape_encounter(encounter, fight_id, driver)
                            wcl_encounters.append(wcl_encounter)
        return wcl_encounters


    @staticmethod
    def scrape_encounter(encounter: WclFight, fight_id: str, driver: webdriver.Chrome) -> FormatWclEncounter:
        file_path = FilePathConsts.wcl_log_encounter_webcache_path(encounter.log_guid, fight_id)
        delimiter = "▓"
        concatenated_html = Utils.try_read_file(file_path)
        if len(concatenated_html) == 0 or GlobalConfigs.WCL_ENCOUNTERS_RESCRAPE:
            base_url = f"https://www.warcraftlogs.com/reports/{encounter.log_guid}#fight={fight_id}&translate=true"
            # Scrape raid setup
            setup_url = base_url + "&view=events"
            setup_table_id = [f'DataTables_Table_{i}' for i in range(100)]  #type: List[str]  #Table ID might not always be 0
            untrimmed_setup_html = Utils.scrape_url_but_await_id(setup_url, 20, setup_table_id, driver)
            setup_html = WclEncounter.trim_setup_html(untrimmed_setup_html)

            # Parse out fight info (can re-use existing html)
            fight_info_html = WclEncounter.extract_fight_info(untrimmed_setup_html)

            # Scrape enemy deaths table
            enemy_deaths_url = base_url + "&type=deaths&hostility=1"
            death_table_id = ['deaths-table-0']  #type: List[str]
            untrimmed_enemy_deaths_html = Utils.scrape_url_but_await_id(enemy_deaths_url, 20, death_table_id, driver)
            ignore_source = True
            enemy_deaths_html = WclEncounter.trim_deaths(untrimmed_enemy_deaths_html, ignore_source)

            # Scrape ability casts
            ability_casts_url = base_url + "&type=casts&hostility=1&by=ability"
            ability_table_id = ['main-table-0']  #type: List[str]
            untrimmed_ability_casts_html = Utils.scrape_url_but_await_id(ability_casts_url, 20, ability_table_id, driver)
            ability_casts_html = WclEncounter.extract_ability_casts(untrimmed_ability_casts_html)

            # Scrape ally deaths table
            # THIS CANNOT FOLLOW DIRECTLY AFTER ENEMY DEATHS as both uses the same table id, messing up the page-load-is-finished checker
            ally_deaths_url = base_url + "&type=deaths&hostility=0"
            untrimmed_ally_deaths_html = Utils.scrape_url_but_await_id(ally_deaths_url, 20, death_table_id, driver)
            ignore_source = False
            ally_deaths_html = WclEncounter.trim_deaths(untrimmed_ally_deaths_html, ignore_source)

            # Ensure none is empty
            if not fight_info_html:
                fight_info_html = "empty"
            if not setup_html:
                setup_html = "empty"
            if not enemy_deaths_html:
                enemy_deaths_html = "empty"
            if not ability_casts_html:
                ability_casts_html = "empty"
            if not ally_deaths_html:
                ally_deaths_html = "empty"

            concatenated_html = delimiter.join([
                fight_info_html,
                setup_html,
                enemy_deaths_html,
                ability_casts_html,
                ally_deaths_html
            ])
            Utils.write_file(concatenated_html, file_path)
        else:
            split_html = concatenated_html.split(delimiter)  #type: List[str]
            if len(split_html) != 5:
                print(f"BudoError: {encounter.log_guid}, {fight_id} has unexpected format. Length is {len(concatenated_html)}")
            fight_info_html = split_html[0]
            setup_html = split_html[1]
            enemy_deaths_html = split_html[2]
            ability_casts_html = split_html[3]
            ally_deaths_html = split_html[4]
        return FormatWclEncounter.parse_all(encounter, fight_id, fight_info_html, setup_html, enemy_deaths_html, ability_casts_html, ally_deaths_html)


    @staticmethod
    def is_there_something_to_scrape(fight_list: List[WclFight]) -> bool:
        FilterCriterion = NamedTuple('FilterCriterion', [('condition', Callable[[WclFight], bool]), ('config_flag', bool)])
        criteria = [
            FilterCriterion(
                condition=lambda fight: fight.fight_id and fight.fight_id != "nan",  # type: ignore[arg-type,return-value]
                config_flag=GlobalConfigs.SCRAPE_MISSING_FIGHT_IDS
            ),
            FilterCriterion(
                condition=lambda fight: fight.outcome == WclColumnConsts.FIGHT_OUTCOME_KILL,
                config_flag=GlobalConfigs.SCRAPE_WIPES
            ),
            FilterCriterion(
                condition=lambda fight: fight.duration_in_sec >= GlobalConfigs.SHORT_FIGHT_THRESHHOLD_IN_SEC,
                config_flag=GlobalConfigs.SCRAPE_SHORT_FIGHTS
            ),
            # Add more criteria here as needed
        ]

        return all(
            criterion.config_flag or any(criterion.condition(fight) for fight in fight_list)
            for criterion in criteria
        )


    @staticmethod
    def trim_setup_html(html_content: str) -> str:
        # Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the table
        setup_table_id = [f'DataTables_Table_{i}' for i in range(100)]  #type: List[str]  #Table ID might not always be 0
        for table_id in setup_table_id:
            table = soup.find('table', id=table_id)
            if not table or isinstance(table, NavigableString):
                continue
            # Find all rows with id matching the pattern "event-row-X-0"
            rows: List[Tag] = table.find_all('tr', id=re.compile(r'event-row-(\d+)-0'))

            # Filter rows to keep only those with id up to event-row-50-0
            stop_at_row = 50

            rows = [row for row in rows if int(re.search(r'event-row-(\d+)-0', row['id']).group(1)) <= stop_at_row] # type: ignore[union-attr,arg-type]

            # Filter rows to keep only those containing "engaged" or "Spec ID"
            rows = [row for row in rows if "engaged" in row.text or "Spec ID" in row.text]

            # Convert the processed rows back to HTML
            delimiter = "█"
            processed_html = delimiter.join(str(row) for row in rows)

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
            return processed_html
        print("BudoWarning: Table not found in ")
        return "Table not found"

    @staticmethod
    def extract_fight_info(html: str) -> str:
        div_id = "filter-fight-boss-wrapper"
        pattern = rf'<div id="{div_id}".*?>(.*?)</div>'
        match = re.search(pattern, html, re.DOTALL)

        if not match:
            return ''
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

    @staticmethod
    def extract_ability_casts(html: str) -> str:
        relevant_html = []

        # Combine all patterns into one
        ability_pattern = r'id="ability-(\d+)-\d">([^<]+)</span>'
        npc_pattern = r'<span class="NPC">([^<]+)</span>'
        cast_count_pattern = r'<span style="display:none">\d+\$</span><div class="report-amount-percent">\d+\.\d+%</div>.*?<span class="report-amount-total">(\d+)</span>'
        combined_pattern = ability_pattern+'|'+npc_pattern+'|'+cast_count_pattern

        # Find all matches
        matches = re.finditer(combined_pattern, html, re.DOTALL)

        for match in matches:
            if match.group(1) and match.group(2):  # Ability
                ability_id, ability_name = match.group(1), match.group(2)
                relevant_html.append(f"Ability: {ability_id} - {ability_name}")
            elif match.group(3):  # NPC
                npc_name = match.group(3)
                relevant_html.append(f"NPC: {npc_name}")
            elif match.group(4):  # Cast Count
                cast_count = match.group(4)
                relevant_html.append(f"Cast Count: {cast_count}")

        # Join all elements into one long string
        delimiter = "█"
        result = delimiter.join(relevant_html)

        return result

    @staticmethod
    def old_extract_ability_casts(html: str) -> str:
        relevant_html = []

        # Pattern for abilities
        ability_pattern = r'id="ability-(\d+)-\d">([^<]+)</span>'

        # Pattern for NPCs
        npc_pattern = r'<span class="NPC">([^<]+)</span>'

        # Ability cast count
        cast_count_pattern = r'<span style="display:none">\d+\$</span><div class="report-amount-percent">\d+\.\d+%</div>.*?<span class="report-amount-total">(\d+)</span>'

        # Find all matches for abilities
        ability_matches = re.finditer(ability_pattern, html)
        for match in ability_matches:
            ability_id, ability_name = match.groups()
            relevant_html.append(f"Ability: {ability_id} - {ability_name}")

        # Find all matches for NPCs
        npc_matches = re.finditer(npc_pattern, html)
        for match in npc_matches:
            npc_name = match.group(1)
            relevant_html.append(f"NPC: {npc_name}")

        # Find all matches for cast count
        cast_count_matches = re.finditer(cast_count_pattern, html, re.DOTALL)
        for match in cast_count_matches:
            cast_count = match.group(1)
            relevant_html.append(f"Cast Count: {cast_count}")

        # Join all elements into one long string
        delimiter = "█"
        result = delimiter.join(relevant_html)

        return result

    @staticmethod
    def trim_deaths(untrimmed_html: str, remove_last_three_events: bool) -> str:

        # Create a BeautifulSoup object
        soup = BeautifulSoup(untrimmed_html, 'html.parser')
        table = soup.find('table', id='deaths-table-0')
        if not table:
            print("BudoWarning: Table not found")
            return ""
        trimmed_html = str(table)

        # Regular expression pattern to match the start and end of the target sections
        if remove_last_three_events:
            pattern = r'</td><td class="tooltip" id="last-three-events-\d+-0">.*?</td>'

            # Use re.sub to replace the matched sections with an empty string
            trimmed_html = re.sub(pattern, '</td>', trimmed_html, flags=re.DOTALL)

        return trimmed_html

    @staticmethod
    def extract_deaths(html_string: str) -> pd.DataFrame:
        # Parse the HTML
        soup = BeautifulSoup(html_string, 'html.parser')

        # Find the table
        table = soup.find('table', {'id': 'deaths-table-0'})

        # Extract headers
        headers = [th.text.strip() for th in table.find_all('th')] # type: ignore[union-attr,arg-type]

        # Extract rows
        rows = [] # Skip the header row
        for tr in table.find_all('tr')[1:]:  # type: ignore[union-attr,arg-type]
            row = [td.text.strip() for td in tr.find_all('td')]
            rows.append(row)

        # Create DataFrame
        df = pd.DataFrame(rows, columns=headers)

        # Replace multiple newlines with '|' in 'Last Three Hits' column
        df['Last Three Hits'] = df['Last Three Hits'].str.replace(r'\n{2,}', '|', regex=True)

        # Print the first few rows
        print(df.head())
        return df

    @staticmethod
    def extract_deaths_as_dct(html_string: str) -> Dict[str,str]:
        df = WclEncounter.extract_deaths(html_string)
        return dict(zip(df['Name'], df['Time']))