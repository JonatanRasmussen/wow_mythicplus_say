import pandas as pd
import ast
from collections import defaultdict
from typing import List, Dict, DefaultDict, Union

from .config.consts_file_paths import FilePathConsts
from .config.global_configs import GlobalConfigs
from .config.wcl_zone_groups import WclZoneFactory
from src.class_wowhead_spell import WowheadSpell
from src.utils import Utils

class FormatSpelllist:
    @staticmethod
    def main(df_wipes_included: pd.DataFrame) -> None:
        dupe_df = FormatSpelllist.filter_outcomes_that_are_kill(df_wipes_included)
        no_dupe_df = FormatSpelllist.remove_duplicate_logs(dupe_df)
        expected_encounters = WclZoneFactory.get_boss_names_from_zone_id(GlobalConfigs.WCL_ZONE_ID)
        FormatSpelllist.validate_encounter_names(no_dupe_df, expected_encounters)
        for name in expected_encounters:
            filtered_df = FormatSpelllist.filter_by_encounter_name(no_dupe_df, name)
            spell_df = FormatSpelllist.create_ability_dict(filtered_df)
            spell_df = FormatSpelllist.map_ally_deaths_to_spells(filtered_df, spell_df)
            #added_npcs_df = FormatSpelllist.visit_wowhead(spell_df, name)
            file_path = FilePathConsts.wcl_spell_list_csv_path(GlobalConfigs.WCL_ZONE_ID, name)
            Utils.write_pandas_df(spell_df, file_path)

    @staticmethod
    def visit_wowhead(df: pd.DataFrame, name: str) -> pd.DataFrame:
        spell_to_npc_mapping = {}
        spell_ids = df['SpellID'].tolist()
        print(f"Scraping spell_ids for encounter {name}:")
        count = 0
        for spell_id in spell_ids:
            count += 1
            print(f"Scraping spell_id {spell_id} from Wowhead ({count} of {len(spell_ids)})")
            wowhead_spell = WowheadSpell(spell_id)
            spell_to_npc_mapping[spell_id] = wowhead_spell.npc_name

        # Add spell_to_npc_mapping as a new column to the df
        df['NPCName'] = df['SpellID'].map(spell_to_npc_mapping)
        return df

    @staticmethod
    def load_encounters_df() -> pd.DataFrame:
        csv_path = FilePathConsts.wcl_log_encounter_csv_path(GlobalConfigs.WCL_ZONE_ID)
        df = Utils.read_pandas_df(csv_path)
        if df.empty:
            print("Error: Pandas dataframe is empty! Run the scrape_wcl_encounters script first!")
        return df

    @staticmethod
    def load_spell_list_df(encounter_name) -> pd.DataFrame:
        csv_path = FilePathConsts.wcl_spell_list_csv_path(GlobalConfigs.WCL_ZONE_ID, encounter_name)
        df = Utils.read_pandas_df(csv_path)
        if df.empty:
            print("Error: Pandas dataframe is empty! Run the scrape_wcl_encounters script first!")
        return df

    @staticmethod
    def filter_outcomes_that_are_kill(df: pd.DataFrame) -> pd.DataFrame:
        filtered_df = df[df['fight_outcome'] == 'kill'].copy()
        filtered_df.reset_index(drop=True, inplace=True)
        return filtered_df

    @staticmethod
    def validate_encounter_names(df: pd.DataFrame, expected_encounters: List[str]) -> None:
        for _, row in df.iterrows():
            matching_names1 = row['fight_boss_text'] == row['fight_zone_name']
            matching_names2 = row['fight_boss_text'] == row['encounter_name']
            if (not matching_names1 or not matching_names2) and (row['fight_boss_text'] != 'nan' or row['fight_boss_text'] is not None):
                print(f"BudoWarning: Mismatch in dungeon/fight name for {row['fight_boss_text']} != {row['fight_zone_name']} != {row['encounter_name']}")
            if row['encounter_name'] not in expected_encounters:
                print(f"BudoWarning: Unexpected encounter {row['encounter_name']} encountered.")


    @staticmethod
    def filter_by_encounter_name(df: pd.DataFrame, encounter_name: str) -> pd.DataFrame:
        filtered_df = df[df['encounter_name'] == encounter_name].copy()
        filtered_df.reset_index(drop=True, inplace=True)
        return filtered_df

    @staticmethod
    def remove_duplicate_logs(df: pd.DataFrame) -> pd.DataFrame:
        # Sort by one of the columns to reduce the number of comparisons
        df.sort_values(by='fight_duration_in_sec', inplace=True)
        # Drop duplicates based on the relevant columns
        filtered_df = df.drop_duplicates(subset=['fight_duration_in_sec', 'encounter_name',
                                                 'setup_players', 'ally_deaths'], keep='first')
        # Reset index for the cleaned DataFrame
        filtered_df.reset_index(drop=True, inplace=True)
        return filtered_df

    @staticmethod
    def create_ability_dict(df: pd.DataFrame) -> pd.DataFrame:
        # Initialize a dictionary to store ability data
        ability_dict: Dict[str, Dict[str, Union[str, int, float]]] = defaultdict(lambda: {
            "SpellID": 0, "SpellName": "", "SpellCasts": 0, "SpellFound": 0, "SpellFoundPercent": 0.0
        })
        total_rows = len(df)

        for _, row in df.iterrows():
            ability_list = row['ability_list']
            seen_abilities = set()  # Track abilities seen in the current row

            for ability in ability_list.strip("[]").split(", "):
                # Parsing the ability information
                ability_info = ability.strip("'").split('░')
                spell_id = str(int(ability_info[0].replace('"', '')))
                spell_name = ability_info[1]
                spell_casts = int(ability_info[2].replace('"', ''))

                # Initialize or update the ability data in the dictionary
                if ability_dict[spell_id]["SpellID"] == 0:
                    ability_dict[spell_id]["SpellID"] = int(spell_id)
                    ability_dict[spell_id]["SpellName"] = spell_name
                    ability_dict[spell_id]["SpellCasts"] = spell_casts
                else:
                    ability_dict[spell_id]["SpellCasts"] += spell_casts  # type: ignore [operator]

                # Only increment SpellFound if this ability hasn't been seen in the current row
                if spell_id not in seen_abilities:
                    ability_dict[spell_id]["SpellFound"] += 1  # type: ignore [operator]
                    seen_abilities.add(spell_id)

        # Calculate the percentage of rows where each ability was found
        for spell_id, data in ability_dict.items():
            data["SpellFoundPercent"] = (data["SpellFound"] / total_rows) * 100 if total_rows > 0 else 0.0  # type: ignore [operator]

        # Convert the dictionary to a DataFrame
        ability_df = pd.DataFrame.from_dict(ability_dict, orient='index').reset_index(drop=True)
        return ability_df

    @staticmethod
    def map_ally_deaths_to_spells(df: pd.DataFrame, spell_df: pd.DataFrame) -> pd.DataFrame:
        lethal_spell_ids: Dict[int, int] = {}
        assisting_spell_ids: Dict[int, int] = {}
        delimiter = '░'

        for _, row in df.iterrows():
            ally_deaths_str = row['ally_deaths']
            ally_deaths = ally_deaths_str[1:-1].split("', '")
            ally_deaths[0] = ally_deaths[0][1:]
            ally_deaths[-1] = ally_deaths[-1][:-1]

            for death in ally_deaths:
                death_parts = death.split(delimiter)
                death_dict = {
                    'name_of_player': death_parts[0] if len(death_parts) > 0 else '',
                    'killing_blow_name': death_parts[1] if len(death_parts) > 1 else '',
                    'killing_blow_id': death_parts[2] if len(death_parts) > 2 else -1,
                    'over': death_parts[3] if len(death_parts) > 3 else '',
                    'hit_1_name': death_parts[4] if len(death_parts) > 4 else '',
                    'hit_1_id': death_parts[5] if len(death_parts) > 5 else -1,
                    'hit_2_name': death_parts[6] if len(death_parts) > 6 else '',
                    'hit_2_id': death_parts[7] if len(death_parts) > 7 else -1,
                    'hit_3_name': death_parts[8] if len(death_parts) > 8 else '',
                    'hit_3_id': death_parts[9] if len(death_parts) > 9 else -1,
                    'damage_taken': death_parts[10] if len(death_parts) > 10 else '',
                    'healing_received': death_parts[11] if len(death_parts) > 11 else '',
                }

                # Convert spell IDs to integers if possible
                try:
                    killing_blow_id = int(death_dict['killing_blow_id'])
                except ValueError:
                    killing_blow_id = -1

                if killing_blow_id != -1:
                    if killing_blow_id not in lethal_spell_ids:
                        lethal_spell_ids[killing_blow_id] = 1
                    else:
                        lethal_spell_ids[killing_blow_id] += 1

                assisting_keys = ['killing_blow_id', 'hit_1_id', 'hit_2_id', 'hit_3_id']
                for key in assisting_keys:
                    try:
                        spell_id = int(death_dict[key])
                    except ValueError:
                        spell_id = -1

                    if spell_id != -1:
                        if spell_id not in assisting_spell_ids:
                            assisting_spell_ids[spell_id] = 1
                        else:
                            assisting_spell_ids[spell_id] += 1

        spell_df['KillingBlowCount'] = spell_df['SpellID'].map(lethal_spell_ids).fillna(0).astype(int)
        spell_df['AssistingBlowCount'] = spell_df['SpellID'].map(assisting_spell_ids).fillna(0).astype(int)

        return FormatSpelllist.add_blow_percentages(spell_df)

    @staticmethod
    def add_blow_percentages(df):
        # Calculate the total number of killing blows and assisting blows
        total_killing_blows = df['KillingBlowCount'].sum()
        total_assisting_blows = df['AssistingBlowCount'].sum()

        # Calculate the KillingBlowPercent and AssistingBlowPercent for each row
        df['KillingBlowPercent'] = (df['KillingBlowCount'] / total_killing_blows) * 100
        df['AssistingBlowPercent'] = (df['AssistingBlowCount'] / total_assisting_blows) * 100

        return df