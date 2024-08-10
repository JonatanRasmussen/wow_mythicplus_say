import re
import ast
#https://www.wowhead.com/item=219317/harvesters-edict
html = r"""
<script type="text/javascript">//<![CDATA[
WH.Gatherer.addData(3, 1, {"219314":{"name_enus":"Ara-Kara Sacbrood","quality":3,"icon":"inv_raid_mercurialegg_red","screenshot":{},"jsonequip":{"hastertng":603,"reqlevel":68,"sellprice":581133,"slotbak":12},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"219316":{"name_enus":"Ceaseless Swarmgland","quality":3,"icon":"inv_misc_organmass_color2","screenshot":{},"jsonequip":{"agi":549,"agistr":549,"reqlevel":68,"sellprice":585302,"slotbak":12,"str":549},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"219317":{"name_enus":"Harvester's Edict","quality":3,"icon":"trade_archaeology_nerubian_obelisk","screenshot":{},"jsonequip":{"agi":549,"agiint":549,"int":549,"reqlevel":68,"sellprice":587415,"slotbak":12},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221150":{"name_enus":"Arachnoid Soulcleaver","quality":3,"icon":"inv_sword_1h_earthendungeon_c_02","screenshot":{},"jsonequip":{"appearances":{"0":[677173,""]},"critstrkrtng":148,"displayid":677173,"dmgmax1":534,"dmgmin1":320,"dmgrange":0.5,"dmgtype1":0,"dps":164.26,"int":1683,"mastrtng":275,"mledmgmax":534,"mledmgmin":320,"mledps":164.26,"mlespeed":2.6,"reqlevel":68,"sellprice":926296,"sheathtype":3,"slotbak":13,"speed":2.6,"sta":433},"attainable":0,"flags2":8712,"displayName":"","qualityTier":0},"221151":{"name_enus":"Devourer's Gauntlets","quality":3,"icon":"inv_glove_plate_earthendungeon_c_01","screenshot":{},"jsonequip":{"appearances":{"0":[678781,""]},"armor":1198,"displayid":678781,"hastertng":371,"int":433,"reqlevel":68,"sellprice":327295,"slotbak":10,"sta":650,"str":433,"strint":433,"versatility":262},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221152":{"name_enus":"Silksteel Striders","quality":3,"icon":"inv_boot_mail_earthendungeon_c_01","screenshot":{},"jsonequip":{"agi":433,"agiint":433,"appearances":{"0":[678869,""]},"armor":876,"displayid":678869,"hastertng":371,"int":433,"mastrtng":262,"reqlevel":68,"sellprice":489069,"slotbak":8,"sta":650},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221153":{"name_enus":"Gauzewoven Legguards","quality":3,"icon":"inv_leather_earthendungeon_c_01_pant","screenshot":{},"jsonequip":{"agi":578,"agiint":578,"appearances":{"0":[677329,""]},"armor":756,"critstrkrtng":332,"displayid":677329,"int":578,"mastrtng":513,"reqlevel":68,"sellprice":655735,"slotbak":7,"sta":867},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221154":{"name_enus":"Swarmcaller's Shroud","quality":3,"icon":"inv_cape_mail_earthendungeon_c_01","screenshot":{},"jsonequip":{"agi":325,"agistrint":325,"appearances":{"0":[678872,""]},"armor":252,"critstrkrtng":177,"displayid":678872,"int":325,"reqlevel":68,"sellprice":492710,"slotbak":16,"sta":488,"str":325,"versatility":299},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221155":{"name_enus":"Swarm Monarch's Spaulders","quality":3,"icon":"inv_shoulder_plate_earthendungeon_c_01","screenshot":{},"jsonequip":{"appearances":{"0":[678775,""]},"armor":1437,"displayid":678775,"int":433,"mastrtng":262,"reqlevel":68,"sellprice":494555,"slotbak":3,"sta":650,"str":433,"strint":433,"versatility":371},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221156":{"name_enus":"Cryptbound Headpiece","quality":3,"icon":"inv_helm_mail_earthendungeon_c_01","screenshot":{},"jsonequip":{"agi":578,"agiint":578,"appearances":{"0":[678864,""]},"armor":1035,"displayid":678864,"hastertng":332,"int":578,"mastrtng":513,"reqlevel":68,"sellprice":496401,"slotbak":1,"sta":867},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221157":{"name_enus":"Unbreakable Beetlebane Bindings","quality":3,"icon":"inv_leather_earthendungeon_c_01_bracer","screenshot":{},"jsonequip":{"agi":325,"agiint":325,"appearances":{"0":[677331,""]},"armor":378,"critstrkrtng":289,"displayid":677331,"int":325,"mastrtng":187,"reqlevel":68,"sellprice":334666,"slotbak":9,"sta":488},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221158":{"name_enus":"Burrower's Cinch","quality":3,"icon":"inv_belt_cloth_earthendungeon_c_01","screenshot":{},"jsonequip":{"appearances":{"0":[677294,""]},"armor":283,"critstrkrtng":412,"displayid":677294,"hastertng":222,"int":433,"reqlevel":68,"sellprice":335906,"slotbak":6,"sta":650},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221159":{"name_enus":"Harvester's Interdiction","quality":3,"icon":"inv_staff_2h_earthendungeon_c_02","screenshot":{"id":1177228,"imageType":2},"jsonequip":{"agi":578,"appearances":{"0":[677127,""]},"displayid":677127,"dmgmax1":1800,"dmgmin1":1330,"dmgrange":0.3,"dmgtype1":0,"dps":434.83,"mastrtng":350,"mledmgmax":1800,"mledmgmin":1330,"mledps":434.83,"mlespeed":3.6,"reqlevel":68,"sellprice":1197250,"sheathtype":2,"slotbak":17,"speed":3.6,"sta":867,"versatility":495},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221160":{"name_enus":"Blight Hunter's Scalpelglaive","quality":3,"icon":"inv_glaive_1h_earthendungeon_c_01","screenshot":{},"jsonequip":{"agi":289,"appearances":{"0":[677184,""]},"displayid":677184,"dmgmax1":1046,"dmgmin1":661,"dmgrange":0.45,"dmgtype1":0,"dps":328.4,"mastrtng":275,"mledmgmax":1046,"mledmgmin":661,"mledps":328.4,"mlespeed":2.6,"reqlevel":68,"sellprice":961322,"sheathtype":1,"slotbak":13,"speed":2.6,"sta":433,"versatility":148},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221161":{"name_enus":"Experimental Goresilk Chestguard","quality":3,"icon":"inv_chest_plate_earthendungeon_c_01","screenshot":{},"jsonequip":{"appearances":{"0":[678776,""]},"armor":1917,"displayid":678776,"hastertng":332,"int":578,"reqlevel":68,"sellprice":692979,"slotbak":5,"sta":867,"str":578,"strint":578,"versatility":513},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221162":{"name_enus":"Claws of Tainted Ichor","quality":3,"icon":"inv_glove_mail_earthendungeon_c_01","screenshot":{},"jsonequip":{"agi":433,"agiint":433,"appearances":{"0":[678871,""]},"armor":796,"displayid":678871,"hastertng":235,"int":433,"reqlevel":68,"sellprice":349709,"slotbak":10,"sta":650,"versatility":399},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221163":{"name_enus":"Whispering Mask","quality":3,"icon":"inv_leather_earthendungeon_c_01_helm","screenshot":{},"jsonequip":{"agi":578,"agiint":578,"appearances":{"0":[677325,""]},"armor":702,"displayid":677325,"int":578,"mastrtng":531,"reqlevel":68,"sellprice":522435,"slotbak":1,"sta":867,"versatility":314},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221164":{"name_enus":"Archaic Venomancer's Footwraps","quality":3,"icon":"inv_pant_cloth_earthendungeon_c_01","screenshot":{},"jsonequip":{"appearances":{"0":[677295,""]},"armor":440,"critstrkrtng":295,"displayid":677295,"hastertng":550,"int":578,"reqlevel":68,"sellprice":633682,"slotbak":7,"sta":867},"attainable":0,"flags2":8192,"displayName":"","qualityTier":0},"221165":{"name_enus":"Unceremonious Bloodletter","quality":3,"icon":"inv_knife_1h_earthendungeon_c_01","screenshot":{},"jsonequip":{"appearances":{"0":[677252,""]},"critstrkrtng":157,"displayid":677252,"dmgmax1":369,"dmgmin1":221,"dmgrange":0.5,"dmgtype1":0,"dps":164.07,"hastertng":266,"int":1683,"mledmgmax":369,"mledmgmin":221,"mledps":164.07,"mlespeed":1.8,"reqlevel":68,"sellprice":908687,"sheathtype":3,"slotbak":13,"speed":1.8,"sta":433},"attainable":0,"flags2":8712,"displayName":"","qualityTier":0}});
WH.Gatherer.addData(10, 1, {"20586":{"name_enus":"Keystone Hero: Ara-Kara, City of Echoes","icon":"inv_achievement_dungeon_arak-ara"},"40370":{"name_enus":"Ara-Kara, City of Echoes","icon":"inv_achievement_dungeon_arak-ara"},"40374":{"name_enus":"Heroic: Ara-Kara, City of Echoes","icon":"inv_achievement_dungeon_arak-ara"},"40375":{"name_enus":"Mythic: Ara-Kara, City of Echoes","icon":"inv_achievement_dungeon_arak-ara"}});
var tabsRelated = new Tabs({parent: WH.ge('jkbfksdbl4'), trackable: "WoW Zone"});
new Listview({template: 'item', id: 'drops', name: WH.TERMS.drops, tabs: tabsRelated, parent: 'lkljbjkb574', computeDataFunc: Listview.funcBox.initLootTable, onAfterCreate: Listview.funcBox.addModeIndicator, data:[{"armor":0,"bonustrees":[4341],"classs":4,"displayName":"Ara-Kara Sacbrood","flags2":8192,"id":219314,"level":437,"name":"Ara-Kara Sacbrood","quality":3,"reqlevel":68,"slot":12,"slotbak":12,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"subclass":-4,"modes":{"mode":[1,2,8,23]}},{"armor":0,"bonustrees":[4341],"classs":4,"displayName":"Ceaseless Swarmgland","flags2":8192,"id":219316,"level":437,"name":"Ceaseless Swarmgland","quality":3,"reqlevel":68,"slot":12,"slotbak":12,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[103,255,577,260,1448,581,268,1456,104,1447,253,261,254,1450,70,269,259,1453,263,1444,250,251,252,1455,1451,66,71,72,1446,73],"subclass":-4,"modes":{"mode":[1,2,8,23]}},{"armor":0,"bonustrees":[4341],"classs":4,"displayName":"Harvester's Edict","flags2":8192,"id":219317,"level":437,"name":"Harvester's Edict","quality":3,"reqlevel":68,"slot":12,"slotbak":12,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[261,254,62,1449,102,1447,105,255,577,63,64,270,262,1450,65,1451,256,257,1452,258,264,1444,265,266,267,1454,1465,1467,1468,1473,268,1456,581,103,104,253,260,1448,269,259,1453,263],"subclass":-4,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677173,""]},"bonustrees":[4341],"classs":2,"displayName":"Arachnoid Soulcleaver","displayid":677173,"dps":164.26,"flags2":8712,"id":221150,"level":437,"name":"Arachnoid Soulcleaver","quality":3,"reqlevel":68,"slot":13,"slotbak":13,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[62,63,1451,64,270,266,65,265,267,1454,1465,1467,1468,1473],"speed":2.6,"subclass":7,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[678781,""]},"armor":1198,"bonustrees":[4341],"classs":4,"displayName":"Devourer's Gauntlets","displayid":678781,"flags2":8192,"id":221151,"level":437,"name":"Devourer's Gauntlets","quality":3,"reqlevel":68,"slot":10,"slotbak":10,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[65,1451,66,250,251,1455,252,70,71,72,1446,73],"subclass":4,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[678869,""]},"armor":876,"bonustrees":[4341],"classs":4,"displayName":"Silksteel Striders","displayid":678869,"flags2":8192,"id":221152,"level":437,"name":"Silksteel Striders","quality":3,"reqlevel":68,"slot":8,"slotbak":8,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[253,262,1468,1444,264,1473,1465,1467,1448,254,255,263],"subclass":3,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677329,""]},"armor":756,"bonustrees":[4341],"classs":4,"displayName":"Gauzewoven Legguards","displayid":677329,"flags2":8192,"id":221153,"level":437,"name":"Gauzewoven Legguards","quality":3,"reqlevel":68,"slot":7,"slotbak":7,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[102,1447,105,270,1450,103,577,581,268,1456,104,269,259,1453,260,261],"subclass":2,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[678872,""]},"armor":252,"bonustrees":[4341],"classs":4,"displayName":"Swarmcaller's Shroud","displayid":678872,"flags2":8192,"id":221154,"level":437,"name":"Swarmcaller's Shroud","quality":3,"reqlevel":68,"slot":16,"slotbak":16,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[261,254,62,1449,102,1447,105,255,577,63,64,270,262,1450,65,1451,256,250,257,1452,73,258,264,1444,66,265,1446,266,267,1454,1465,1467,1468,1473,268,1456,581,103,104,253,260,1448,70,269,259,1453,263,251,252,1455,71,72],"subclass":-6,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[678775,""]},"armor":1437,"bonustrees":[4341],"classs":4,"displayName":"Swarm Monarch's Spaulders","displayid":678775,"flags2":8192,"id":221155,"level":437,"name":"Swarm Monarch's Spaulders","quality":3,"reqlevel":68,"slot":3,"slotbak":3,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[65,1451,66,250,251,1455,252,70,71,72,1446,73],"subclass":4,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[678864,""]},"armor":1035,"bonustrees":[4341],"classs":4,"displayName":"Cryptbound Headpiece","displayid":678864,"flags2":8192,"id":221156,"level":437,"name":"Cryptbound Headpiece","quality":3,"reqlevel":68,"slot":1,"slotbak":1,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[253,262,1468,1444,264,1473,1465,1467,1448,254,255,263],"subclass":3,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677331,""]},"armor":378,"bonustrees":[4341],"classs":4,"displayName":"Unbreakable Beetlebane Bindings","displayid":677331,"flags2":8192,"id":221157,"level":437,"name":"Unbreakable Beetlebane Bindings","quality":3,"reqlevel":68,"slot":9,"slotbak":9,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[102,1447,105,270,1450,103,577,581,268,1456,104,269,259,1453,260,261],"subclass":2,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677294,""]},"armor":283,"bonustrees":[4341],"classs":4,"displayName":"Burrower's Cinch","displayid":677294,"flags2":8192,"id":221158,"level":437,"name":"Burrower's Cinch","quality":3,"reqlevel":68,"slot":6,"slotbak":6,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[62,1449,1452,256,63,64,265,257,258,266,267,1454],"subclass":1,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677127,""]},"bonustrees":[4341],"classs":2,"displayName":"Harvester's Interdiction","displayid":677127,"dps":434.83,"flags2":8192,"id":221159,"level":437,"name":"Harvester's Interdiction","quality":3,"reqlevel":68,"slot":17,"slotbak":17,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[255,103,104,1447,268,269],"speed":3.6,"subclass":10,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677184,""]},"bonustrees":[4341],"classs":2,"displayName":"Blight Hunter's Scalpelglaive","displayid":677184,"dps":328.4,"flags2":8192,"id":221160,"level":437,"name":"Blight Hunter's Scalpelglaive","quality":3,"reqlevel":68,"slot":13,"slotbak":13,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[577,581,1456],"speed":2.6,"subclass":9,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[678776,""]},"armor":1917,"bonustrees":[4341],"classs":4,"displayName":"Experimental Goresilk Chestguard","displayid":678776,"flags2":8192,"id":221161,"level":437,"name":"Experimental Goresilk Chestguard","quality":3,"reqlevel":68,"slot":5,"slotbak":5,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[65,1451,66,250,251,1455,252,70,71,72,1446,73],"subclass":4,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[678871,""]},"armor":796,"bonustrees":[4341],"classs":4,"displayName":"Claws of Tainted Ichor","displayid":678871,"flags2":8192,"id":221162,"level":437,"name":"Claws of Tainted Ichor","quality":3,"reqlevel":68,"slot":10,"slotbak":10,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[253,262,1468,1444,264,1473,1465,1467,1448,254,255,263],"subclass":3,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677325,""]},"armor":702,"bonustrees":[4341],"classs":4,"displayName":"Whispering Mask","displayid":677325,"flags2":8192,"id":221163,"level":437,"name":"Whispering Mask","quality":3,"reqlevel":68,"slot":1,"slotbak":1,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[102,1447,105,270,1450,103,577,581,268,1456,104,269,259,1453,260,261],"subclass":2,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677295,""]},"armor":440,"bonustrees":[4341],"classs":4,"displayName":"Archaic Venomancer's Footwraps","displayid":677295,"flags2":8192,"id":221164,"level":437,"name":"Archaic Venomancer's Footwraps","quality":3,"reqlevel":68,"slot":7,"slotbak":7,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[62,1449,1452,256,63,64,265,257,258,266,267,1454],"subclass":1,"modes":{"mode":[1,2,8,23]}},{"appearances":{"0":[677252,""]},"bonustrees":[4341],"classs":2,"displayName":"Unceremonious Bloodletter","displayid":677252,"dps":164.07,"flags2":8712,"id":221165,"level":437,"name":"Unceremonious Bloodletter","quality":3,"reqlevel":68,"slot":13,"slotbak":13,"source":[2],"sourcemore":[{"bd":1,"z":15093}],"specs":[62,102,258,105,256,63,64,257,262,264,265,266,267,1454,1465,1467,1468,1473],"speed":1.8,"subclass":15,"modes":{"mode":[1,2,8,23]}}]});
new Listview({template: 'npc', id: 'npcs', name: WH.TERMS.npcs, tabs: tabsRelated, parent: 'lkljbjkb574', note: "<a href=\"\/npcs?filter=6;15093;0\">Filter these results<\/a>", data: [{"boss":1,"classification":1,"displayName":"Avanoxx","displayNames":["Avanoxx"],"id":213179,"location":[15093],"name":"Avanoxx","names":["Avanoxx"],"type":1},{"boss":1,"classification":1,"displayName":"Anub'zekt","displayNames":["Anub'zekt"],"id":215405,"location":[15093],"name":"Anub'zekt","names":["Anub'zekt"],"tag":"Swarmguard","type":7},{"boss":1,"classification":1,"displayName":"Ki'katal the Harvester","displayNames":["Ki'katal the Harvester"],"id":215407,"location":[15093],"name":"Ki'katal the Harvester","names":["Ki'katal the Harvester"],"type":7},{"classification":0,"displayName":"Starved Crawler","displayNames":["Starved Crawler"],"id":218961,"location":[15093],"name":"Starved Crawler","names":["Starved Crawler"],"type":1},{"classification":1,"displayName":"Bloodstained Webmage","displayNames":["Bloodstained Webmage"],"id":223253,"location":[15093],"name":"Bloodstained Webmage","names":["Bloodstained Webmage"],"type":7}]});
new Listview({template: 'achievement', id: 'achievements', name: WH.TERMS.achievements, tabs: tabsRelated, parent: 'lkljbjkb574', visibleCols: ['category'], data: [{"category":15272,"description":"Complete Ara-Kara, City of Echoes at Mythic Level 10 or higher, within the time limit.","id":20586,"name":"Keystone Hero: Ara-Kara, City of Echoes","parentcat":81,"points":0,"reward":"Max Level Unlock: Teleport to Ara-Kara, City of Echoes","side":3,"type":1,"zone":15093},{"category":15524,"description":"Defeat Ki'katal the Harvester in Ara-Kara, City of Echoes.","id":40370,"name":"Ara-Kara, City of Echoes","parentcat":168,"points":10,"side":3,"type":1,"zone":15093},{"category":15524,"description":"Defeat Ki'katal the Harvester in Ara-Kara, City of Echoes on Heroic difficulty or higher.","id":40374,"name":"Heroic: Ara-Kara, City of Echoes","parentcat":168,"points":10,"side":3,"type":1,"zone":15093},{"category":15524,"description":"Defeat Ki'katal the Harvester in Ara-Kara, City of Echoes on Mythic or Mythic Keystone difficulty.","id":40375,"name":"Mythic: Ara-Kara, City of Echoes","parentcat":168,"points":10,"side":3,"type":1,"zone":15093}]});
</script>
"""

