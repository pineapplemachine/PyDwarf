# Introduction

Welcome to PyDwarf! This tool is currently quite early in development and so please don't be surprised if there are bugs, missing features, or if this tutorial simply lags behind.

There's a lot of stuff that PyDwarf automates and most of it is highly customizeable. The scope of this tutorial is in showing how to configure PyDwarf, how to create and register a new mod with it, to describe the tools available to you in writing that mod, and how to apply it to Dwarf Fortress's raws. If there are questions this tutorial fails to answer, answers can be found within PyDwarf's source code and documentation.

Feature requests, bugs, and generally incomprehensible behavior should be reported using the PyDwarf repository's issues page, found [here](https://github.com/pineapplemachine/PyDwarf/issues).



# Configuring PyDwarf

PyDwarf's manager needs to be told things like where to find input raws, where to output new raws to, and which scripts to run. By default, these varaiables are set only using the information in the `config.json` file located in PyDwarf's root directory and using any command line arguments passed to the script upon execution. You can exert more power over the configuration by modifying the configuration override script `override_config.py`, which should assign some dictionary to an `export` attribute. The settings assigned there will override those defined in `config.json`.

For the typical user, what this all means is essentially limited to setting the paths in their `config.json` file and adding to the list the scripts they want to run. For the advanced user, this may mean writing their own config override script that dynamically sets configuration variables. For example, my own configuration file is shared between two operating systems. So in my script I describe where my Dwarf Fortress directory is located based on which OS the script is being run for.

The scripts specified in a config object's scripts attribute (or in the scripts array of a json config file) are very flexible. There are several ways that a script can be added to this list:

* Describe the name of a specific script. For example, `flybears`. If there could be other scripts by the same name, it's important to differentiate between them by including the namespace, e.g. `pineapple.flybears`. These scripts must be within files located in the scripts/ directory in order to be made available in this way.
* Describe a namespace. For example, `pineapple.*`. This will run every script in the pineapple namespace. Namespaces can have a hierarchy: `pineapple.a.*` would run the scripts named `pineapple.a.script` and `pineapple.a.x.script` but not the scripts `pineapple.script` or `pineapple.b.script`.
* Provide a direct reference to a function or an urist object. (This only works in Python override scripts, not in `config.json`.)
* A dictionary containing various attributes to describe functionality. Attributes which will receive special handling are these:
    * `name`: The name of a script or a namespace. Understood the same way that a lone string would be.
    * `func`: Works only in Python override scripts, not in the json file: Specify a particular function to run via its reference.
    * `args`: The script or function will be run using these arguments, passed via Python's `**kwargs` functionality.
    * `match`: Urist metadata must match every attribute here. For example, `"match": {"version": "1.0"}` would match only a script which includes `version = "1.0"` in its metadata.
    * `ignore_df_version`: Normally, if the current Dwarf Fortress version given in config isn't covered by a function's `compatibility` metadata (if specified), PyDwarf will refuse to run that function. If this flag is set to `true`, e.g. `"ignore_df_version": true`, then the script(s) specified will be run regardless of their compatibility.

For convenient reference, this is an example config.json file:

``` json
{
    "input":    "E:/Sophie/Desktop/Files/Games/Dwarf Fortress/df_40_24_win/rawvanilla/objects",
    "output":   "E:/Sophie/Desktop/Files/Games/Dwarf Fortress/df_40_24_win/raw/objects",
    "backup":   "E:/Sophie/Desktop/Files/Games/Dwarf Fortress/df_40_24_win/rawbak/",
    
    "version":  "auto",
    "dfhackdir": "auto",
    "dfhackver": "auto",
    
    "scripts": [
        {"name": "pineapple.deerappear", "args": {"tile": "'d'", "color": [6, 0, 1]}},
        {"name": "pineapple.noexotic", "match": {"version": "alpha"}},
        "pineapple.nograzers",
        "putnam.materialsplus",
        "smeeprocket.transgender",
        "witty.restrictednobles"
    ],
    
    "packages": [
        "scripts"
    ]
}
```

Here is the purpose of each of those attributes:

