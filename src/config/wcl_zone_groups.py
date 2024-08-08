from typing import List

class WclZoneFactory:

    # Keys
    NAME_KEY = "name"
    BOSSES_KEY = "bosses"

    ZONE_ID_TWW_MYTHICPLUS_S1 = "39"

    # Data
    WCL_ZONES = {
        ZONE_ID_TWW_MYTHICPLUS_S1: {
            NAME_KEY: "TWW M+ S1",
            BOSSES_KEY: [
                ("12660", "",       "Ara-Kara, City of Echoes",   "AK"),
                ("12669", "",       "City of Threads",            "CoT"),
                ("60670", "10670",  "Grim Batol",                 "GB"),
                ("62290", "12290",  "Mists of Tirna Scithe",      "MoTS"),
                ("61822", "11822",  "Siege of Boralus",           "SoB"),
                ("12662", "",       "Hallowfall",                 "Db"),
                ("62286", "12286",  "The Necrotic Wake",          "NW"),
                ("12652", "",       "The Stonevault",             "Sv"),
            ]
        }
        # Add other zones here as needed
    }

    @staticmethod
    def convert_icon_url_to_boss_id(target_icon_url: str) -> str:
        for zone_data in WclZoneFactory.WCL_ZONES.values():
            for boss_data in zone_data[WclZoneFactory.BOSSES_KEY]:
                boss_id, icon_url = boss_data[0], boss_data[1]

                if icon_url and icon_url == target_icon_url:
                    return boss_id
                if icon_url == "" and target_icon_url == boss_id:
                    return boss_id

        return ""

    @classmethod
    def get_boss_ids_from_zone_id(cls, wcl_zone_id: str) -> List[str]:
        if wcl_zone_id in cls.WCL_ZONES:
            zone_data = cls.WCL_ZONES[wcl_zone_id]
            return [boss_data[0] for boss_data in zone_data[cls.BOSSES_KEY]]
        return []

    @classmethod
    def get_boss_names_from_zone_id(cls, wcl_zone_id: str) -> List[str]:
        if wcl_zone_id in cls.WCL_ZONES:
            zone_data = cls.WCL_ZONES[wcl_zone_id]
            return [boss_data[2] for boss_data in zone_data[cls.BOSSES_KEY]]
        return []

    @classmethod
    def get_zone_id_from_boss_id(cls, wcl_boss_id: str) -> str:
        for zone_id, zone_data in cls.WCL_ZONES.items():
            for boss_data in zone_data[cls.BOSSES_KEY]:
                if boss_data[0] == wcl_boss_id:
                    return zone_id
        return ""

    @staticmethod
    def boss_id_is_valid(wcl_boss_id: str) -> bool:
        return WclZoneFactory.get_zone_id_from_boss_id(wcl_boss_id) != ""