# Extract the JSON data from the script tag
json_data = re.search(r'WH\.Gatherer\.addData\(3, 1, (\{.*?\})\);', html, re.DOTALL).group(1)  #type: ignore [union-attr]

# Parse the JSON data using ast.literal_eval
items_data = ast.literal_eval(json_data)

class Item:
    def __init__(self, item_id, data):
        self.id = item_id
        self.name = data.get('name_enus', '')
        self.quality = data.get('quality', 0)
        self.icon = data.get('icon', '')
        self.screenshot = data.get('screenshot', {})
        self.jsonequip = data.get('jsonequip', {})
        self.attainable = data.get('attainable', 0)
        self.flags2 = data.get('flags2', 0)
        self.display_name = data.get('displayName', '')
        self.quality_tier = data.get('qualityTier', 0)

        # Extracting jsonequip fields
        self.hastertng = self.jsonequip.get('hastertng', 0)
        self.reqlevel = self.jsonequip.get('reqlevel', 0)
        self.sellprice = self.jsonequip.get('sellprice', 0)
        self.slotbak = self.jsonequip.get('slotbak', 0)
        self.agi = self.jsonequip.get('agi', 0)
        self.agistr = self.jsonequip.get('agistr', 0)
        self.str = self.jsonequip.get('str', 0)
        self.int = self.jsonequip.get('int', 0)
        self.agiint = self.jsonequip.get('agiint', 0)
        self.appearances = self.jsonequip.get('appearances', {})
        self.armor = self.jsonequip.get('armor', 0)
        self.critstrkrtng = self.jsonequip.get('critstrkrtng', 0)
        self.displayid = self.jsonequip.get('displayid', 0)
        self.dmgmax1 = self.jsonequip.get('dmgmax1', 0)
        self.dmgmin1 = self.jsonequip.get('dmgmin1', 0)
        self.dmgrange = self.jsonequip.get('dmgrange', 0)
        self.dmgtype1 = self.jsonequip.get('dmgtype1', 0)
        self.dps = self.jsonequip.get('dps', 0)
        self.mledmgmax = self.jsonequip.get('mledmgmax', 0)
        self.mledmgmin = self.jsonequip.get('mledmgmin', 0)
        self.mledps = self.jsonequip.get('mledps', 0)
        self.mlespeed = self.jsonequip.get('mlespeed', 0)
        self.sheathtype = self.jsonequip.get('sheathtype', 0)
        self.speed = self.jsonequip.get('speed', 0)
        self.sta = self.jsonequip.get('sta', 0)
        self.versatility = self.jsonequip.get('versatility', 0)
        self.masstrtng = self.jsonequip.get('mastrtng', 0)
        self.agistrint = self.jsonequip.get('agistrint', 0)

