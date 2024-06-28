
WeakAurasSaved = {
["displays"] = {
["ThisIsTest"] = {
["iconSource"] = -1,
["icon"] = true,
["regionType"] = "icon",
["internalVersion"] = 75,
["id"] = "ThisIsTest",
["parent"] = "GroupTest",
["alpha"] = 0,
["height"] = 16,
["width"] = 16,
["triggers"] = {
{
["trigger"] = {
["use_castType"] = true,
["type"] = "unit",
["use_alwaystrue"] = false,
["subeventSuffix"] = "_CAST_START",
["event"] = "Cast",
["unit"] = "nameplate",
["castType"] = "cast",
["spellIds"] = {
372696,
},
["use_spellIds"] = true,
["subeventPrefix"] = "SPELL",
["use_unit"] = true,
["names"] = {
},
["debuffType"] = "HELPFUL",
},
},
["activeTriggerMode"] = -10,
},
["load"] = {
["use_zone"] = false,
["use_zoneIds"] = true,
["talent"] = {
["multi"] = {
},
},
["zoneIds"] = "g430",
},
["actions"] = {
["start"] = {
["message_type"] = "SAY",
["do_message"] = true,
["message"] = "Dangerdanger",
},
},
},
["ThisIsTest2"] = {
["iconSource"] = 0,
["displayIcon"] = "451165",
["icon"] = true,
["regionType"] = "icon",
["internalVersion"] = 75,
["id"] = "ThisIsTest2",
["parent"] = "GroupTest",
["alpha"] = 0,
["height"] = 16,
["width"] = 16,
["triggers"] = {
{
["trigger"] = {
["use_castType"] = true,
["type"] = "combatlog",
["use_alwaystrue"] = false,
["subeventSuffix"] = "_CAST_SUCCESS",
["spellId"] = {
372730,
},
["use_sourceName"] = false,
["event"] = "Combat Log",
["unit"] = "nameplate",
["castType"] = "cast",
["use_spellId"] = true,
["spellIds"] = {
372730,
},
["use_spellIds"] = true,
["names"] = {
},
["use_unit"] = true,
["subeventPrefix"] = "SPELL",
["debuffType"] = "HELPFUL",
},
},
["activeTriggerMode"] = -10,
},
["load"] = {
["use_zone"] = false,
["use_zoneIds"] = true,
["talent"] = {
["multi"] = {
},
},
["zoneIds"] = "g430",
},
["actions"] = {
["start"] = {
["message_type"] = "SAY",
["do_message"] = true,
["message"] = "Maybedanger",
},
},
},
["GroupTest"] = {
["iconSource"] = -1,
["icon"] = true,
["regionType"] = "group",
["internalVersion"] = 75,
["scale"] = 1,
["id"] = "GroupTest",
["controlledChildren"] = {
"ThisIsTest2",
"ThisIsTest",
},
},
},
}