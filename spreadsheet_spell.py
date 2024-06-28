from wowhead_spell import WowheadSpell

class SpreadsheetSpell:

    # Cast column expected values
    CAST_VALUE_CAST = "Cast"
    CAST_VALUE_CHANNEL = "Channel"
    CAST_VALUE_SUCCESS = "Success"

    # Role column expected values
    ROLES_VALUE_ALL = "All"
    ROLES_VALUE_TANK = "Tank"

    def __init__(self, dungeon: str,zone_id: str, section: str,
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
        for attr, value in self.__dict__.items():
            print(f"{attr}: {value}")
        print()

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

    def _crossref_spell_name(self, wowhead_spell: WowheadSpell) -> None:
        if wowhead_spell.spell_name != self.ability_name:
            print(f"Warning: {self.spell_name_and_id}'s spell_name ({self.ability_name}) does not match wowhead data ({wowhead_spell.spell_name})")

    def _crossref_icon_id(self, wowhead_spell: WowheadSpell) -> None:
        if self.icon_id != -1 and wowhead_spell.icon_id != self.icon_id:
            print(f"Error: {self.spell_name_and_id}'s icon_id ({self.icon_id}) does not match wowhead data ({wowhead_spell.icon_id})")

    def _crossref_channeled_cast(self, wowhead_spell: WowheadSpell) -> None:
        if self.cast == self.CAST_VALUE_CHANNEL and wowhead_spell.cast_value_is_channeled:
            print(f"Error: {self.spell_name_and_id}'s cast type ({self.cast}) does not match wowhead data (Cast time: {wowhead_spell.cast_time})")

    def _crossref_instant_cast(self, wowhead_spell: WowheadSpell) -> None:
        if self.cast == self.CAST_VALUE_CAST and wowhead_spell.cast_value_is_instant:
            print(f"Error: {self.spell_name_and_id}'s cast type ({self.cast}) does not match wowhead data (Cast time: {wowhead_spell.cast_time})")

    def _crossref_zone_name(self, wowhead_spell: WowheadSpell) -> None:
        if wowhead_spell.zone_name != self.dungeon:
            print(f"Error: {self.spell_name_and_id}'s dungeon ({self.dungeon}) does not match wowhead data ({wowhead_spell.zone_name})")