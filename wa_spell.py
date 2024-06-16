

class WaSpell:

    def __init__(self, spell_id: int, instance_id: str, use_nameplate: bool, chat_msg: str):
        self.spell_id: int = spell_id
        self.instance_id: str = instance_id
        self.use_nameplate: bool = use_nameplate
        self.chat_msg: str = chat_msg