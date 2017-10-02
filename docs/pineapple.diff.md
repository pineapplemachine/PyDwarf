# pineapple.diff

## Introduction

When I wrote the `pineapple.diff` script it was a sort of off-hand thing I didn't expect anyone to really use... it turns out that to a lot of people this is the most interesting part of PyDwarf! `pineapple.diff` acts as a mod merger, but it's a little smarter than most because it diff's files based on individual tokens, unlike other mod mergers which diff based on lines. Additionally, it's able to merge several mods at once and tell you whether there were conflicts and exactly where they are so that you can address the conflicts yourself.

This tutorial assumes that you have PyDwarf installed and already know how to run and configure PyDwarf. If you haven't figured all of that out yet, I strongly recommend that you follow this tutorial first: [Your First Time with PyDwarf](introduction.md).

## Let's get started!

The very first thing you'll need is one or more mods that you want to merge into your modded install.

Take note: The mods you want to merge have to be in the same structure as a normal Dwarf Fortress install. For example, let's consider the imaginary example mod **cool_mod**. Let's say **cool_mod** modifies `entity_default.txt` and nothing else, and it provides a single file that you would normally manually overwrite the original `entity_default` file with.

To merge this mod using `pineapple.diff` you would need to create a directory structure containing the file like `cool_mod/raw/objects/entity_default.txt`. This is because PyDwarf won't know where the file belongs, otherwise!

Then you will need to add `pineapple.diff` to your list of scripts for PyDwarf to run. Here is what your yaml configuration file's scripts list might look like if you wanted to install **cool_mod**, where `C:/path/to/cool_mod` is the actual file path to the **cool_mod** folder on your system.

``` yaml
scripts:
  - name: pineapple.diff
    args: {'paths': ['C:/path/to/cool_mod']}
```

You could also add more mods in a list, like this, if you wanted to merge more than one:

``` yaml
scripts:
  - name: pineapple.diff
    args: {'paths': ['C:/path/to/cool_mod', 'C:/path/to/awesome_mod', 'C:/path/to/excellent_mod']}
```

Then when you run PyDwarf its log should look something like this:

``` text
sophie:PyDwarf pineapple$ python manager.py
2017.10.02.12.13.26: INFO: Applying yaml configuration from config.yaml.
2017.10.02.12.13.26: INFO: Applying python configuration from config.py.
2017.10.02.12.13.26: INFO: Running PyDwarf manager version 1.1.4.
2017.10.02.12.13.26: INFO: Configuring session using raws input directory /Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23_vanilla.
2017.10.02.12.13.30: INFO: Backing up raws to desination /Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23_backup.
2017.10.02.12.13.30: INFO: Running script pineapple.diffwith args {'paths': ['/Users/pineapple/Desktop/stuff/cool_mod']}.
2017.10.02.12.13.31: INFO: Handling diff for file /Users/pineapple/Desktop/stuff/cool_mod/raw/objects/entity_default.txt...
2017.10.02.12.13.31: INFO: SUCCESS: Merged 1 mods without conflicts.
2017.10.02.12.13.31: INFO: Writing output to destination /Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23.
2017.10.02.12.13.31: INFO: All done!
```

## Other stuff you should know

- `pineapple.diff` should be the very first script in your list. If you put it later in the script list, then PyDwarf won't know what the original raws looked like anymore, and will make errors when trying to compare mods you want to merge.

- If the mod you're installing isn't normally compatible with the version of Dwarf Fortress you're modifying, PyDwarf can't fix that! Attempting to install mods written for different versions of Dwarf Fortress with `pineapple.diff` is usually going to result in broken raws.

- Attempting to add different mods that add the same file might not give you the results you want; `pineapple.diff` will pick one version of the newly added file and go with it and won't attempt to combine them.

- Sometimes a conflict might be encountered when merging mods; this means that two different mods tried to make different changes to the same part of a file. When this happens PyDwarf will let you know what happened and where it happened so that you can open those files in a text editor and resolve the conflicts yourself.
