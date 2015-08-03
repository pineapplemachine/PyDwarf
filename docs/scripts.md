# Scripts

## dragondeplatino.gemset.art

Created by DragonDePlatino and Sophie Kirschner.

 Writes miscelleneous image files to data/art/. 

#### Arguments:

* **variety:** Which tileset to use. Should be either '24x24' or '48x48'.

## dragondeplatino.gemset.font

Created by DragonDePlatino and Sophie Kirschner.

 Puts the appropriate curses and map files in their appropriate places, and modifies settings in data/init/init.txt such that the new graphics will be loaded. 

#### Arguments:

* **variety:** Which tileset to use. Should be either '24x24' or '48x48'.

## dragondeplatino.gemset.full

Created by DragonDePlatino and Sophie Kirschner.

 Performs a full installation, and this is probably what you want to run. 

#### Arguments:

* **properties:** File path to indicate where to find the json outputted by the gemsetproperties.py utility script.

* **variety:** Which tileset to use. Should be either '24x24' or '48x48'.

## dragondeplatino.gemset.graphics

Created by DragonDePlatino and Sophie Kirschner.

 Writes a number of image and raws files to raw/graphics/. 

#### Arguments:

* **remove_example:** Whether to remove DF's example graphics file raw/graphics/graphics_example.txt.

* **variety:** Which tileset to use. Should be either '24x24' or '48x48'.

## dragondeplatino.gemset.hack

Created by DragonDePlatino and Sophie Kirschner.

 Adds multilevel commands to DFHack's raw/onLoad.init. 

## dragondeplatino.gemset.objects

Created by DragonDePlatino and Sophie Kirschner.

 In the raws, sets the tiles and colors for creatures, inorganics, and some plants. 

#### Arguments:

* **properties:** File path to indicate where to find the json outputted by the gemsetproperties.py utility script.

## dragondeplatino.gemset.overrides

Created by DragonDePlatino and Sophie Kirschner.

 Handles TWBT files: An overrides.txt file is placed in data/init/ and the pertinent image files are placed in `data/art/`. 

#### Arguments:

* **variety:** Which tileset to use. Should be either '24x24' or '48x48'.

## mynamespace.myscript

Created by Yours Truly.

Remove all tokens of a certain kind, [AQUIFER] tokens by default.

#### Arguments:

* **token:** The kind of token to remove.

## omniclasm.decay.deteriorate.clothes

Created by Omniclasm and Sophie Kirschner.

This script is fairly straight forward. All of those slightly worn wool shoes that dwarves scatter all over the place will deteriorate at a greatly increased rate, and eventually just crumble into nothing. As warm and fuzzy as a dining room full of used socks makes your dwarves feel, your FPS does not like it. 

#### Arguments:

* **auto_run:** If set to True then the script will be started automatically upon startup.

## omniclasm.decay.deteriorate.corpses

Created by Omniclasm and Sophie Kirschner.

In long running forts, especially evil biomes, you end up with a lot of toes, teeth, fingers, and limbs scattered all over the place. Various corpses from various sieges, stray kitten corpses, probably some heads. This script causes all of those to rot away into nothing after several months. 

#### Arguments:

* **auto_run:** If set to True then the script will be started automatically upon startup.

## omniclasm.decay.deteriorate.food

Created by Omniclasm and Sophie Kirschner.

With this script running, all food and plants wear out and disappear after several months. Barrels and stockpiles will keep them from rotting, but it won't keep them from decaying. 

#### Arguments:

* **auto_run:** If set to True then the script will be started automatically upon startup.

## omniclasm.decay.starvingdead

Created by Omniclasm and Sophie Kirschner.

With this script running, all undead that have been on the map for a time (default: 1 month) start to gradually decay, losing strength, speed, and toughness. After they have been on the map for even longer (default: 3 months), they collapse upon themselves, never to be reanimated. 

#### Arguments:

