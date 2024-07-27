import os
import requests
import pandas as pd
from typing import List

from .config.consts_wowhead import WowheadConsts
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


class SpreadsheetSpell:

    def __init__(self, dungeon: str, zone_id: str, section: str,
                 cast: str, rt: str, action: str, wa_name: str,
                 spell_id: int, icon_id: int, roles: str):
        self.dungeon: str = dungeon
        self.zone_id: str = zone_id
        self.section: str = section
        self.cast: str = cast
        self.rt: str = rt
        self.action: str = action
        self.wa_name: str = wa_name
        self.spell_id: int = spell_id
        self.icon_id: int = icon_id
        self.roles: str = roles
        self.ability_name: str = self._parse_ability_name(wa_name)
        self.spell_name_and_id: str = f"{self.ability_name} {spell_id}"

    def print_all_data(self) -> None:
        print()
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")

    def cross_reference_wowhead_data(self) -> None:
        wowhead_spell = WowheadSpell(self.spell_id)
        self._crossref_spell_name(wowhead_spell)
        self._crossref_icon_id(wowhead_spell)
        self._crossref_channeled_cast(wowhead_spell)
        self._crossref_instant_cast(wowhead_spell)
        self._crossref_zone_name(wowhead_spell)
        return

    def _parse_ability_name(self, ability_name: str) -> str:
        if len(ability_name) != 0 and ability_name[-1].isdigit():
            return ability_name[:-1]
        return ability_name

    def _crossref_spell_name(self, wowhead_spell: 'WowheadSpell') -> None:
        if wowhead_spell.spell_name != self.ability_name:
            print(f"Warning: {self.spell_name_and_id}'s spell_name "
                  f"({self.ability_name}) does not match Wowhead's name "
                  f"({wowhead_spell.spell_name})")

    def _crossref_icon_id(self, wowhead_spell: 'WowheadSpell') -> None:
        if self.icon_id != -1 and wowhead_spell.icon_id != self.icon_id:
            print(f"Error: {self.spell_name_and_id}'s icon_id "
                  f"({self.icon_id}) does not match Wowhead's icon_id "
                  f"({wowhead_spell.icon_id})")

    def _crossref_channeled_cast(self, wowhead_spell: 'WowheadSpell') -> None:
        if self.cast == SpreadsheetConsts.CAST_VALUE_CHANNEL and not wowhead_spell.cast_value_is_channeled:
            print(f"Error: {self.spell_name_and_id}'s cast type "
                  f"({self.cast}) does not match Wowhead's cast_time "
                  f"({wowhead_spell.cast_time})")

    def _crossref_instant_cast(self, wowhead_spell: 'WowheadSpell') -> None:
        if self.cast == SpreadsheetConsts.CAST_VALUE_CAST and wowhead_spell.cast_value_is_instant:
            print(f"Error: {self.spell_name_and_id}'s cast type "
                  f"({self.cast}) does not match Wowhead's cast_time "
                  f"({wowhead_spell.cast_time})")

    def _crossref_zone_name(self, wowhead_spell: 'WowheadSpell') -> None:
        if wowhead_spell.zone_name != self.dungeon and wowhead_spell.zone_name_was_found:
            print(f"Error: {self.spell_name_and_id}'s dungeon "
                  f"({self.dungeon}) does not match Wowhead's zone_name "
                  f"({wowhead_spell.zone_name})")


