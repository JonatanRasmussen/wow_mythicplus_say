

class SpellConfig:

    def __init__(self, spell_id: int, npc_zone: int,
                 instance_id: str, use_nameplate: bool, chat_msg: str):
        self.spell_id: int = spell_id
        self.npc_zone: int = npc_zone
        self.instance_id: str = instance_id
        self.use_nameplate: bool = use_nameplate
        self.chat_msg: str = chat_msg