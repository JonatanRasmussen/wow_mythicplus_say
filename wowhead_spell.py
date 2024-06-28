import os
import requests

from global_configs import GlobalConfigs

class WowheadSpell:

    # Default values for missing data
    _BAD_RESPONSE_VALUE = "Failed to retrieve page. Status code:"
    _ICON_ID_NOT_FOUND = -1
    _SPELL_NAME_NOT_FOUND = "Name Not Found"
    _CAST_TIME_NOT_FOUND = "Cast Time Not Found"
    _ZONE_ID_NOT_FOUND = "Zone ID Not Found"
    _ZONE_NAME_NOT_FOUND = "Zone Name Not Found"

    # WowHead values
    _CHANNELED_CAST_VALUE = "Channeled"
    _INSTANT_CAST_VALUE = "Instant"

    def __init__(self, spell_id: int):
        self.page_source: str = self._load_page_source(spell_id)
        self.spell_name: str = self._parse_spell_name()
        self.spell_id: int = spell_id
        self.icon_id: int = self._parse_icon_id()
        self.cast_time: str = self._parse_cast_time()
        self.cast_value_is_channeled: bool = self.cast_time == WowheadSpell._CHANNELED_CAST_VALUE
        self.cast_value_is_instant: bool = self.cast_time == WowheadSpell._INSTANT_CAST_VALUE
        self.zone_id: str = self._parse_zone_id()
        self.zone_name: str = self._parse_zone_name()
        self.page_source_is_valid: bool = self._page_source_is_code_200()

    def print_all_data(self) -> None:
        exclude_attrs = ['page_source']
        for attr, value in self.__dict__.items():
            if attr not in exclude_attrs:
                print(f"{attr}: {value}")
        print()

    def _save_page_source(self, spell_id: int) -> None:
        if GlobalConfigs.SAVE_WOWHEAD_PAGES_LOCALLY:
            folder = GlobalConfigs.CACHED_WOWHEAD_PAGES_FOLDER
            file_path = os.path.join(folder, f"{spell_id}.html")
            os.makedirs(folder, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.page_source)

    def _load_page_source(self, spell_id: int) -> str:
        folder = GlobalConfigs.CACHED_WOWHEAD_PAGES_FOLDER
        file_path = os.path.join(folder, f"{spell_id}.html")
        if GlobalConfigs.USE_CACHED_WOWHEAD_PAGES and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        return self._fetch_wowhead_page_source(spell_id)


    def _scuffed_html_parser(self, html: str, start: str, end: str, default: str) -> str:
        if start in html:
            split_start = html.split(start, 1)
            if len(split_start) > 1:
                split_end = split_start[1].split(end, 1)
                if len(split_end) > 1:
                    return split_end[0].strip()
        print(f"Warning: Default value '{default}' triggered for spell_id {self.spell_id}")
        return default

    def _fetch_wowhead_page_source(self, spell_id: int) -> str:
        ptr_version = GlobalConfigs.PTR_VERSION
        url = f"https://www.wowhead.com/{ptr_version}spell={spell_id}"
        response = requests.get(url, timeout=5000)
        if response.status_code == 200:
            return response.text
        self._save_page_source(spell_id)
        return f"{WowheadSpell._BAD_RESPONSE_VALUE} {response.status_code}"

    def _page_source_is_code_200(self) -> bool:
        error_msg = WowheadSpell._BAD_RESPONSE_VALUE
        if len(self.page_source) >= len(error_msg):
            if self.page_source[0:len(error_msg)] != error_msg:
                return True
        return False

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
        default = str(WowheadSpell._ICON_ID_NOT_FOUND)
        return int(self._scuffed_html_parser(html, start, end, default))

    def _parse_cast_time(self) -> str:
        html = self.page_source
        start = "<th>Cast time</th>"
        end = "</tr>"
        default = WowheadSpell._CAST_TIME_NOT_FOUND
        value_row = self._scuffed_html_parser(html, start, end, default)
        inner_start = "<td>"
        inner_end = "</td>"
        return self._scuffed_html_parser(value_row, inner_start, inner_end, default)

    def _parse_zone_id(self) -> str:
        html = self.page_source
        start = ',"location":['
        end = "],"
        default = WowheadSpell._ZONE_ID_NOT_FOUND
        return self._scuffed_html_parser(html, start, end, default)

    def _parse_zone_name(self) -> str:
        html = self.page_source
        start = '" onmousedown="return false">'
        end = "</a>"
        default = WowheadSpell._ZONE_NAME_NOT_FOUND
        return self._scuffed_html_parser(html, start, end, default)