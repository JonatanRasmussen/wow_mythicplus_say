from spell_config import SpellConfig
from wowhead_spell import WowheadSpell

if __name__ == "__main__":
    spell_configs = [
        SpellConfig(385536, 12345, "123abc", True, "hey"),
        SpellConfig(336759, 12345, "123abc", True, "Yoyo hey"),
    ]
    for config in spell_configs:
        wowhead_spell = WowheadSpell(config.spell_id, config.npc_zone)
