# PyDwarf config settings

Here's a list of values which PyDwarf looks for in a configuration file and an explanation of each.

## input

#### Description

This tells PyDwarf where to find your Dwarf Fortress directory. Its files will be loaded so that they can be exposed to scripts for adding, moving, removing, and modifying.

#### Examples

Your input path might look something like this on OSX or Linux.

``` yaml
input: '/Users/pineapple/Desktop/games/df/df_osx_40_24_original/'
```

And it might look more like this on Windows.

``` yaml
input: 'C:/pineapple/Desktop/games/df/df_40_24_win_original/'
```

## output

#### Description

When PyDwarf is all done running its scripts on the inputted files, this is the path to which the resulting files will be written. If this path isn't specified then PyDwarf will output to the same directory that it loaded as input. This is probably not what you want to do! Except for restoring from an earlier backup there's no way to reverse many of the changes that PyDwarf makes. In almost all cases, it's better for you to copy the Dwarf Fortress directory you're using as input to another location, then output to that copy. This way, if you want to change PyDwarf's settings and run it again to apply those changes to your Dwarf Fortress files, it will be as simple as running PyDwarf again: The original files will be inputted, and the prior output will be overwritten.

#### Examples

Your output path might look something like this on OSX or Linux.

``` yaml
output: '/Users/pineapple/Desktop/games/df/df_osx_40_24/'
```

And it might look like this on Windows.

``` yaml
output: 'C:/pineapple/Desktop/games/df/df_40_24_win/'
```

## backup

#### Description

Before PyDwarf allows any changes to be made to your Dwarf Fortress files, it will backup files that it can expect to be modified to this location. If no backup directory is specified then PyDwarf will go on without creating a backup - but this isn't recommended!

#### Examples

Your backup path might look something like this on OSX or Linux.

``` yaml
backup: '/Users/pineapple/Desktop/games/df/df_osx_40_24_bak/'
```

And it might look like this on Windows.

``` yaml
backup: 'C:/pineapple/Desktop/games/df/df_40_24_win_bak/'
```

## paths

#### Description

In order to avoid keeping track of every single file in your Dwarf Fortress directory - you almost certainly don't want PyDwarf taking its time worrying over your megabytes of saved game data, for example - PyDwarf relies on a list of paths which need considering. If no paths are specified then everything in your Dwarf Fortress directory will be loaded. If it's set to `auto` then PyDwarf will do its damndest to know which files it needs to know about all on its own. Otherwise, paths to files or whole directories can be provided as a list.

#### Examples

Allow PyDwarf to automatically determine which files to track. (This is the behavior you'll want in the vast majority of cases.)

``` yaml
paths: auto
```

Track all the files in your Dwarf Fortress directory.

``` yaml
paths: null
```

Track only your `raw/objects` directory.

``` yaml
paths: raw/objects
```

Track only your `data/init/d_init.txt` file, and your `hack` and `stonesense` directories.

``` yaml
paths:
  - data/init/d_init.txt
  - hack
  - stonesense
```

## version

#### Description

Because some scripts can only be compatible with certain versions of Dwarf Fortress, and because sometimes files need to be treated differently internally depending on the Dwarf Fortress version, PyDwarf will put up a small fuss if no Dwarf Fortress version is specified. It can optionally be set to `auto`, in which case PyDwarf will try to automatically determine your Dwarf Fortress version.

#### Examples

Allow PyDwarf to automatically determine your Dwarf Fortress version. (This is the behavior you'll want in the vast majority of cases.)

``` yaml
version: auto
```

Manually specify your Dwarf Fortress version.

``` yaml
version: "0.40.24"
```

## hackversion

#### Description

Similar to the `version` information, this setting tells PyDwarf which DFHack version - if any - is installed to your Dwarf Fortress directory. Scripts will have access to this version information and will be able to react accordingly.

#### Examples

Allow PyDwarf to automatically determine your DFHack version. (This is the behavior you'll want in the vast majority of cases.)

``` yaml
hackversion: auto
```

Manually specify your DFHack version.

``` yaml
hackversion: "0.40.24-r3"
```

## packages

#### Description

PyDwarf's script loading system means that before scripts can be run they have to be registered, and before they can be registered the modules containing them have to be imported. The primary purpose of this list of packages is to give PyDwarf a chance to register scripts before starting up. For example, in almost all cases, you'll want to specify the `scripts/` directory within PyDwarf's root directory and nothing more. This is the directory where PyDwarf's packaged scripts are located and where, typically, you would place downloaded scripts as a way to install them.

The `scripts/` directory is sneaky: It contains more than just installed scripts, it also contains a special Python file, `scripts/__init__.py`, which is run when the `scripts` package is given here. Then that Python file in turn imports all the PyDwarf scripts in that directory so that your installed scripts can be registered.

Note that if no packages are specified in this way then no scripts will be registered, and consequently PyDwarf won't know about any of your installed scripts.

#### Examples

Import only the default scripts package.

``` yaml
packages:
  - scripts
```

Import the default package as well as two theoretical packages named `foo` and `bar`.

``` yaml
packages:
  - scripts
  - foo
  - bar
```

## scripts

#### Description

Here registered scripts can be listed a few ways, most importantly by name, and they'll be run in the order they appear. An example of a single installed script might be `pineapple.noexotic`, and this name can be added to your scripts list in order to have it run. Another way to run scripts would be to add an entry like `umiman.smallthings.*`, which will cause all the scripts with the `umiman.smallthings` prefix to be run: With a default installation those scripts would be `umiman.smallthings.engraving`, `umiman.smallthings.prefstring`, `umiman.smallthings.speech.nofamily`, and `umiman.smallthings.speech.threats`. Many scripts can also be given arguments which alter their behavior. For example, the script `pineapple.boneflux` can be run using a custom number of bones required in the reaction it adds by specifying arguments like so: `args: {bone_count: 4}`.

Scripts can usually be specified given only the last part of their name, for example `pineapple.flybears` could be shortened to just `flybears`. However, if you happen to have more than one script installed by the name of `noexotic` then both scripts would be run, which probably isn't what you want PyDwarf to do in such a case. (Even though it does its best to please.)

If no scripts are given in this way then PyDwarf simply won't run any.

#### Examples

No scripts would be run.

``` yaml
scripts: null
```

The script `pineapple.noexotic` would be run, the scripts prefixed with `smallthings.umiman` would be run, and the script `pineapple.boneflux` would be run with a custom number of bones as reagent.

``` yaml
scripts:
  - pineapple.noexotic
  - umiman.smallthings.*
  - name: pineapple.boneflux
    args: {bone_count: 4}
```

The scripts `witty.restrictednobles` and `pineapple.flybears` would be run.

``` yaml
scripts:
  - restrictednobles
  - flybears
```
