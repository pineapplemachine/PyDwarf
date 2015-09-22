# GemSet v1.32

Colorful, sharp, and crystal-clear.

Created by DragonDePlatino. (http://www.bay12forums.com/smf/index.php?topic=150753.msg6230901#msg6230901)  
Rewritten for PyDwarf by Sophie Kirschner. (http://www.pineapplemachine.com)

## Introduction

The first complete 24x24 graphics set for Dwarf Fortress, GemSet provides the aesthetics of ASCII and convenience of graphics.

Drawn natively in a 24x24 resolution for 1080p and 4K displays, GemSet is much more crisp than its 16x16 contemporaries. The entire graphics set uses a bright 32-color palette, so everything will be crystal-clear on even the highest-resolution displays. All profession graphics are color-coded according to their ASCII counterparts and black has been kept as the dominant color of the graphics set. If you want graphics but don't want to sacrifice the aesthetics of ASCII, this is the graphics set for you.

Included in the mod are these:
* 24x24 and 48x48 versions of all creatures.
* TWBT overrides for all items and tiles. Buildings coming soon.
* A hand-drawn curses_24 and curses_48 tileset.
* A new set of raws and several BAMM! scripts for installation.
* An OnLoad.init for custom multilayer settings.

## Requirements

GemSet requires that both [DFHack](https://github.com/DFHack/dfhack/releases) and [TWBT](https://github.com/mifki/df-twbt/releases) be installed.

## PyDwarf Components

### dragondeplatino.gemset.full

Performs a full installation, and this is probably what you want to run. By default the 24x24 graphics set is installed, but this behavior can be changed by running `{"name": "dragondeplatino.gemset.full", "args": {"variety": "4x848"}}`. In this case, the 48x48 set would be installed instead. The options accepted for this argument are `24x24` and `48x48`.

### dragondeplatino.gemset.art

Writes miscelleneous image files to `data/art/`. Accepts a `variety` argument same as `dragondeplatino.gemset.full`, which also defaults to the 24x24 graphics set.

### dragondeplatino.gemset.font

Puts the appropriate curses and map files in their appropriate places, and modifies settings in `data/init/init.txt` such that the new graphics will be loaded. Also accepts a `variety` argument.

### dragondeplatino.gemset.graphics

Writes a number of image and raws files to `raw/graphics/`. Accepts the same `variety` argument.

### dragondeplatino.gemset.hack

Adds `multilevel` commands to DFHack's `raw/onLoad.init`. Doesn't need a `variety` argument.

### dragondeplatino.gemset.objects

In the raws, sets the tiles and colors for creatures, inorganics, and some plants. Also doesn't take a `variety` argument.

### dragondeplatino.gemset.twbt

Handles TWBT files: An `overrides.txt` file is placed in `data/init/` and the pertinent image files are placed in `data/art/`. Accepts a `variety` argument.

## Help Wanted

I am unable to view GemSet on my monitor without it being squished to 1600x900. [Share your 1080p and 4K screenshots, please!](http://www.bay12forums.com/smf/index.php?topic=150753.msg6230901#msg6230901)

I may be missing some overrides. Notify me if you see any strange or missing graphics.

## Donations

When I first conceived this project, I wanted to make Dwarf Fortress more accessible and bring more people into the community. It's my way of thanking the developers for everything they've done. So if you're reading this, please consider supporting Dwarf Fortress by donating to Bay 12 Games. Dwarf Fortress wouldn't have been possible without the incredible dedication of Toady One and ThreeToe.

[**Donate to Bay12 Games!**](http://www.bay12games.com/support.html)

## GemSet History

#### Version 0.99
Released on 2015-05-15.
 - Initial release.

#### Version 1.0
Released on 2015-05-15.
 - Text files added for all creatures.
 - TRAINED_HUNTER and TRAINED_WAR versions for all creatures.
 - Alpha transparency fixed on curses_square_24.png and curses_square_48.png.
 - Alpha transparency fixed on 48px graphics.

#### Version 1.1
Released on 2015-05-17.
 - Updated armor designs for all races.
 - Miscellaneous fixes to race graphics.
 - Miscellaneous fixes to creature graphics.
 - Fixed bordering issue with 48x48 tiles.
 - Fixed monarchs, champions and children displaying incorrectly.
 - Smaller icons for GIANT, TRAINED_WAR and TRAINED_HUNTER creatures.
 - Tweaked colors for ANIMATED creatures.
 - The undead have turned. *shot*

#### Version 1.2
Released on 2015-05-24.
 - TWBT overrides for all items.
 - Graphics for procedurally-generated creatures.
 - Alignment fixes and minor tweaks for the curses tileset.

#### Version 1.21
Released on 2015-05-25.
 - Color scheme altered to be less ugly.
 - Changed perspective of bed furniture.
 - Fixed the colored background of some item tiles.

#### Version 1.3
Released on 2015-06-04.
 - TWBT overrides for all tiles.
 - Finalized armor designs for all races.
 - Changed raw tiles for creatures, gems, stones, minerals, soil and grasses.
 - Changed raw colors for gems, stones, minerals, soil and grasses.
 - Unique item tiles for each stone type.
 - Included several BAMM! scripts to document raw changes.
 - Added an onLoad.init for custom multilevel settings.
 - Changed all images to RGB color to fix transparency.
 - Fixed all items that use black foregrounds like bins and barrels.
 - Fixed giant swans being displayed as giant puffins.
 - Color scheme replaced with default.
 - Fixed shading on cages.

#### Version 1.31
Released on 2015-06-04.
 - Non-varied floor tiles will display properly now.
 - Increased background transparency of constructed floor tiles.

#### Version 1.32
Released on 2015-06-12.
 - Resized text tileset from 24x24 to 16x24 and redrew many characters in both tilesets.
 - Added missing grass and shrub tiles.
 - Split soil and plant tiles into their own sheets.
 - Reworked tree trunk and interior tiles.
 - Corrected black part of constructed floor tiles.
 - Included mouse.png for ease-of-installation.

## Credits

Max™ - Text files for races.  
Button - Help with [BAMM!](http://www.bay12forums.com/smf/index.php?topic=150925.0)  
DragonDePlatino - Everything else