* **start:** Number of months before decay sets in.

* **die:** Number of months before collapsing entirely.

* **auto_run:** If set to True then the script will be started automatically upon startup.

## pineapple.adoptsowner

Created by Sophie Kirschner.

ADOPTS_OWNER tokens are added to or removed from creatures.

#### Arguments:

* **add_to:** If set to None, no ADOPTS_OWNER tokens are added. If set to '\*', tokens are added to all creatures. If set to an iterable containing IDs of creatures, ADOPTS_OWNER will be added to each of those creatures. Defaults to None.

* **remove_from:** If set to None, no ADOPTS_OWNER tokens are removed. If set to '\*', all ADOPTS_OWNER tokens are removed. If set to an iterable containing IDs of creatures, ADOPTS_OWNER will be removed from each of those creatures. Defaults to '\*'.

## pineapple.bauxitetoaluminum

Created by Sophie Kirschner.

Adds a reaction to the smelter to allow the creation of aluminum bars from bauxite (as ore) and cryolite (as flux). Credit to this forum discussion for the reaction and general inspiration: http://www.bay12forums.com/smf/index.php?topic=31523.0

#### Arguments:

* **entities:** Adds the reaction to these entities. Defaults to only MOUNTAIN.

* **aluminum_value:** Multiplies the MATERIAL_VALUE of aluminum by this much. Defaults to 0.75 to account for the increased availability of aluminum as a consequence of the new reaction.

* **add_to_file:** Adds the reaction to this file.

## pineapple.boneflux

Created by Sophie Kirschner.

Adds a reaction to the kiln which consumes bones and produces flux. Inspired by/stolen from Rubble's Bone Flux mod.

#### Arguments:

* **reaction_name:** The name of the reaction to be shown in the kiln.

* **entities:** Adds the reaction to these entities. Defaults to MOUNTAIN and PLAINS.

* **add_to_file:** Adds the reaction to this file.

* **bone_count:** The number of bones required in the reaction.

* **product_id:** ID of the boulder to get out of the reaction. Defaults to CALCITE.

## pineapple.butcherinorganic

Created by Sophie Kirschner.

Allows butchering of some inorganics, get things like wood or stone from some corpses. Inspired by/stolen from Igfig's Modest Mod.

#### Arguments:

* **templates:** Associates material template names as keys with items as values. Each named template will be given a BUTCHER_SPECIAL:ITEM:NONE token, where ITEM is the value given. Defaults to adding logs, bars, and boulders to wood, metal, and stone templates respectively.

## pineapple.castanvil

Created by Sophie Kirschner.

Adds a reaction to the smelter which makes it possible to create an iron anvil without already having a forge. Inspired by/stolen from Rubble's Cast Anvil mod.

#### Arguments:

* **entities:** Adds the reaction to these entities. Defaults to only MOUNTAIN.

* **add_to_file:** Adds the reaction to this file.

* **anvil_cost:** The cost in iron bars to create an anvil in this way. Defaults to 5.

## pineapple.cavegrass

Created by Sophie Kirschner.

Changes the grasses in each cavern level to make the different levels more visually distinct, as well as adding a much greater variety. With default arguments the first cavern will be primarly green and yellow, the second blue and cyan, the third red and gray. Inspired by/stolen from Rubble's Cave Color mod.

#### Arguments:

* **grasses:** A dictionary specifying which grasses to change and modify. See the default_grasses dict for documentation.

## pineapple.deerappear

Created by Sophie Kirschner.

Changes the appearance of each deer from a brown D to yellow d.

#### Arguments:

* **tile:** Set the tile that the deer's appeance will be set to.

* **color:** Set the arguments that the deer's color token will be given.

* **creature:** Change the creature whose appearance will be modified. (Heresy!)

## pineapple.diff

Created by Sophie Kirschner.

