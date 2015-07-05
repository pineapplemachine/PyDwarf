# Configuring PyDwarf

The steps given here are specifically for Windows, but the procedure on other operating systems will be almost identical.

- First thing, ensure that [Python 2.7](https://www.python.org/download/releases/2.7.8/) is installed on your computer. If this is the only version of Python you have installed then the commands the following steps will tell you to run should look exactly like they're presented, and are run by opening a command line in PyDwarf's root directory, typing the given text, then hitting enter. If you have other versions of Python installed as well, you'll likely need to do some tinkering with environment variables that's outside the scope of this example.

- In order to keep everything working as smoothly as possible, the first thing you should do is to copy your Dwarf Fortress directory to another location before running PyDwarf. Navigate to the directory containing your Dwarf Fortress folder, copy it, and paste it somewhere. It may be easiest to place the copy in the same location and append `_vanilla` to the end of the directory's name.

- Right-click on `config.json`, located in PyDwarf's root directory, and select `Open with`. In the `Open with` menu, select `Choose default program` and find Notepad in the list of programs. Upon selecting Notepad, a window will appear showing the contents of `config.json`.

- Now you're looking at a JSON file. It's assigns several parameters in the format of `"name": value,` and the most important ones right now are the ones named `input`, `output`, `backup`, and `scripts`. You can see that most of the values are text information, but `scripts` in particular is assigned a list of values contained within square brackets.

- Set the value for `input`, which is a file path, to the location of that copy of Dwarf Fortress you made in a previous step. This tells PyDwarf where to read your files from so that they can be worked upon by various mods.

- Set the value for `output`, which is also a file path, to the location of the Dwarf Fortress folder that you play with. This is where PyDwarf will write your files to when it's finished modifying them.

- Set the value for `backup`, another file path, to somewhere for the Dwarf Fortress files to be backed up to. This could be something like the name of the `input` folder with `_backup` appended. This helps to ensure that if something weird goes wrong - and don't worry, it really shouldn't - you'll still have a copy of your original files lying around somewhere.

- And the really fun part is the `scripts` parameter. Here names of scripts are given in the order that they should be run. It's also possible to pass arguments to scripts here, which change the way it behaves. One way to get a list of the available scripts is to run `python manager.py --list`, and one way to see documentation regarding one of these scripts to describe its purpose and usage is to run `python manager.py --meta script.name`.

- For the sake of example, you can try adding an item to the end of the `scripts` list, the text (including quotes) `"pineapple.subplants"`. In doing so, be sure to add a comma to the end of the previous line, these commas serve to separate items in the list.

- And finally, to actually run PyDwarf and apply the mods, run `python manager.py`. You're all done! Run Dwarf Fortress and generate a new world to see the changes to your raws take effect.
