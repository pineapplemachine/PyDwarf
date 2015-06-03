# PyDwarf

## Introduction

PyDwarf is licensed via the exceptionally permissive [zlib/libpng license](https://github.com/pineapplemachine/PyDwarf/blob/master/license.txt). It's written for [Python 2.7](https://www.python.org/download/releases/2.7.8/) and is intended as a mod tool for the wonderful game [Dwarf Fortress](http://www.bay12games.com/dwarves/).

I have an enormous love for Dwarf Fortress and for its mods. In the years I've been playing and following this game, I think that there's always been a gap where a really powerful raws mod manager could be. This is the niche PyDwarf is intended to fill: I want to give mod authors the power to query and modify Dwarf Fortress's raws files with an elegance hitherto unseen, and I want to give users the ability to apply these mods with a minimum of effort.

## For the user

Currently, to change things about PyDwarf like what directory it looks in for your raws, where it outputs the changes to, things of that nature, it looks in config.py. This is a Python script which sets a number of variables that the mod manager needs to know about. For the most part, making these settings work with your particular machine will only be a matter of changing the values at the right-hand side of `some.directory = 'where'` assignments. This is a short-term solution for a young project, however - I understand that it may be overwhelming for those who haven't got programming experience on which to stand. In the future, PyDwarf will also accept simpler ini or ini-like configuration files that are much easier for the layperson to comprehend. But, to the point: Once you've got the settings ready you can apply the mods you've chosen by running manager.py.

## For the mod author

### The mod loader

By default, the settings file will load any python scripts contained within the scripts/ directory whose file names begin with "pydwarf." and end with ".py". Within these scripts, any function decorated with the pydwarf.urist() decorator becomes registered with the mod manager so that it can be referred to in the settings file. The decorator accepts arguments which are treated as metadata for those registered functions. The functions themselves may have any number of keyword arguments, including **kwargs, which can be specified when indicating a script within the settings script. Please refer to pydwarf.py's urist documentation for a more thorough explanation of how function metadata is considered, and see the scripts included in the scripts/ directory for numerous examples of function registration.

### The querying functionality

The backbone of PyDwarf is its ability to query and modify the raws. Though it would be difficult to concisely explain all the functionality it affords a mod author, I believe an example can say volumes. This example snippet, run on vanilla Dwarf Fortress raws, would cause all female bears to fly: 

``` python
for bear in df.allobj(type='CREATURE', re_id='BEAR_.+'):
    bear.get('CASTE:FEMALE').add('FLIER')
```

For more detailed documentation, take a look at [the tutorial](https://github.com/pineapplemachine/PyDwarf/blob/master/tutorial.md)!

![Image of a flying female bear](https://github.com/pineapplemachine/PyDwarf/blob/master/images/logo_transparent.png?raw=true)
