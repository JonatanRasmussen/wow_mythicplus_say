import os
import requests


class WowheadSpell:

    _PAGE_SOURCE_FOLDER = "wowhead_spell_ids"
    _BAD_RESPONSE_VALUE = "Failed to retrieve page. Status code:"
    _CAST_TIME_NOT_FOUND = "Not Found"
    _CHANNELED_CAST_VALUE = "Channeled"
    _INSTANT_CAST_VALUE = "Instant"

    def __init__(self, spell_id: int, npc_zone: int):
        self.spell_id: int = spell_id
        self.npc_zone: int = npc_zone
        self.page_source: str = self._fetch_wowhead_page_source()
        self.page_source_is_valid: bool = self._page_source_is_code_200()
        self.cast_value: str = self._parse_cast_value()
        self.cast_value_is_channeled: bool = self.cast_value == WowheadSpell._CHANNELED_CAST_VALUE
        self.cast_value_is_instant: bool = self.cast_value == WowheadSpell._INSTANT_CAST_VALUE
        self.location: str = self._parse_location()
        self.location_matches_zone: bool = self.location == str(self.npc_zone)
        self.print_page_source()
        self.save_page_source()

    def print_page_source(self) -> None:
        print(self.page_source)

    def save_page_source(self) -> None:
        folder = WowheadSpell._PAGE_SOURCE_FOLDER
        file_path = os.path.join(folder, f"{self.spell_id}.html")
        os.makedirs(folder, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"<!-- eslint-disable -->\n{self.page_source}")

    @staticmethod
    def scuffed_html_parser(html: str, start: str, end: str, default: str) -> str:
        if start in html:
            split_start = html.split(start, 1)
            if len(split_start) > 1:
                split_end = split_start[1].split(end, 1)
                if len(split_end) > 1:
                    return split_end[0].strip()
        return default

    def _fetch_wowhead_page_source(self) -> str:
        url = f"https://www.wowhead.com/spell={self.spell_id}"
        response = requests.get(url, timeout=5000)
        if response.status_code == 200:
            return response.text
        return f"{WowheadSpell._BAD_RESPONSE_VALUE} {response.status_code}"

    def _page_source_is_code_200(self) -> bool:
        error_msg = WowheadSpell._BAD_RESPONSE_VALUE
        if len(self.page_source) >= len(error_msg):
            if self.page_source[0:len(error_msg)] == error_msg:
                return True
        return False

    def _parse_cast_value(self) -> str:
        html = self.page_source
        start = "<th>Cast time</th>"
        end = "</tr>"
        default = WowheadSpell._CAST_TIME_NOT_FOUND
        value_row = WowheadSpell.scuffed_html_parser(html, start, end, default)
        inner_start = "<td>"
        inner_end = "</td>"
        return WowheadSpell.scuffed_html_parser(value_row, inner_start, inner_end, default)

    def _parse_location(self) -> str:
        html = self.page_source
        start = ',"location":['
        end = "],"
        default = WowheadSpell._CAST_TIME_NOT_FOUND
        return WowheadSpell.scuffed_html_parser(html, start, end, default)