* `input`: The directory containing inputted raws.
* `output`: Which directory to output the raws to after the scripts have run and modified them. If set to `null` (in json) or `None` (in Python) then the output directory will be the same as the input.
* `backup`: Before anything else is done, if it's not `null` or `None`, the input raws will be copied and saved to this directory.
* `version`: Specifies the Dwarf Fortress version. For example, `"version": "0.40.24"`. If set to `auto` then PyDwarf will attempt to detect the Dwarf Fortress version automatically. This should succeed as long as either the `input` or `output` directory is somewhere inside Dwarf Fortress's directory.
* `dfhackdir`: The location of a hack/ directory, if any, within the Dwarf Fortress directory
* `dfhackver`: The version of DFHack contained within a hack/ directory, if any, within the Dwarf Fortress directory
* `scripts`: Lists the scripts that should be run.
* `packages`: Lists the Python packages that should be imported. In essence, it specifies for PyDwarf that it should look for scripts inside the `scripts` package, in this case a directory containing an `__init__.py` file. This is an advanced feature and the typical user won't need to worry about this.



# Applying Mods

Once PyDwarf has been configured, applying the mods specified in its configuration is as simple as running `manager.py`. With Python 2.7 installed, the most straightforward way to do this for many users will be to open a terminal or command prompt in PyDwarf's root directory and run `python manager.py`.

PyDwarf's configuration can also be passed as command line arguments when running manager.py. These are the arguments it accepts, all of which supersede any identically-named options set in `config.json` or `config.py` when specified.

* `-i` or `--input`: Specifies raws input directory.
* `-o` or `--output`: Specifies raws output directory.
* `-b` or `--backup`: Specifies raws backup directory.
* `-ver` or `--version`: Specifies Dwarf Fortress version.
* `-hdir` or `--dfhackdir`: Specifies DFHack directory.
* `-hver` or `--dfhackver`: Specifies DFHack version.
* `-s` or `--scripts`: The list of scripts to run. (Only names and namespaces may be specified in this way, not dictionaries.)
* `-p` or `--packages`: The list of Python packages to import.
* `-c` or `--config`: Imports configuration from the json file given by the path.
* `-v` or `--verbose`: Sets the logging level for standard output to `DEBUG`. (By default, fully verbose logs are written to the `logs/` directory regardless of this flag.)
* `--log`: Specifies the log file path.
* `--list`: Lists registered scripts in alphabetical order.
* `--meta`: When given names of scripts as arguments, shows each script's metadata in a readable format. When given no arguments, metadata for all registered scripts is displayed.
* `--jscripts`: More complicated alternative to `--scripts` which accepts a json array just like the `scripts` attribute in `config.json`.
* `-h` or `--help`: Shows a summary of each argument's purpose.