Merges and applies changes made to some modded raws via diff checking. Should be reasonably smart about automatic conflict resolution but if it complains then I recommend giving things a manual checkover afterwards. Also, the token-based diff'ing approach should work much better than any line-based diff. Using this tool to apply mods made to other versions of Dwarf Fortress probably won't work so well.

#### Arguments:

* **paths:** Should be an iterable containing paths to individual raws files or to directories containing many. Files that do not yet exist in the raws will be added anew. Files that do exist will be compared to the current raws and the according additions/removals will be made. At least one path must be given.

## pineapple.discipline

Created by Sophie Kirschner.

Applies natural discipline skill bonuses to creatures that should probably have them. Credit to Mictlantecuhtli for creating the mod which inspired this one. www.bay12forums.com/smf/index.php?topic=140460.0

#### Arguments:

* **discipline_bonus:** A dict mapping property names to values: For each of these tokens that a creature possesses the corresponding bonuses are summed. The resulting value, rounded up, is used to determine the skill bonus.

* **entity_bonus:** Handled separately, adds this value to the bonus for creatures which are listed as being members of any entity.

* **badger_bonus:** Also handled separately, adds this skill bonus to badgers.

## pineapple.easypatch

Created by Sophie Kirschner.

Given a path to a file, a directory, a content string, a tokenlist, a raws file object, or an iterable containing a combination of these, a file or files are added to the dir object, and these same objects can be permitted using the permitted_entities argument.

#### Arguments:

* **files:** The file or files to be added.

* **\*\*kwargs:** Passed on to pineapple.utils.permitobjects.

## pineapple.flybears

Created by Sophie Kirschner.

Example script which causes all female bears to fly.

## pineapple.greensteel

Created by Sophie Kirschner.

Adds an alloy which is lighter and sharper than steel but not so much as adamantine. It can be made from similar ingredients as steel with the addition of adamantine bars or a new adamant ore.

#### Arguments:

* **entities:** The entities which should be permitted this reaction. Defaults to only MOUNTAIN.

## pineapple.maxage

Created by Sophie Kirschner.

Applies a MAXAGE to most vanilla creatures which don't already have one.

#### Arguments:

* **output_needs_age:** When True, creatures that have no MAXAGE and aren't specified in the ages dict will be outputted to the log. Can maybe be helpful for debugging things.

* **apply_default_age:** Most creatures that don't have a MAXAGE and aren't specified in the ages dict will have this default applied to their MAXAGE. It should be an iterable containing arguments same as values in the ages dict. This will not be applied to wagons, to megabeasts, to undead, or to nonexistent creatures.

* **ages:** A dictionary mapping creature names as keys to what that creature's arguments should be for MAXAGE: That is, it should look like (minimum_lifespan, maximum_lifespan).

## pineapple.metalitems

Created by Sophie Kirschner.

Allows the forging of every type of metal item from the specified metals.

#### Arguments:

* **items:** These are the items that the listed metals will always be allowed for.

* **metals:** These metals will be made to allow forging of each item specified.

## pineapple.noanimalmen

Created by Sophie Kirschner.

 Removes all creatures which either have a [APPLY_CREATURE_VARIATION:ANIMAL_PERSON] token or have an ID ending in '_MAN'. 

## pineapple.noaquifers

Created by Sophie Kirschner.

Removes all AQUIFER tokens.

## pineapple.noexotic

Created by Sophie Kirschner.

Replaces all [PET_EXOTIC] and [MOUNT_EXOTIC] tags with their non-exotic counterparts.

## pineapple.nogiantanimals

Created by Sophie Kirschner.

 Removes all creatures which either have a [APPLY_CREATURE_VARIATION:GIANT] token or have an ID matching a few patterns which involve the word 'GIANT' or 'GIGANTIC'. 

## pineapple.nograzers

Created by Sophie Kirschner.

Removes all [GRAZER] and [STANDARD_GRAZER] tokens.

## pineapple.nomaxage

Created by Sophie Kirschner.