class WowheadSpell:

    # Page source statuses
    _BAD_RESPONSE_VALUE = "Failed to retrieve page. Status code:"
    _BAD_URL_INPUT_VALUE = "Bad input value. Retrieval of page was not attempted."

    # Default values for missing data
    _GENERIC_NOT_FOUND_NUMERIC_VALUE = -1
    _ICON_ID_NOT_FOUND = "Icon ID Not Found"
    _SPELL_NAME_NOT_FOUND = "Name Not Found"
    _CAST_TIME_NOT_FOUND = "Cast Time Not Found"
    _ZONE_ID_NOT_FOUND = "Zone ID Not Found"
    _ZONE_NAME_NOT_FOUND = "Zone Name Not Found"

    # WowHead values
    _CHANNELED_CAST_VALUE = "Channeled"
    _INSTANT_CAST_VALUE = "Instant"

    def __init__(self, spell_id: int):
        self.page_source: str = self._load_page_source(spell_id, False)
        self.page_source_is_valid: bool = self._page_source_is_code_200(self.page_source)
        self.spell_name: str = self._parse_spell_name()
        self.spell_id: int = spell_id
        self.icon_id: int = self._parse_icon_id()
        self.cast_time: str = self._parse_cast_time()
        self.cast_value_is_channeled: bool = self.cast_time == WowheadSpell._CHANNELED_CAST_VALUE
        self.cast_value_is_instant: bool = self.cast_time == WowheadSpell._INSTANT_CAST_VALUE
        self.zone_id: int = self._parse_zone_id()
        self.zone_page_source: str = self._load_page_source(self.zone_id, True)
        self.zone_page_source_is_valid: bool = self._page_source_is_code_200(self.zone_page_source)
        self.zone_name: str = self._parse_zone_name()
        self.zone_name_was_found: bool = self.zone_name != WowheadSpell._ZONE_NAME_NOT_FOUND

    def print_all_data(self) -> None:
        exclude_attrs = ['page_source', 'zone_page_source']
        print()
        for attr, value in self.__dict__.items():
            if attr not in exclude_attrs:
                print(f"{attr}: {value}")

    def _cache_page_source(self, spell_id: int, page_source: str, is_zone_instead: bool) -> None:
        folder = WowheadConsts.ZONE_ID_CACHE if is_zone_instead else WowheadConsts.SPELL_ID_CACHE
        file_path = os.path.join(folder, f"{spell_id}.html")
        os.makedirs(folder, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(page_source)

    def _load_page_source(self, spell_id: int, is_zone_instead: bool) -> str:
        if spell_id == WowheadSpell._GENERIC_NOT_FOUND_NUMERIC_VALUE:
            return WowheadSpell._BAD_URL_INPUT_VALUE
        rescrape = WowheadConsts.RESCRAPE_ZONE_IDS if is_zone_instead else WowheadConsts.RESCRAPE_SPELL_IDS
        folder = WowheadConsts.ZONE_ID_CACHE if is_zone_instead else WowheadConsts.SPELL_ID_CACHE
        file_path = os.path.join(folder, f"{spell_id}.html")
        if not rescrape and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        return self._fetch_wowhead_page_source(spell_id, is_zone_instead)

    def _fetch_wowhead_page_source(self, spell_id: int, is_zone_instead: bool) -> str:
        sub_url = "zone" if is_zone_instead else "spell"
        url = f"https://www.wowhead.com/{WowheadConsts.PTR_VERSION}{sub_url}={spell_id}"
        response = requests.get(url, timeout=5000)
        if response.status_code == 200:
            self._cache_page_source(spell_id, response.text, is_zone_instead)
            return response.text
        return f"{WowheadSpell._BAD_RESPONSE_VALUE} {response.status_code}"

    def _page_source_is_code_200(self, page_source: str) -> bool:
        if page_source == WowheadSpell._BAD_URL_INPUT_VALUE:
            return False
        error_msg = WowheadSpell._BAD_RESPONSE_VALUE
        if len(page_source) >= len(error_msg):
            if page_source[0:len(error_msg)] != error_msg:
                return True
        print("Error: Page source is not code 200.")
        return False

    def _scuffed_html_parser(self, html: str, start: str, end: str, default: str) -> str:
        if start in html:
            split_start = html.split(start, 1)
            if len(split_start) > 1:
                split_end = split_start[1].split(end, 1)
                if len(split_end) > 1:
                    return split_end[0].strip()
        print(f"Warning: Default value '{default}' triggered for spell_id {self.spell_id}")
        return default

    def _parse_spell_name(self) -> str:
        html = self.page_source
        start = "<title>"
        end = " - Spell"
        default = WowheadSpell._SPELL_NAME_NOT_FOUND
        return self._scuffed_html_parser(html, start, end, default)

    def _parse_icon_id(self) -> int:
        html = self.page_source
        start = 'href="https://wow.zamimg.com/https://wow.zamimg.com/images/wow/icons/large/'
        end = '.jpg">'
        default = WowheadSpell._ICON_ID_NOT_FOUND
        icon_id_str = self._scuffed_html_parser(html, start, end, default)
        if icon_id_str == WowheadSpell._ICON_ID_NOT_FOUND:
            return WowheadSpell._GENERIC_NOT_FOUND_NUMERIC_VALUE
        try:
            return int(icon_id_str)
        except ValueError:
            print(f"Warning: Icon ID {icon_id_str} for {self.spell_id} is not numeric.")
            return int(default)

    def _parse_cast_time(self) -> str:
        html = self.page_source
        start = "<th>Cast time</th>"
        end = "</tr>"
        default = WowheadSpell._CAST_TIME_NOT_FOUND
        value_row = self._scuffed_html_parser(html, start, end, default)
        inner_start = "<td>"
        inner_end = "</td>"
        return self._scuffed_html_parser(value_row, inner_start, inner_end, default)

    def _parse_zone_id(self) -> int:
        html = self.page_source
        start = ',"location":['
        end = "],"
        default = WowheadSpell._ZONE_ID_NOT_FOUND
        zone_id_str = self._scuffed_html_parser(html, start, end, default)
        if zone_id_str == WowheadSpell._ZONE_ID_NOT_FOUND:
            return WowheadSpell._GENERIC_NOT_FOUND_NUMERIC_VALUE
        try:
            return int(zone_id_str)
        except ValueError:
            print(f"Warning: Zone ID {zone_id_str} for {self.spell_id} is not numeric.")
            return int(default)

    def _parse_zone_name(self) -> str:
        html = self.zone_page_source
        start = '},"name":"'
        end = '",'
        default = WowheadSpell._ZONE_NAME_NOT_FOUND
        if not self.zone_page_source_is_valid:
            return default
        return self._scuffed_html_parser(html, start, end, default)