![Example gif of running PyDwarf from the command line](http://www.pineapplemachine.com/pydwarf/terminal_example.gif)



# Creating a Mod

Given the default settings, scripts must be located in PyDwarf's scripts/ directory to be registered and allowed to run. They must also have a `*.py` extension and be prefixed with `pydwarf.*`. For example, the script `scripts/pineapple/pydwarf.flybears.py` is loaded because it's in the scripts/ directory and its name follows the expected pattern.

It's recommended (but not strictly necessary) that scripts be placed in directories corresponding to their authors. For example, scripts written by myself are placed in the `scripts/pineapple/` directory.

Once a Python script has been created which is located in the correct place and which follows the naming convention, at least one function should be placed in it. The first argument of the function must accept a raws.dir object and the remainder must be named arguments which, in most cases, should be assigned default values for the sake of ease-of-use. The function should be immediately preceded by a `@pydwarf.urist()` decorator. Metadata can be assigned by passing named arguments to the decorator. There is no metadata that absolutely must be specified. For example, if no name is given in the decorator, the name of the decorated function is used instead. Additionally, the line `import pydwarf` should be placed at the top of the file. Sometimes, more complex scripts may require the classes provided by PyDwarf's `raws` package. In such cases, `import raws` should be placed at the top of the file together with `import pydwarf`.

Here's an example script which, though it does nothing, would be properly understood by PyDwarf.

```python
import pydwarf

@pydwarf.urist(
    name = 'pineapple.example',
    author = 'Sophie Kirschner',
    description = 'This script doesn\'t actually do anything!'
)
def examplefunction(df):
    pass
```

For more complete documentation regarding what metadata gets special consideration, refer to documentation in `pydwarf/urist.py`.



# Experimenting with PyDwarf

It's easy to start playing around with PyDwarf's raws querying and modification functionality! Navigate a terminal to PyDwarf's directory and run `python`, then `import raws` and set `df = raws.dir(path='...')` where `...` refers to a directory like `path/to/dwarf/fortress/raw/objects`. All of PyDwarf's raws functionality will be exposed to you. Here's an example of what you can do from here:

``` bash
client-170:PyDwarf pineapple$ python
Python 2.7.8 (v2.7.8:ee879c0ffa11, Jun 29 2014, 21:07:35)
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import raws
>>> df = raws.dir(path='raw/objects')
>>> elf = df.getobj('CREATURE:ELF')
>>> description = elf.get('DESCRIPTION')
>>> print description
[DESCRIPTION:A medium-sized creature dedicated to the ruthless protection of nature.]
>>> description.setarg('A medium-sized creature undeserving of life.')
>>> print description
[DESCRIPTION:A medium-sized creature undeserving of life.]
>>> df.write(path='raw/objects')
<raws.dir.rawsdir instance at 0x10239b758>
>>> quit()
client-170:PyDwarf pineapple$ grep 'CREATURE:ELF' raw/objects/creature_standard.txt -A 4
[CREATURE:ELF]
    [DESCRIPTION:A medium-sized creature undeserving of life.]
    [NAME:elf:elves:elven]
    [CASTE_NAME:elf:elves:elven]
    [CREATURE_TILE:'e'][COLOR:3:0:0]
```



# The Modder's Toolbox

There are three very important classes provided by PyDwarf's `raws` package. They are `raws.dir`, which contains instances of `raws.file`, which itself contains instances of `raws.token`. `raws.dir` describes an entire directory of raws. `raws.file` describes a single raws file. And `raws.token` describes a single token within a raws file. (Those tokens are alternatively called "tags": They're contained within Dwarf Fortress raws and they look like, for example, `[TOKEN:ARGUMENTS]`. Each one of these possesses a number of methods that can be used to find specific tokens, and some methods used to add or remove tokens or files.

These are the methods you'll probably be using most often. For others, or for more information regarding the ones listed, look at `raws/queryable.py`. It defines significantly more, more specialized, methods than these in addition to a generalized ```query``` method upon which all other queries are built. This is where the various methods are defined and most thoroughly documented. To start getting a more comprehensive idea of the available methods and their usefulness I strongly recommend looking at the many scripts already located within the `scripts/` directory.

* `df.get`: Returns the first token matching the query. For example, `df.get('ENTITY:MOUNTAIN')` would return the `[ENTITY:MOUNTAIN]` token.
* `df.all`: Returns all tokens matching the query. For example, `df.all('PET_EXOTIC')` would return all `[PET_EXOTIC]` tokens.
* `df.until`: Returns all tokens up until the first token matching the query. For example, `df.get('ENTITY:MOUNTAIN').until('ENTITY:FOREST')` would return all tokens between `[ENTITY:MOUNTAIN]` and `[ENTITY:FOREST]`.
* `df.getobj`: Returns the first object of a given type and id. For example, `df.getobj('CREATURE:DWARF')` would return the `[CREATURE:DWARF]` token in `creature_standard`. (And never the identical token in `entity_default`!) Unlike the previous methods, this one can only be used on `raws.dir` objects.
* `df.allobj`: Returns all objects of a given type. For example, `df.allobj('ITEM_WEAPON')` would return all weapons. Like `df.getobj`, this method can only be used on `raws.dir` objects.
* `df.add`: Adds a new token or tokens after the `raws.token` this method is called for or, in the case of a `raws.file` object, appends the tokens at the end of the file. For example, `df.getobj('CREATURE:DWARF').add('FLIER')` would make dwarves fly. This method cannot be used for `raws.dir` objects.
* `df.remove`: When called for a `raws.token` object, that token is removed from the file containing it. When called for a `raws.file` object, that file is removed from the `raws.dir` object containing it. For example, `df.getobj('CREATURE:CAT').get('ADOPTS_OWNER').remove()` would cause cats to no longer annoyingly adopt their own dwarves. This method cannot be used for `raws.dir` objects.

Unlike a `raws.dir` object, when such a query is performed on a `raws.file` or a `raws.token`, the query stops at the end of that file. (For a `raws.dir` object the query is run for every token in every file.) While `df.get('CREATURE:DEER')` would return the token in `creature_large_temperate`, `df['descriptor_shape_standard'].get('CREATURE:DEER')` would return `None`.

Here's a simple example combining the various querying methods. This snippet would add a `[FLIER]` token to the female caste of each vanilla species of bear. (In summary: It makes female bears fly.)

```python
for bear in df.allobj(type='CREATURE', re_id='BEAR_.+'):
    bear.get('CASTE:FEMALE').add('FLIER')
```

![Image of a flying female bear](https://github.com/pineapplemachine/PyDwarf/blob/master/images/logo_transparent.png?raw=true)