Removes MAXAGE tokens from creatures.

#### Arguments:

* **apply_to_creatures:** Also removes MAXAGE from these creatures regardless of whether they possess any of the properties in required_property. Set to None to apply to no other creatures. Defaults to None.

* **required_property:** An iterable containing token values, e.g. ('INTELLIGENT', 'CAN_LEARN'): for each creature having both a MAXAGE token and one or more of these tokens, that creature's MAXAGE token will be removed. If set to None, then no MAXAGE tokens will be removed in this way. If set to ['\*'], MAXAGE tokens will be removed from all creatures.

## pineapple.orientation

Created by Sophie Kirschner.

Causes all creatures of some type to have a single sexuality, heterosexual being the default. (You boring snob!)

#### Arguments:

* **mode:** Accepts one of these strings as its value, or None: "hetero", the default, makes the creatures exclusively straight. "gay" makes the creatures exclusively gay. "bi" makes the creatures exclusively bisexual. "ace" makes the creatures exclusively asexual. Can alternatively be set as a custom tuple same as those found in the mode_info dict: The list/tuple should contain six values corresponding to (disinterest in the same gender, romantic (but not marriage) interest in the same, commitment to the same, disinterest in the other gender, romantic interest in the other, commitment to the other).

* **creatures:** An iterable containing creatures whose sexuality should be affected. Set to None to affect all creatures.

## pineapple.sanitize.nonexistentids

Created by Sophie Kirschner.

 Checks for and removes any instances where a COPY_TAGS_FROM or similar token refers to an ID that doesn't exist. 

## pineapple.skillrust

Created by Sophie Kirschner.

Modifies skill rust for given creatures. Disables it entirely by default.

#### Arguments:

* **rates:** What the skill rust rates are to be changed to. It must be a tuple or list containing three values. The default is ('NONE', 'NONE', 'NONE'), which disables skill rust entirely. Dwarf Fortress's default rates are ('8', '16', '16'). Lower numbers indicate faster skill rust.

* **creatures:** An iterable containing creatures for which to disable skill rust.

## pineapple.stoneclarity

Created by Sophie Kirschner.

Allows powerful editing of the appearances of stone, ore, and gems.

#### Arguments:

* **rules:** By default makes all flux stone white, makes all fuel use \*, makes all ore use £ unmined and \* in stockpiles, makes cobaltite use % unmined and • in stockpiles, makes all gems use ☼. Specify an object other than default_rules to customize behavior, and refer to default_rules as an example of how rules are expected to be represented

* **query:** This query is run for each inorganic found and looks for tokens that should be recognized as indicators that some inorganic belongs to some group. Refer to the default query for more information.

* **fuels:** If left unspecified, stoneclarity will attempt to automatically detect which inorganics are fuels. If you know that no prior script added new inorganics which can be made into coke then you can cut down a on execution time by setting fuels to fuels_vanilla.

## pineapple.subplants

Created by Sophie Kirschner.

Makes all subterranean plants grow year-round.

## pineapple.useablemats

Created by Sophie Kirschner.

Causes scales, feathers, and chitin to become useful for crafting. Inspired by/stolen from Rubble's Usable Scale/Feathers/Chitin fixes.

#### Arguments:

* **scales:** Recognized when using the default options dict. If set to True, scales will be made to act more like leather for crafting purposes.

* **feathers:** Recognized when using the default options dict. If set to True, feathers will be useable for making soft items, such as clothing.

* **options:** A dictionary associating option names with tuples where the first element is the name of a MATERIAL_TEMPLATE and the second is tokens to be added to that template. Option names, when passed as a keyword argument and set to False, will cause that option to be disabled.

* **chitin:** Recognized when using the default options dict. If set to True, chitin will be made to act more like shells for crafting purposes.

## pineapple.utils.addhack

Created by Sophie Kirschner.

Utility script for adding a new DFHack script.

#### Arguments:

* **onload:** If set to True then the auto_run line will be added to raw/onLoad.init.

* **\*\*kwargs:** Other named arguments will be passed on to the dir.add method used to create the file object corresponding to the added script.

* **startup:** If set to True then the auto_run line will be added to dfhack.init.

* **auto_run:** If set to True, a line will be added to dfhack.init containing only the name of the added script. If set to None, no such line will be added. If set to an arbitrary string, that string will be added as a new line at the end of dfhack.init.

## pineapple.utils.addobject

Created by Sophie Kirschner.

Utility script for adding a new object to the raws.

#### Arguments:

* **item_rarity:** Most items, when adding tokens to entities to permit them, accept an optional second argument specifying rarity. It should be one of 'RARE', 'UNCOMMON', 'COMMON', or 'FORCED'. This argument can be used to set that rarity.

* **add_to_file:** The name of the file to add the object to. If it doesn't exist already then the file is created anew. The string is formatted such that %(type)s is replaced with the object_header, lower case.

* **permit_entities:** For relevant object types such as reactions, buildings, and items, if permit_entities is specified then tokens are added to those entities to permit the added object.

* **tokens:** The tokens belonging to the object to create.

* **object_header:** When the object is added to a file which doesn't already exist, an [OBJECT:TYPE] token must be added at its beginning. This argument, if specified, provides the type in that token. Otherwise, when the argument is left set to None, the type will be automatically decided.

* **type:** Specifies the object type. If type and id are left unspecified, the first token of the tokens argument is assumed to be the object's [TYPE:ID] token and the type and id arguments are taken out of that.

* **id:** Specifies the object id. If type and id are left unspecified, the first token of the tokens argument is assumed to be the object's [TYPE:ID] token and the type and id arguments are taken out of that.

## pineapple.utils.addobjects

Created by Sophie Kirschner.

Utility script for adding several new objects to the raws at once.

#### Arguments:

* **\*\*kwargs:** Passed on to pineapple.utils.addobject.

* **add_to_file:** The name of the file to add the object to. If it doesn't exist already then the file is created anew. The string is formatted such that %(type)s is replaced with the object_header, lower case.

* **objects:** An iterable containing tokens belonging to the objects to add.

## pineapple.utils.addtoentity

Created by Sophie Kirschner.

A simple utility script which adds tokens to entities.

#### Arguments:

* **tokens:** A string or collection of tokens to add to each entity.

* **entities:** Adds tokens to these entities.

## pineapple.utils.objecttokens

Created by Sophie Kirschner.

Utility script for adding or removing tokens from objects.

#### Arguments:

* **add_to:** If set to None, no tokens tokens are added. If set to '\*', tokens are added to all objects. If set to an iterable containing IDs of objects, tokens will be added to each of those objects.

* **token:** The token to be added or removed.

* **object_type:** The type of object which should be affected.

* **remove_from:** If set to None, no matching tokens are removed. If set to '\*', all matching tokens are removed. If set to an iterable containing IDs of objects, matching tokens will be removed from each of those objects.

## pineapple.utils.permitobject

Created by Sophie Kirschner.

Utility script for permitting an object with entities.

#### Arguments:

* **permit_entities:** For relevant object types such as reactions, buildings, and items, if permit_entities is specified then tokens are added to those entities to permit the added object.

* **type:** Specifies the object type.

* **item_rarity:** Some items, when adding tokens to entities to permit them, accept an optional second argument specifying rarity. It should be one of 'RARE', 'UNCOMMON', 'COMMON', or 'FORCED'. This argument can be used to set that rarity.

* **id:** Specifies the object id.

## pineapple.utils.permitobjects

Created by Sophie Kirschner.

Utility script for permitting several objects at once with entities.

#### Arguments:

* **\*\*kwargs:** Passed on to pineapple.utils.permitobject.

* **objects:** An iterable containing either tokens or type, id tuples representing objects to be permitted.