# Create Item objects
items = []
for item_id, item_data in items_data.items():
    item = Item(item_id, item_data)
    items.append(item)

# Print some information about the items
""" for item in items:
    print(f"Item ID: {item.id}")
    print(f"Name: {item.name}")
    print(f"Quality: {item.quality}")
    print(f"Icon: {item.icon}")
    print(f"Required Level: {item.reqlevel}")
    print(f"Sell Price: {item.sellprice}")
    print(f"Slot: {item.slotbak}")
    print(f"Agility: {item.agi}")
    print(f"Strength: {item.str}")
    print(f"Intellect: {item.int}")
    print(f"Stamina: {item.sta}")
    print(f"Versatility: {item.versatility}")
    print(f"Mastery Rating: {item.masstrtng}")
    print(f"Critical Strike Rating: {item.critstrkrtng}")
    print(f"Display ID: {item.displayid}")
    print(f"Damage Max: {item.dmgmax1}")
    print(f"Damage Min: {item.dmgmin1}")
    print(f"DPS: {item.dps}")
    print(f"Speed: {item.speed}")
    print(f"Armor: {item.armor}")
    print(f"Appearances: {item.appearances}")
    print("---") """

# Function to recursively print nested dictionaries
def print_nested_dict(d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            print(' ' * indent + f"{key}:")
            print_nested_dict(value, indent + 2)
        else:
            print(' ' * indent + f"{key}: {value}")

# Print all information about the items
for item in items:
    print(f"Item ID: {item.id}")
    for key, value in item.__dict__.items():
        if isinstance(value, dict):
            print(f"{key}:")
            print_nested_dict(value, 2)
        else:
            print(f"{key}: {value}")
    print("---")
