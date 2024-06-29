from typing import List
import pandas as pd

from global_configs import GlobalConfigs
from spreadsheet_spell import SpreadsheetSpell

class ParseExcelsheet:

    @staticmethod
    def generate_weakaura_code() -> str:
        df = ParseExcelsheet._get_df()
        spells = ParseExcelsheet._create_spelllist(df)
        weakaura_code = ParseExcelsheet._create_weakaura_code(spells)
        return weakaura_code


    @staticmethod
    def _get_df() -> pd.DataFrame:
        file_name = GlobalConfigs.EXCEL_SHEET_NAME
        df = pd.read_excel(file_name)
        return df

    @staticmethod
    def _create_spelllist(df: pd.DataFrame) -> List[SpreadsheetSpell]:
        spells = []
        for index, row in df.iterrows():
            print(f"{int(str(index)) + 1} of {df.shape[0]}: {row['Dungeon']} {row['Section']} {row['SpellID']} {row['AbilityName']}")
            spell = SpreadsheetSpell(
                dungeon=row['Dungeon'],
                zone_id=row['ZoneID'],
                section=row['Section'],
                cast=row['Cast'],
                rt=row['Rt'],
                action=row['Action'],
                wa_name=row['AbilityName'],
                spell_id=row['SpellID'],
                icon_id=row['IconID'],
                roles=row['Roles']
            )
            spell.cross_reference_wowhead_data()
            spells.append(spell)
        return spells

    @staticmethod
    def _create_weakaura_code(spells: List[SpreadsheetSpell]) -> str:
        return str(len(spells))