## pineapple.woodmechanisms

Created by Sophie Kirschner.

Allows construction of wooden mechanisms at the craftdwarf's workshop. Inspired by/stolen from Rubble's Wooden Mechanisms mod.

#### Arguments:

* **entities:** Adds the reaction to these entities. Defaults to MOUNTAIN and PLAINS.

* **add_to_file:** Adds the reaction to this file.

* **log_count:** The number of logs required in the reaction.

## pkdawson.vegan

Created by Patrick Dawson and Sophie Kirschner.

Adds reactions to the craftdwarf's workshop for making quivers and backpacks from cloth, which normally require leather. Also adds a DFHack script which disables non-vegan labors using autolabor.

#### Arguments:

* **lua_file:** The DFHack script will be added to this path, relative to DF's root directory. If set to None then no DFHack script will be written.

* **entities:** Adds the reaction to these entities. Defaults to MOUNTAIN and PLAINS.

* **add_to_file:** Adds the reaction to this file.

* **labors:** These labors will be disabled using a DFHack script. If set to None then no DFHack script will be written. The default labors are BUTCHER, TRAPPER, DISSECT_VERMIN, LEATHER, TANNER, MAKE_CHEESE, MILK, FISH, CLEAN_FISH, DISSECT_FISH, HUNT, BONE_CARVE, SHEARER, BEEKEEPING, WAX_WORKING, GELD. 

* **auto_run:** If set to True, and if the DFHack script is added, then a line will be added to the end of dfhack.init which runs this script on startup. If set to False then the script will wait to be run manually.

## putnam.materialsplus

Created by Putnam and Sophie Kirschner.

Adds a bunch of materials to the game.

## putnam.microreduce

Created by Putnam and Sophie Kirschner.

A mod to reduce the amount of micromanagement in Dwarf Fortress. One-step soap making and clothesmaking!

## shukaro.creationforge

Created by Shukaro and Sophie Kirschner.

This is a simple workshop I modded in to help test custom reactions, buildings, and creatures. It's used to create various different items so that you don't have to set up an entire fortress to test some reactions. Hopefully it's a useful tool to people, even if it's just to look at the raw formatting.

## shukaro.higherlearning

Created by Shukaro and Sophie Kirschner.

Have you ever wondered to yourself, "Man, my dwarves are such idiots, I wish I could chisel some intelligence into their heads."? No? Then, er, disregard that last bit. What I present to you, here and now, no strings attached, is a workshop to solve a problem that you probably didn't even know you had! I call it, the Dwarven Higher Learning Mod. Now, what this thingawazzit does, is give your dwarves an opportunity to polish up some skills that they may have trouble practicing elsewhere. You know the situation, Urist McDoctor has your legendary axedwarf on your table, and he's got no idea how to stop him from bleeding out from wounds caused by rogue fluffy wamblers. Or you have precious little metal available on the glacier you so stupidly bravely embarked on, so you can't afford to waste it on dabbling weaponsmiths who've never handled a hammer before in their lives. This mod's workshops allow training through the time-honored traditions of; hitting rocks until your hands bleed, performing repetitive actions that will sap your will to live, practicing your skills on subjects that are worth less than most peasants (and won't sue for malpractice), and studying the works of your fellow dwarves, knowing full-well that you'll never be quite as good as them.

#### Arguments:

* **entities:** An iterable containing names of entities the workshops will be added to. Defaults to only MOUNTAIN.

## smeeprocket.transgender

Created by SmeepRocket and Sophie Kirschner.

Adds transgender and intersex castes to creatures.

#### Arguments:

* **beards:** If True, all dwarf castes will be given beards. If False, none of the added castes will have beards for any species. Defaults to True.

* **frequency:** Higher numbers cause rarer incidence of added castes.

* **species:** An iterable containing each species that should be given transgender and intersex castes.

## stal.armoury.attacks

Created by Stalhansch and Sophie Kirschner.

