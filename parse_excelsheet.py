from typing import List
import pandas as pd

from global_configs import GlobalConfigs
from spreadsheet_spell import SpreadsheetSpell

class ParseExcelsheet:

    @staticmethod
    def _generate_weakaura_code() -> str:
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
        for _, row in df.iterrows():
            spell = SpreadsheetSpell(
                dungeon=row['Dungeon'],
                zone_id=row['ZoneID'],
                section=row['Section'],
                cast=row['Cast'],
                rt=row['Rt'],
                action=row['Action'],
                wa_name=row['AbilityName'],
                spell_id=row['Spell ID'],
                icon_id=row['Icon ID'],
                roles=row['Roles']
            )
            spell.cross_reference_wowhead_data()
            spells.append(spell)
        return spells

    @staticmethod
    def _create_weakaura_code(spells: List[SpreadsheetSpell]) -> str:
        return str(len(spells))
