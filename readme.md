# PyDwarf

I have an enormous love for Dwarf Fortress and for its mods. In the years I've been playing and following this game, I think that there's always been a gap where a really powerful raws mod manager could be. This is the niche PyDwarf is intended to fill: I want to give mod authors the power to access and modify Dwarf Fortress's files with an elegance hitherto unseen, and I want to give users the ability to apply these mods with a minimum of effort.

PyDwarf is licensed via the exceptionally permissive [zlib/libpng license](https://github.com/pineapplemachine/PyDwarf/blob/master/license.txt). It's written for [Python 2.7](https://www.python.org/downloads/release/python-279/) and is intended as a mod tool for the wonderful game [Dwarf Fortress](http://www.bay12games.com/dwarves/).

## Configuring PyDwarf

PyDwarf is easy to configure! Open `config.yaml` with your favorite plain text editor and tell it where to find your Dwarf Fortress raws, edit the list of scripts to reflect the mods you want to run and in what order you'd like them to run. Once the configuration is to your liking you can run `manager.py`: With Python 2.7 installed this can be done by opening a command line in the PyDwarf directory and running `python manager.py`.

Here's a [step-by-step tutorial](docs/introduction.md) describing what this process might entail your first time around, here's [detailed documentation](docs/config.md) on how to configure PyDwarf, and here's a full [list of scripts](docs/scripts.md) which come bundled with PyDwarf.

## Modding using PyDwarf

If you're interested in writing your own mods for PyDwarf or in understanding its more advanced features, take a look at [this tutorial](docs/modding.md), which goes into detail about how to write mods using PyDwarf.

## Links & Documentation

- [Download and install Python 2.7](https://www.python.org/downloads/release/python-279/)
- [Series of Python tutorials](learnpythonthehardway.org/book/ex0.html)
- [Tutorial for your first time using PyDwarf](docs/introduction.md)
- [Tutorial for getting started modding with PyDwarf](docs/modding.md)
- [Documentation for advanced configuring of PyDwarf](docs/config.md)
- [Documentation for PyDwarf's Python code](docs/index.html)
- [Documentation for scripts packaged with PyDwarf](docs/scripts.md)
- [Issue tracker on GitHub](https://github.com/pineapplemachine/PyDwarf/issues)
- [PyDwarf on the Bay12 forums](http://www.bay12forums.com/smf/index.php?topic=150857.0)

![Image of a flying female bear](images/logo_transparent.png)
