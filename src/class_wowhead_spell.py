import os
import requests
import pandas as pd
from typing import List

from .config.consts_file_paths import FilePathConsts
from .config.global_configs import GlobalConfigs
from .utils import Utils


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

    @staticmethod
    def write_wowhead_spell_ids_to_csv(wowhead_spells: List['WowheadSpell']) -> None:
        # Convert the list of dataclass objects to a list of dictionaries
        wowhead_spells_dict_list = [wowhead_spell.__dict__ for wowhead_spell in wowhead_spells]
        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(wowhead_spells_dict_list)
        file_path = FilePathConsts.wowhead_spell_ids_csv_path(GlobalConfigs.WCL_ZONE_ID)
        Utils.write_pandas_df(df, file_path)


    def print_all_data(self) -> None:
        exclude_attrs = ['page_source', 'zone_page_source']
        print()
        for attr, value in self.__dict__.items():
            if attr not in exclude_attrs:
                print(f"{attr}: {value}")

    def _cache_page_source(self, spell_id: int, page_source: str, is_zone_instead: bool) -> None:
        folder = FilePathConsts.CACHED_HTML_WOWHEAD_ZONE_IDS if is_zone_instead else FilePathConsts.CACHED_HTML_WOWHEAD_SPELL_IDS
        file_path = os.path.join(folder, f"{spell_id}.html")
        os.makedirs(folder, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(page_source)

    def _load_page_source(self, spell_id: int, is_zone_instead: bool) -> str:
        if spell_id == WowheadSpell._GENERIC_NOT_FOUND_NUMERIC_VALUE:
            return WowheadSpell._BAD_URL_INPUT_VALUE
        enable_rescrape = GlobalConfigs.WOWHEAD_ZONE_IDS_RESCRAPE if is_zone_instead else GlobalConfigs.WOWHEAD_SPELL_IDS_RESCRAPE
        folder = FilePathConsts.CACHED_HTML_WOWHEAD_ZONE_IDS if is_zone_instead else FilePathConsts.CACHED_HTML_WOWHEAD_SPELL_IDS
        file_path = os.path.join(folder, f"{spell_id}.html")
        if not enable_rescrape and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        return self._fetch_wowhead_page_source(spell_id, is_zone_instead)

    def _fetch_wowhead_page_source(self, spell_id: int, is_zone_instead: bool) -> str:
        sub_url = "zone" if is_zone_instead else "spell"
        url = f"https://www.wowhead.com/{GlobalConfigs.WOWHEAD_PTR_VERSION}{sub_url}={spell_id}"
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