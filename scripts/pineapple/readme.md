# List of mods

Mods created for PyDwarf by Sophie Kirschner. (http://www.pineapplemachine.com)

## adoptsowner

With default arguments `[ADOPTS_OWNER]` tokens are removed from all creatures. The script can also be used to remove the tokens from specific creatures, or to add them instead.

## bauxitetoaluminum

Adds a reaction to get aluminum bars from bauxite and cryolite and reduces the value of aluminum to account for the increased availability.

## boneflux

Adds a reaction to the kiln which consumes bones and produces flux stone.

## butcherinorganic

Butchering creatures of inorganic composition will often yield the corresponding raw materials, such as logs or boulders or metal bars.

## castanvil

Adds a reaction which allows creating an iron anvil from bars at a smelter.

## cavegrass

Intended for adding or changing grasses in caverns. By default numerous additional grasses are added, and cave grasses are colored such that each level can be more easily distinguished by the colors of its grasses.

## deerappear

Useful for changing the tile and color of single creatures. The default arguments change the appearance of deer from a brown D to a yellow d.

## diff

Can be used to merge and apply changes made to modified raws. Attempting to apply changes made to raws belonging to differing Dwarf Fortress versions in this way may lead to errors. When the script is run it will notify the user of any conflicts so that they can be resolved manually.

## discipline

Adds discipline as a natural skill to creatures that shouldn't be running away so easily. Creatures given bonuses include civilized creatures, trainable creatures, evil creatures, megabeasts, and more.

## easypatch

Add a file or a bunch of tokens and the script handles entity permissions all on its own. Good for adding small mods, for example:

``` json
{
    "name": "pineapple.easypatch",
    "args": {
        "files": "path/to/raws",
        "loc": "raw/objects",
        "permit_entities": "MOUNTAIN"
    }
}
```

## flybears

A simple example script which adds a `[FLIER]` tag to all female vanilla bears.

## greensteel

Adds a new alloy of pig iron and adamantine, green steel, which is superior to steel but weaker than adamantine. It can also be smelted as an alloy of pig iron and a new adamant ore, which is very similar to adamantine but occurs normally (though rarely) in clusters and veins and cannot be used to create items such as weapons and armor.

## maxage

Gives `[MAXAGE]` tokens to many creatures that don't have one in the vanilla raws, but probably should.

## metalitems

Allows forging items of types using metals normally disallowed by Dwarf Fortress. For example, with the default arguments, this script will allow the forging of golden weapons and armor. (How useful that equipment would actually be is questionable, but as we all know !!fun!! doesn't ask those sorts of questions.)

## noaquifers

Removes all `[AQUIFER]` tokens.

## noexotic

Replaces all `[PET_EXOTIC]` and `[MOUNT_EXOTIC]` tokens with `[PET]` and `[MOUNT]` tokens, respectively. This will make it possible to train many animals that otherwise could not be.

## nograzers

Removes all `[GRAZER]` and `[STANDARD_GRAZER]` tokens. With this script applied animals will no longer need to be pastured where vegetation is present.

## nomaxage

Removes `[MAXAGE]` tokens from creatures. With default arguments, removes the tag from all intelligent creatures.

## orientation

For setting the orientations of some creatures to some predefined setting. Running with default settings will make all dwarves, humans, elves, and goblins exclusively heterosexual and committed to marriage.

## skillrust

Sets the skill rust rates of creatures. By default skill rust is entirely disabled for dwarves, humans, and elves.

## stoneclarity

Can be used to set the appearance of stones, ores, and gems based on customizable rules. Can be useful to make it easier to recognize the purpose of some unmined tile at a glance.

## subplants

Makes all subterranean plants grow year-round, regardless of season, by ensuring that each has all of `[SPRING]`, `[SUMMER]`, `[AUTUMN]`, and `[WINTER]` tokens.

## usablemats

With default settings it becomes possible to craft items using the normally uncooperative scale, feathers, and chitin.

## utils

### addtoentity

Utility script intended for adding things like `[PERMITTED_REACTION:ID]` to entities.

### objecttokens

Utility script which abstracts adding tokens to or removing them from objects, either all at once or given an iterable containing object IDs.

### addhack

Utility script for adding a DFHack script. It can also add a line to dfhack.init to automatically run the script when the game starts.

### addobject

Utility script adds an object and handles permitting reactions and buildings and such with entities.

### addobject

Utility script adds multiple objects using pineapple.utils.addobject.

### permitobject

Utility script adds tokens like `[PERMITTED_REACTION:ID]` to entities given an object.

### permitobjects

Utility script permits multiple objects using pineapple.utils.permitobject.

## woodmechanisms

Makes it possible to craft mechanisms from wood at a craftdwarf's workshop.
