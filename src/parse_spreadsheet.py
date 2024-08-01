import pandas as pd
from typing import List

from .class_spreadsheet_spell import SpreadsheetSpell
from .config.consts_spreadsheets import SpreadsheetConsts


class ParseSpreadsheet:

    @staticmethod
    def generate_weakaura_code() -> str:
        df = ParseSpreadsheet._read_df_from_spreadsheet()
        spells = ParseSpreadsheet._create_spell_list(df)
        weakaura_code = ParseSpreadsheet._create_weakaura_code(spells)
        return weakaura_code

    @staticmethod
    def _read_df_from_spreadsheet() -> pd.DataFrame:
        file_path = SpreadsheetConsts.SPREADSHEET_PATH
        df = pd.read_excel(file_path)
        return df

    @staticmethod
    def _create_spell_list(df: pd.DataFrame) -> List['SpreadsheetSpell']:
        spells = []
        for index, row in df.iterrows():
            print(f"{int(str(index)) + 1} of {df.shape[0]}: "
                  f"{row[SpreadsheetConsts.COLUMN_DUNGEON]} {row[SpreadsheetConsts.COLUMN_SECTION]} "
                  f"{row[SpreadsheetConsts.COLUMN_SPELL_ID]} {row[SpreadsheetConsts.COLUMN_ABILITY_NAME]}")

            spell = SpreadsheetSpell(
                dungeon=row[SpreadsheetConsts.COLUMN_DUNGEON],
                zone_id=row[SpreadsheetConsts.COLUMN_ZONE_ID],
                section=row[SpreadsheetConsts.COLUMN_SECTION],
                cast=row[SpreadsheetConsts.COLUMN_CAST],
                rt=row[SpreadsheetConsts.COLUMN_RT],
                action=row[SpreadsheetConsts.COLUMN_ACTION],
                wa_name=row[SpreadsheetConsts.COLUMN_ABILITY_NAME],
                spell_id=row[SpreadsheetConsts.COLUMN_SPELL_ID],
                icon_id=row[SpreadsheetConsts.COLUMN_SPELL_ICON],
                roles=row[SpreadsheetConsts.COLUMN_ROLES]
            )
            spell.cross_reference_wowhead_data()
            spells.append(spell)
        return spells

    @staticmethod
    def _create_weakaura_code(spells: List['SpreadsheetSpell']) -> str:
        return str(len(spells))