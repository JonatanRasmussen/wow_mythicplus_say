import pandas as pd
import re
from bs4 import BeautifulSoup
from typing import List

from .config.consts_file_paths import FilePathConsts
from .config.global_configs import GlobalConfigs
from .config.class_wcl_fight import WclFight
from src.utils import Utils

class FormatWclEncounter:

    # Encounter id
    log_guid: str
    encounter_id: str

    # WclFight properties
    fight_id: str
    fight_outcome: str
    fight_duration: str
    fight_duration_in_sec: int
    fight_wcl_boss_id: str
    fight_boss_text: str
    fight_zone_name: str
    fight_boss_level: str
    fight_affix_icon: str
    fight_time: str

    # Encounter info
    encounter_name: str
    encounter_icon: str
    encounter_level: str
    encounter_affixes: str
    encounter_duration: str
    encounter_time: str

    # Encounter setup
    setup_instance_name: str
    setup_instance_id: str
    setup_level: str
    setup_affixes: str
    setup_players: str
    setup_classes: str
    setup_spec_ids: str

    # NPC order
    npc_death_order: str

    # Ability
    ability_list: str

    # Friendly deaths
    ally_deaths: str

    def __init__(self):
        pass

    @classmethod
    def parse_all(cls, fight: WclFight, fight_id: str, fight_info: str, setup: str, enemy_deaths: str, ability_casts: str, ally_deaths: str) -> 'FormatWclEncounter':
        wcl_encounter = FormatWclEncounter()
        wcl_encounter.parse_wcl_fight(fight)
        wcl_encounter.encounter_id = fight_id
        wcl_encounter.parse_fight_info(fight_info)
        wcl_encounter.parse_setup(setup)
        wcl_encounter.parse_enemy_deaths(enemy_deaths)
        wcl_encounter.parse_ability_casts(ability_casts)
        wcl_encounter.parse_ally_deaths(ally_deaths)
        wcl_encounter.print_all_properties()
        return wcl_encounter

    @staticmethod
    def write_encounters_to_csv(encounters: List['FormatWclEncounter']) -> None:
        # Convert the list of dataclass objects to a list of dictionaries
        encounters_dict_list = [encounter.__dict__ for encounter in encounters]
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(encounters_dict_list)
        file_path = FilePathConsts.wcl_log_encounter_csv_path(GlobalConfigs.WCL_ZONE_ID)
        Utils.write_pandas_df(df, file_path)

    def print_all_properties(self) -> None:
        properties = vars(self)
        for prop, value in properties.items():
            print(f"{prop}: {value}")

    def parse_wcl_fight(self, fight: WclFight) -> None:
        self.log_guid = fight.log_guid
        self.fight_id = fight.fight_id
        self.fight_outcome = fight.outcome
        self.fight_duration = fight.duration
        self.fight_duration_in_sec = fight.duration_in_sec
        self.fight_wcl_boss_id = fight.wcl_boss_id
        self.fight_boss_text = fight.boss_text
        self.fight_zone_name = fight.zone_name
        self.fight_boss_level = fight.boss_level
        self.fight_affix_icon = fight.affix_icon
        self.fight_time = fight.fight_time

    def parse_fight_info(self, fight_info_html: str) -> None:
        soup = BeautifulSoup(fight_info_html, 'html.parser')
        # Extract dungeon name
        self.encounter_name = soup.find('div', id='filter-fight-boss-text').text.strip().replace('<span class="sub-arrow">+</span>', '')  # type: ignore[union-attr]
        # Extract dungeon icon URL
        self.encounter_icon = str(soup.find('img', id='filter-fight-boss-icon')['src'])# type: ignore[index]
        # Extract level
        self.encounter_level = soup.find('div', id='filter-fight-details-text').text.split('Level')[1].split()[0]  # type: ignore[union-attr]
        # Extract affixes
        self.encounter_affixes = str([img['title'] for img in soup.find_all('img', class_='affix-icon')])
        # Extract duration
        self.encounter_duration = soup.find('span', class_='fight-duration').text.strip('()') # type: ignore[union-attr]
        # Extract time
        self.encounter_time = soup.find('span', class_='fight-time').text.strip()  # type: ignore[union-attr]

    def parse_setup(self, setup_html):
        soup = BeautifulSoup(setup_html, 'html.parser')

        # Extract encounter information
        first_row = soup.find('tr', class_='odd')
        self.setup_instance_name = first_row.find('span', class_='Boss').text
        self.setup_instance_id = first_row.find('span', class_='estimate').text
        self.setup_level = first_row.find_all('span', class_='estimate')[1].text

        # Extract affixes
        affix_images = first_row.find_all('img', class_='affix-icon')
        self.setup_affixes = str([img['title'] for img in affix_images])

        # Extract player information
        players = []
        classes = []
        spec_ids = []

        # Find all <a> elements with class names corresponding to character classes
        player_links = soup.find_all('a', class_=['DeathKnight', 'DemonHunter', 'Druid', 'Evoker',
                                                  'Hunter', 'Mage', 'Monk', 'Paladin', 'Priest',
                                                  'Rogue', 'Shaman', 'Warlock', 'Warrior'])

        for link in player_links:
            name = link.text.strip()
            class_name = link['class'][0]

            # Find the closest parent <td> and then find the spec ID within it
            parent_td = link.find_parent('td')
            if parent_td:
                spec_id_span = parent_td.find('span', class_='estimate')
                if spec_id_span:
                    spec_id = spec_id_span.text.strip()
                else:
                    spec_id = 'Unknown'
            else:
                spec_id = 'Unknown'

            players.append(name)
            classes.append(class_name)
            spec_ids.append(spec_id)

        self.setup_players = str(players)
        self.setup_classes = str(classes)
        self.setup_spec_ids = str(spec_ids)

    def parse_enemy_deaths(self, enemy_deaths_html: str) -> None:
        soup = BeautifulSoup(enemy_deaths_html, 'html.parser')
        npc_names = []
        seen_names = set()

        rows = soup.find_all('tr', class_=['odd', 'even'])
        for row in rows:
            name_cell = row.find('td', class_='main-table-name')
            if name_cell:
                maybe_null_name = name_cell.find('span', class_='main-table-link NPC')
                if maybe_null_name:
                    full_name = maybe_null_name.text.strip()
                    # Remove the number at the end of the name
                    name = re.sub(r'\s+\d+$', '', full_name)
                    if name not in seen_names:
                        npc_names.append(name)
                        seen_names.add(name)

        self.npc_death_order = str(npc_names)

    def parse_ability_casts(self, ability_casts_html: str) -> None:
        # Split the string into a list
        elements = ability_casts_html.split('█')

        # Remove elements starting with 'NPC: '
        filtered = [e for e in elements if not e.startswith('NPC: ')]

        # Initialize the result list
        result = []

        # Process pairs of Ability and Cast Count
        for i in range(0, len(filtered) - 1, 2):
            if filtered[i].startswith('Ability: ') and filtered[i+1].startswith('Cast Count: '):
                ability_parts = filtered[i].split(' - ')
                if len(ability_parts) == 2:
                    ability_id = ability_parts[0].split(': ')[1]
                    ability_name = ability_parts[1]
                    cast_count = filtered[i+1].split(': ')[1]

                    # Format the string and add to result
                    delimiter = '░'
                    result.append(f"{ability_id}{delimiter}{ability_name}{delimiter}{cast_count}")
            else:
                # If we don't have a matching pair, stop processing
                break

        self.ability_list = str(result)

    def parse_ally_deaths(self, ally_deaths_html: str) -> None:
        soup = BeautifulSoup(ally_deaths_html, 'html.parser')
        rows = soup.find_all('tr', {'class': ['odd', 'even']})

        death_data = []

        for row in rows:
            find_span = row.find('span', class_='main-table-link')
            if not find_span:
                continue
            name_of_player = find_span.text.strip()

            killing_blow_td = row.find_all('td')[2]
            killing_blow_span = killing_blow_td.find('span', class_=re.compile('school-'))
            killing_blow_name = killing_blow_span.text.strip() if killing_blow_span else None
            killing_blow_a = killing_blow_td.find('a')
            killing_blow_id = re.search(r'spell=(\d+)', killing_blow_a['href']).group(1) if killing_blow_a else None  # type: ignore[union-attr]

            over = row.find_all('td', class_='main-table-number')[1].text.strip()

            last_three_hits = row.find('td', class_='tooltip')
            last_three_hits_data = []
            hit_1_name = ""
            hit_1_id = ""
            hit_2_name = ""
            hit_2_id = ""
            hit_3_name = ""
            hit_3_id = ""

            count = 0
            for hit in last_three_hits.find_all('span', style='float:left; margin-right:4px'):
                count += 1
                hit_name = hit.find('span', class_=re.compile('school-')).text.strip()
                hit_id = re.search(r'spell=(\d+)', hit.find('a')['href']).group(1) if hit.find('a') else None # type: ignore[union-attr]
                last_three_hits_data.append((hit_name, hit_id))
                if hit_id:
                    if count == 1:
                        hit_1_name = hit_name
                        hit_1_id = hit_id
                    if count == 2:
                        hit_2_name = hit_name
                        hit_2_id = hit_id
                    if count == 3:
                        hit_3_name = hit_name
                        hit_3_id = hit_id

            damage_taken = row.find('td', class_='main-table-number damage').text.strip()
            healing_received = row.find('td', class_='main-table-number healing').text.strip()

            properties = [
                name_of_player,
                killing_blow_name,
                killing_blow_id,
                over,
                hit_1_name,
                hit_1_id,
                hit_2_name,
                hit_2_id,
                hit_3_name,
                hit_3_id,
                damage_taken,
                healing_received,
            ]
            delimiter = '░'
            serialized_death_data = delimiter.join(str(prop) for prop in properties)
            death_data.append(serialized_death_data)

        self.ally_deaths = str(death_data)
