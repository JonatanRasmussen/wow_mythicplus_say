from typing import List

class WclZoneFactory:

    # Keys
    NAME_KEY = "name"
    BOSSES_KEY = "bosses"

    ZONE_ID_TWW_MYTHICPLUS = "45"
    ZONE_ID_MIDNIGHT_MYTHICPLUS = "49"

    # Data
    WCL_ZONES = {
        ZONE_ID_TWW_MYTHICPLUS: {
            NAME_KEY: "TWW M+",
            BOSSES_KEY: [
                ("62660", "Ara-Kara, City of Echoes"),
                ("12830", "Eco-Dome Al'dani"),
                ("62287", "Halls of Atonement"),
                ("62773", "Operation: Floodgate"),
                ("62649", "Priory of the Sacred Flame"),
                ("112442", "Tazavesh: So'leah's Gambit"),
                ("112441", "Tazavesh: Streets of Wonder"),
                ("62662", "The Dawnbreaker"),
            ]
        },
        ZONE_ID_MIDNIGHT_MYTHICPLUS: {
            NAME_KEY: "TWW M+",
            BOSSES_KEY: [
                ("162526", "Algeth'ar Academy"),
                ("62811", "Magister's Terrace"),
                ("62874", "Maisara Caverns"),
                ("62915", "Nexus-Point Xenas"),
                ("60658", "Pit of Saron"),
                ("411753", "Seat of the Triumvirate"),
                ("111209", "Skyreach"),
                ("62805", "Windrunner Spire"),
            ]
        }
    }

    @classmethod
    def get_boss_id_by_name(cls, dungeon_name: str) -> str:
        for _, zone_data in cls.WCL_ZONES.items():
            for boss_id, boss_name in zone_data[cls.BOSSES_KEY]:
                if boss_name == dungeon_name:
                    return boss_id
        if dungeon_name not in {"Encounters and Trash Fights", "Trash Fights", "Encounters"}:
            print(f"Warning: No match was found for {dungeon_name}")
        return "0"

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