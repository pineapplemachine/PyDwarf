# Your First Time with PyDwarf

The steps given here are specifically for Windows, but the procedure on other operating systems will be almost identical.

## Installing Python

- First thing, ensure that [Python 2.7](https://www.python.org/download/releases/2.7.8/) is installed on your computer. PyDwarf will not run with Python 3. If you have multiple version of python installed but would prefer to keep Python 3 as your default, substituting `python2` for `python` at the beginning of PyDwarf commands should work (e.g. `python2 manager.py`)
  - **On Windows:** there are lots of [helpful resources for windows](http://stackoverflow.com/questions/4583367/how-to-run-multiple-python-version-on-windows) available to guide you through other ways to achieve this
  - **On Mac:** some optional suggestions for managing python on macOS can be [found here](https://docs.python-guide.org/starting/install/osx/)
  - when in doubt, you can check your python version with `python --version`

## Setting up DF Folders (input, output and backup)

- In order to keep everything working as smoothly as possible, you should copy your Dwarf Fortress directory to another location before messing about with PyDwarf. Navigate to the directory containing your Dwarf Fortress folder, copy it, and paste it somewhere. It may be easiest to place the copy in the same location and append `_original` to the end of the directory's name. After doing this you might, for example, have a folder at `C:/df_40_24_win` which will become the `output` folder and another at `C:/df_40_24_win_original` which will become the `input` folder.

- Create a folder where Dwarf Fortress files can be backed up to. This helps to ensure that if something weird goes wrong with your original, inputted folder - and don't worry, it really shouldn't - then you'll still have a copy of your original files lying around somewhere. This could be something like the name of the `input` folder with `_backup` appended: `C:/df_40_24_win_backup`.

## Download and Extract PyDwarf

- If you haven't already, you'll need to download PyDwarf and extract the archive somewhere. It much doesn't matter where, though I recommend you *don't* put it inside your Dwarf Fortress directory. The most important files located in here are named `manager.py`, which is for actually running PyDwarf, and `config.yaml`, for telling it precisely what to do when it runs.

## Configure PyDwarf

- You'll want to open the `config.yaml` file, located in PyDwarf's root directory, with a text editor such as Notepad. And then you'll be looking at a yaml file. It assigns several parameters in the format of `name: value` and the most important ones right now are the ones named `input`, `output`, `backup`, and `scripts`. You can see that most of the values are simple text, but `scripts` in particular is assigned a sequence of values.

- PyDwarf also supports json configuration files, and loading configuration from a Python module. The default places PyDwarf looks for these are `config.json` and `override.py`, respectively, located in its root directory. For examples of what these files might look like you can check out the files in `docs/config/`. (But you probably don't need to worry about this.)

- Set the value for `input`, which is a file path, to the location of that copy of Dwarf Fortress you made in a previous step. This tells PyDwarf where to read your files from so that they can be worked upon by various mods. For example, this file path might be something like `C:/df_40_24_win_original`.

- And set the value for `output`, which is also a file path, to the location of the Dwarf Fortress folder that you play with. This is where PyDwarf will write your files to when it's finished modifying them. This path might look like `C:/df_40_24_win`. You need to have separate input and output directories because *PyDwarf's changes to the output directory cannot be undone!* You need the original folder in case you don't like PyDwarf's changes, or in case you want to re-run PyDwarf with different settings.

- Likewise, set `backup` to the name of your backup folder created earlier (for example `C:/df_40_24_backup`)

## List, Run, and Install Scripts

- And the really fun part is the `scripts` parameter. Here names of scripts are given in the order that they should be run. It's also possible to pass arguments to scripts here, which can customize the way they behave. Check out the example config file for how to do that! One way to get a list of the available scripts is to run `python manager.py --list`, and one way to see documentation regarding a particular one of these scripts a description of its purpose and usage is to run `python manager.py --meta script.name`, where `script.name` is the name of the script you want to see.

- For the sake of example, you can try adding an item to the list of `scripts`. The line you add would, if you wanted to add the script `pineapple.subplants`, look like this: `    - pineapple.subplants`. Be sure to indent it the same as the other items in the list! Here's a helpful and [much more thorough guide](http://symfony.com/doc/current/components/yaml/yaml_format.html) on how to use yaml.

- Installing new mods for PyDwarf is really simple if you want to use one that didn't come packaged with it. Simply place the uncompressed files, which should include at least one file with a name like `pydwarf.scriptname.py`, anywhere in the `scripts` directory located within PyDwarf's root directory. If you had installed a mod named `this.is.a.script`, for example, you could tell PyDwarf to include it by adding it in the same way as the previous script: In the `scripts` list of `config.yaml`, you'd add a line to the list that looks like `    - this.is.a.script`.

- And finally, to actually run PyDwarf and apply the mods, run `python manager.py`. It will helpfully tell you if anything went wrong and, if so, what exactly happened. But PyDwarf is a piece of work and sometimes those errors may be hard to understand. If you're not sure how to fix it, you can always post in the [GitHub issue tracker](https://github.com/pineapplemachine/PyDwarf/issues) or the [Bay12 forum topic](http://www.bay12forums.com/smf/index.php?topic=150857.msg6239158#msg6239158) to ask for help.

- After running `manager.py`, if everything went smoothly, you're all done! Now you can run Dwarf Fortress and generate a new world to see the changes take effect.
