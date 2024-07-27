from .consts_file_paths import FilePathConsts

class SpreadsheetConsts:
    # Paths
    SPREADSHEET_PATH = FilePathConsts.FINAL_OUTPUT_SPREADSHEET

    # Spreadsheet column names
    COLUMN_DUNGEON = "Dungeon"
    COLUMN_ZONE_ID = "ZoneID"
    COLUMN_SECTION = "Section"
    COLUMN_CAST = "Cast"
    COLUMN_RT = "Rt"
    COLUMN_ACTION = "Action"
    COLUMN_ABILITY_NAME = "AbilityName"
    COLUMN_SPELL_ID = "SpellID"
    COLUMN_SPELL_ICON = "IconID"
    COLUMN_ROLES = "Roles"

    # Cast column expected values
    CAST_VALUE_CAST = "Cast"
    CAST_VALUE_CHANNEL = "Channel"
    CAST_VALUE_SUCCESS = "Success"

    # Role column expected values
    ROLES_VALUE_ALL = "All"
    ROLES_VALUE_TANK = "Tank"