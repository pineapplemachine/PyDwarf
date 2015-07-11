# Configuring PyDwarf

The steps given here are specifically for Windows, but the procedure on other operating systems will be almost identical.

- First thing, ensure that [Python 2.7](https://www.python.org/download/releases/2.7.8/) is installed on your computer. If you have another version of Python already installed this can be a little complicated but there are lots of [helpful resources](http://stackoverflow.com/questions/4583367/how-to-run-multiple-python-version-on-windows) available to guide you through it. PyDwarf will not run with Python 3.

- In order to keep everything working as smoothly as possible, you should copy your Dwarf Fortress directory to another location before messing about with PyDwarf. Navigate to the directory containing your Dwarf Fortress folder, copy it, and paste it somewhere. It may be easiest to place the copy in the same location and append `_original` to the end of the directory's name. After doing this you might, for example, have a folder at `C:/df_40_24_win` and another at `C:/df_40_24_win_original`.

- If you haven't already, you'll need to download PyDwarf and extract the archive somewhere. It much doesn't matter where, though I recommend you *don't* put it inside your Dwarf Fortress directory. The most important files located in here are named `manager.py`, which is for actually running PyDwarf, and `config.json`, for telling it precisely what to do when it runs.

- You'll want to open the `config.json` file, located in PyDwarf's root directory, with a text editor such as Notepad. And then you'll be looking at a JSON file. It assigns several parameters in the format of `"name": value,` and the most important ones right now are the ones named `input`, `output`, `backup`, and `scripts`. You can see that most of the values are text information enclosed within quotes, but `scripts` in particular is assigned a list of values contained within square brackets.

- Set the value for `input`, which is a file path, to the location of that copy of Dwarf Fortress you made in a previous step. This tells PyDwarf where to read your files from so that they can be worked upon by various mods. For example, this file path might be something like `C:/df_40_24_win_original`. The json file format can be particular about slashes, so it's best to make sure your file paths use forward slashes `/` and never backslashes `\`.

- And set the value for `output`, which is also a file path, to the location of the Dwarf Fortress folder that you play with. This is where PyDwarf will write your files to when it's finished modifying them. This path might look like `C:/df_40_24_win`.

- As well as the value for `backup`, another file path, to somewhere for the Dwarf Fortress files to be backed up to. This could be something like the name of the `input` folder with `_backup` appended. This helps to ensure that if something weird goes wrong - and don't worry, it really shouldn't - you'll still have a copy of your original files lying around somewhere. The path might look like `C:/df_40_24_win_backup`.

- And the really fun part is the `scripts` parameter. Here names of scripts are given in the order that they should be run. It's also possible to pass arguments to scripts here, which change the way it behaves. One way to get a list of the available scripts is to run `python manager.py --list`, and one way to see documentation regarding one of these scripts to describe its purpose and usage is to run `python manager.py --meta script.name`.

- For the sake of example, you can try adding an item to the end of the `scripts` list, the text (including quotes) `"pineapple.subplants"`. In doing so, be sure to add a comma to the end of the previous line, these commas serve to separate items in the list.

- Installing new mods for PyDwarf is really simple, if you want to use one that didn't come packaged with it. Simply place the uncompressed files, which should include at least one with a name like `pydwarf.scriptname.py`, anywhere in the `scripts` directory located within PyDwarf's root directory. If you had installed a mod named `this.is.a.script`, for example, you could tell PyDwarf to include it by adding it in the same way as the previous script: In the `scripts` list of `config.json`, you'd need to add a line to the list that looks like `"this.is.a.script"`.

- And finally, to actually run PyDwarf and apply the mods, run `python manager.py`. It will helpfully tell you if anything went wrong and, if so, what exactly happened. But PyDwarf is a piece of work and sometimes those errors may be hard to understand. If you're not sure how to fix it, you can always post in the [GitHub issue tracker](https://github.com/pineapplemachine/PyDwarf/issues) or the [Bay12 forum topic](http://www.bay12forums.com/smf/index.php?topic=150857.msg6239158#msg6239158) to ask for help.

- After running `manager.py`, if everything went smoothly, you're all done! Now you can run Dwarf Fortress and generate a new world to see the changes take effect.
