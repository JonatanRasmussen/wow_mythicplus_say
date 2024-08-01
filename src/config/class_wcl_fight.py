from dataclasses import dataclass

@dataclass
class WclFight:
    log_guid: str
    fight_id: str
    outcome: str
    duration: str
    duration_in_sec: int
    wcl_boss_id: str
    boss_text: str
    zone_name: str
    boss_level: str
    affix_icon: str
    fight_time: str