Removes attacks from creatures. By default, as a way to improve balance in combat, scratch and bite attacks are removed from dwarves, humans, and elves.

#### Arguments:

* **remove_attacks:** Removes these attacks from species listed in remove_attacks_from. Defaults to scratch and bite.

* **remove_attacks_from:** If set to True, specified remove_attacks are removed from the species in the list to improve combat balancing. If set to None those attacks will not be touched. Defaults to dwarves, humans, and elves.

## stal.armoury.items

Created by Stalhansch and Sophie Kirschner.

Attempts to improve the balance and realism of combat.

#### Arguments:

* **remove_entity_items:** Determines whether items that would be made unavailable to entities should be removed from those entities or not. If you're also using other mods that make changes to weapons and armour and such it may be desireable to set this flag to False. Otherwise, for best results, the flag should be set to True. Defaults to True

## umiman.smallthings.engraving

Created by Umiman, Fieari, and Sophie Kirschner.

Has this been done before? While I think it's impossible to change any of the inbuilt engraving stuff like, "this is a picture of a dwarf and a tentacle demon. The dwarf is embracing the tentacle demon", it is possible to edit and add to more basic ones such as "this is a picture of a crescent moon". Basically, I added maybe 100 or so new engravings you can potentially see on your floors, walls, studded armour, images, and the like. Keep in mind maybe one or two metagame just a tad but it's funny! I swear! 

## umiman.smallthings.prefstring

Created by Umiman, Fieari, and Sophie Kirschner.

This mod simply just adds to the number of prefstrings for everything in the game to a minimum of five each. Prefstrings are the stuff that tell your dwarves what to like about a creature. For example, "He likes large roaches for their ability to disgust". With this mod, you'll see more fleshed out descriptions of the things your dwarves like, as well as more varied ones. With five each, it's pretty rare to see the same two twice. Hopefully I don't have any repeating prefstrings. 

## umiman.smallthings.speech.nofamily

Created by Umiman and Sophie Kirschner.

Adds more dialog options to no_family.txt.

## umiman.smallthings.speech.threats

Created by Umiman and Sophie Kirschner.

Awhile back I asked the community to contribute to fill out the threat.txt which is used in adventurer when someone threatens you. I.E: in vanilla, when you face a megabeast or someone who has killed a named creature, they will talk about who they killed and then say, "prepare to die!!!". That's all they said. Boring. This compilation has some of the best threats (around 150 and counting) compiled from that thread and should make killing things too proud of their own achievements a lot more fun. 

## witty.restrictednobles.custom

Created by Witty and Sophie Kirschner.

Allows allowing and preventing various species from becoming dwarven nobles.

#### Arguments:

* **inclusions:** An iterable containing each species that should be specified as allowed. If any is allowed in this way, any species not specifically allowed will be disallowed.

* **exclusions:** An iterable containing each species that should be disallowed. All species not disallowed in this way will be able to become dwarven nobles.

## witty.restrictednobles.standard

Created by Witty and Sophie Kirschner.

Witty: This is a pretty simple mod I've been meaning to make for a while. This should restrict all nobles of a given dwarven civ to dwarves and only dwarves. edit: taking into consideration that non-dwarves will be functional fort citizens as of the next version, I've decided to go with another option. The newest addition will now only exclude goblins from dwarven positions, since their current worldgen behavior still makes them the most likely to dominate dwarven nobility. But now the occasional elf or human king will get their fair dues. The dwarf-only "module" will still come packaged. Note this will require a new world to take effect. All raw changes will be indicated by the WM insignia.  Sophie: By default, this script will only prevent goblins from becoming nobles. Set the onlydwarves flag to True in order to prevent all other races as well. 

#### Arguments:

* **onlydwarves:** Defaults to False. If True, only dwarves will be allowed to hold positions in Dwarven forts and civs. If False, only goblins will be prevented from holding those positions.