# Modding with PyDwarf

## Introduction

So you want to use the fantastical powers of PyDwarf to write your own mods for Dwarf Fortress. (If you don't then what are you even doing here?)

PyDwarf and scripts written for it are written in Python. And so this documentation assumes that you have a working knowledge of programming in Python. If you're looking to start modding and you aren't familiar with Python then there are [loads of helpful courses and tutorials](https://www.codecademy.com/tracks/python) no more distant than a few clicks of the mouse.

PyDwarf offers quite a lot of functionality and abstraction and it would be impossible to effectively cover everything in just one tutorial. To help fill in the gaps you can look through the [generated documentation](index.html) which is still far from perfect but it should help set you on your way. If you want even more information, there are several places to go: You can look to PyDwarf's [`scripts/` directory](../scripts) for a bunch of example mods, you can poke your nose into the source code and most of what you'd care about is located in [this directory](../raws), or you can simply ask for help in the [Bay12 forum topic](http://www.bay12forums.com/smf/index.php?topic=150857.msg6239158#msg6239158) or the [GitHub issue tracker](https://github.com/pineapplemachine/PyDwarf/issues).

## PyDwarf's Hierarchy of Objects

### raws.dir

In PyDwarf, your Dwarf Fortress directory is represented in its entirety by one `raws.dir` object. That is, an instance of the `dir` class which is located within the `raws` package. If you were to open a command line in PyDwarf's root directory, run `python`, `import raws`, and then create a new `raws.dir` object then what you would have is essentially an empty Dwarf Fortress directory.

``` python
client-170:PyDwarf pineapple$ python
>>> import raws
>>> emptydir = raws.dir()
```

Realistically, you're not going to be so interested in an empty `raws.dir` object. In almost all cases you'll actually want to load it from somewhere. Let's actually load our Dwarf Fortress directory as a `raws.dir`.

``` python
>>> df = raws.dir('df_osx_40_23')
```

In this tutorial our `raws.dir` object is keeping track of every file in the Dwarf Fortress directory we loaded. It's important to note, though, that when running PyDwarf normally many files are excluded from this loading: You probably don't want PyDwarf to worry itself with your saves directory, for example. You can manually tell a `raws.dir` what to care about upon instantiation by including a `paths` argument.

### raws.basefile

A `raws.dir` object keeps track of what's in it by using objects which inherit from the `raws.basefile` class. There are a few different kinds: `raws.reffile` is mainly for keeping track of things like images or text files where we don't need to know about their content, `raws.binfile` is for files where we want to mess around with what's inside them but we're not too concerned about the formatting of that particular file, and the most important is `raws.rawfile` which provides quite a lot of extra functionality for accessing and modifying raws files.

``` python
>>> print type(df['data/art/curses_800x600.bmp'])
<class 'raws.reffile.reffile'>
>>> print type(df['dfhack.init'])
<class 'raws.binfile.binfile'>
>>> print type(df['raw/objects/creature_standard.txt'])
<class 'raws.rawfile.rawfile'>
```

It's also possible to add files to or remove them from a `raws.dir` using its `add` and `remove` methods.

#### raws.reffile

These files are pretty simple: When a `raws.dir` is loaded for some directory these are files it remembers the location so that when its output is written it can just copy the file over. Without intervention, PyDwarf will never look at the contents of these files.

#### raws.binfile

These files have their binary content represented by a string. It's often a good fit for plain text files such as `dfhack.init`.

#### raws.rawfile

These files are parsed and the raws data inside is given a lot of special consideration by PyDwarf. This is what we'll be focusing on in this tutorial. Each `raws.file` object is represented by a sequence of tokens, each of which represents a bit of text that looks something like `[CREATURE:DWARF]`.

### raws.token

Each of those tokens in a `raws.rawfile` is recorded within a `raws.token` object. To show how this data is kept, take these first few tokens from `raw/objects/creature_standard.txt` as an example.

```
[OBJECT:CREATURE]
[CREATURE:DWARF]
    [DESCRIPTION:A short, sturdy creature fond of drink and industry.]
    [NAME:dwarf:dwarves:dwarven]
```

This would be recorded in the file as a series of tokens. Here's some code showing how this data might be accessed.

``` python
>>> tokens = df['raw/objects/creature_standard.txt'].list(range=4)
>>> print tokens
[OBJECT:CREATURE]
[CREATURE:DWARF]
    [DESCRIPTION:A short, sturdy creature fond of drink and industry.]
    [NAME:dwarf:dwarves:dwarven]
>>> print tokens[0]
[OBJECT:CREATURE]
>>> print tokens[0].value
OBJECT
>>> print tokens[0].args
CREATURE
>>> print tokens[0].next
[CREATURE:DWARF]
>>> print tokens[0].prev
None
>>> print tokens[0].file
raw/objects/creature_standard.txt
>>> print tokens[-1]
[NAME:dwarf:dwarves:dwarven]
>>> print tokens[-1].args
dwarf:dwarves:dwarven
>>> print len(tokens[-1].args)
3
>>> print tokens[-1].args[0]
dwarf
```

Each token has a number of important attributes.

* `value` represents the first string inside the braces, as delimited by colons.
* `args` is a list of the second through final strings in the braces. It can be accessed and modified just like a normal Python list.
* `prev` is a reference to the preceding `raws.token` in the file, list, or other collection.
* `next` is a reference to the following `raws.token` in the same.
* `prefix` is text outside braces and preceding the token.
* `suffix` is text outside braces and following the token.
* `file` is a reference to the `raws.rawfile` in which the `raws.token` is contained, or `None` if it doesn't belong to any file.

## Finding Particular Tokens

### The Query Method

So you've familiarized yourself with how PyDwarf keeps track of all this data and now you're ready to have a go yourself. But where do you start? How do you tell PyDwarf to find that one specific token for you?

Anything that can contain raws data - `raws.dir`, `raws.rawfile`, `raws.token` objects, and a few more - has access to a number of methods to make finding what you need easier. Most of them are abstractions of a base `query` method, which is for finding a token or tokens which meet some condition.

Here you can see just how the `query` method works. Don't expect to be using it much if at all, but know that the methods you will be using all use this method to do most of their work.

The definition of the `query` method looks like this.

``` python
def query(self, filters, tokens=None, iter=False, **kwargs):
```

* `filters` is an iterable of callable objects like functions, lambdas, or `raws.filter` objects, or optionally a single filter. Each should accept one or two arguments and return either a single boolean or a tuple containing two booleans. The first returned boolean dictates whether a token was a match or not - if it's a match then it'll be included in the method's returned or yielded value. The second returned boolean, if included, decides whether the query should be immediately terminated. The first argument is a reference to the token being checked for matching. The second argument, if included, is a count recording the number of tokens that this filter has already matched in this one query.
* `tokens` is an iterable of tokens to step through and perform the query on. If left unspecified the iterator is retrieved automatically.
* `iter` tells the method whether to return a `raws.tokenlist` or a `raws.tokengenerator`. In most cases there'll be no need to worry about the distinction: Both of them can be queried like any other collection of tokens, the most important difference is that the former keeps a list in memory whereas the latter acts like a generator.
* `**kwargs` are passed on to the object's `tokens` method if the `tokens` argument is left set to `None`.

### Removing Aquifers

Let's say you wanted to find and remove all of the `[AQUIFER]` tokens in your raws. Here's how you could go about that using the `all` method.

``` python
>>> aquifers = df.all('AQUIFER')
>>> print len(aquifers)
19
>>> for aquifer in aquifers: aquifer.remove()
...
>>> print len(df.all('AQUIFER'))
0
```

If you wanted, you could do the same thing using the `query` method and a lambda function as a filter.

``` python
>>> aquifers = df.query(lambda token: token.value == 'AQUIFER')
>>> print len(aquifers)
19
>>> for aquifer in aquifers: aquifer.remove()
...
>>> print len(df.all('AQUIFER'))
0
```

### Finding the Dwarf

Or let's say you wanted to find the `[CREATURE:DWARF]` token defining the actual creature. For this we'd have to do something a little complicated to make sure we get the token that actually defines the creature, and not the token which is just a property of `[ENTITY:MOUNTAIN]`.

``` python
>>> print len(df.all('CREATURE:DWARF'))
2
```

``` python
>>> headers = df.query(lambda token: token == 'OBJECT:CREATURE')
>>> dwarves = headers.each(lambda token: token.get('CREATURE:DWARF'))
>>> print len(dwarves)
1
>>> dwarf = dwarves[0]
>>> print dwarf
[CREATURE:DWARF]
>>> print dwarf.file
raw/objects/creature_standard.txt
```

We can do this because we know that the `[CREATURE:DWARF]` token we want will always appear after an `[OBJECT:CREATURE]` token in some file. So first we used a query to get all the `[OBJECT:CREATURE]` headers, then we used the `each` method of `raws.tokencollection` to find the `[CREATURE:DWARF]` token which followed one of those headers.

You could also do something like this, since you know what file the token is in, but it's not the best practice. What if a mod you installed moved the `[CREATURE:DWARF]` definition to a different file?

``` python
>>> print df['raw/objects/creature_standard.txt'].get('CREATURE:DWARF')
[CREATURE:DWARF]
```

Fortunately, you won't have to worry about this stuff. PyDwarf helpfully provides methods that concern themselves about all these caveats so that you don't have to. You could have found that token just like this, using the `getobj` method.

``` python
>>> dwarf = df.getobj('CREATURE:DWARF')
>>> print dwarf
[CREATURE:DWARF]
>>> print dwarf.file
raw/objects/creature_standard.txt
```

### Your Toolbox

There are lots of these sorts of methods and in order to understand all of them you'd want to look more deeply into PyDwarf's documentation. But to start you off, here's some of the ones you might find yourself using most often.

* [`get`](index.html#raws.queryable.get) finds the first matching token.
* [`last`](index.html#raws.queryable.last) finds the last matching token.
* [`all`](index.html#raws.queryable.all) finds all the matching tokens.
* [`getprop`](index.html#raws.queryableprop.getprop) gets the first matching token that's a property of this object, like `[FLIER]` is a property of `[CREATURE:MOSQUITO]`. There are also the [`lastprop`](index.html#raws.queryableprop.lastprop) and [`allprop`](index.html#raws.queryableprop.allprop) methods.
* [`getobj`](index.html#raws.queryableobj.getobj) finds the object of a given type and id. There's also [`allobj`](index.html#raws.queryableobj.allobj) which can find, for example, all the objects of a given type.

## Registering Your Script with PyDwarf

### Writing Your Script

Now you have an idea for a mod. Maybe you were even able to make the changes you wanted via Python in the command line, or by running a simple script. Good job! I'm proud of your initiative and your imagination. But now it's time to wrap it up in a nice package so that PyDwarf knows how to handle it, so that others can have PyDwarf manage your mod just like any other.

Let's say you've made a simple script for removing all the `[AQUIFER]` tokens like we did in [that one example](#removing-aquifers) only a short while ago, and that your code looks like this.

``` python
for aquifer in df.all('AQUIFER'):
    aquifer.remove()
```

### The Appropriate Place

First thing you'll want to create a Python file in PyDwarf's `scripts/` directory. There are ways to have PyDwarf recognize this script when it's placed elsewhere, but this is definitely where you want to put it for now. For this example let's create a folder called `mynamespace` in which to put the scripts you write and let's create a file in it named `pydwarf.myscript.py`. In order for a script to be recognized here the file name has to start with `pydwarf.` and end with `.py` but everything in between is up to you and PyDwarf doesn't care what subdirectory the script goes in. (But those who download your mod might. Try to keep things organized!)

In this file you should place your nifty code inside a function like so.

``` python
import pydwarf

def myscript(df):
    # Find and remove each aquifer
    for aquifer in df.all('AQUIFER'):
        aquifer.remove()
        
    # All done, now let PyDwarf know the script did its job successfully.
    return pydwarf.success()
```

### Script Arguments

The first argument must always accept a reference to the Dwarf Fortress `raws.dir` object. Other named arguments can be specified by the user of your script as a way of customizing its behavior. As a matter of fact, let's add one such argument now. In this example we'll allow the user to tell your script to remove something other than aquifers if that's what they want.

``` python
def myscript(df, token='AQUIFER'):
    # Find and remove each token
    for aquifer in df.all(token):
        aquifer.remove()
        
    # All done, now let PyDwarf know the script did its job successfully.
    return pydwarf.success()
```

### Registering Your Script

But we aren't done just yet! PyDwarf won't load any old function as a script, it needs to have a `pydwarf.urist` decorator in order for it to be registered. (PyDwarf won't know what to do with your script if it isn't registered.) If you're in a terrible hurry this could be as simple as preceding your function with a single line, `@pydwarf.urist`, like so.

``` python
import pydwarf

@pydwarf.urist
def myscript(df, token='AQUIFER'):
    # Find and remove each token
    for aquifer in df.all(token):
        aquifer.remove()
        
    # All done, now let PyDwarf know the script did its job successfully.
    return pydwarf.success()
```

But people who download and use your script would certainly like it much better if you included information about your script, what it does, and how to use it. Here's what your whole `mynamespace/pydwarf.myscript.py` file might look like with all this information added.

``` python
import pydwarf

@pydwarf.urist(
    name = 'mynamespace.myscript',
    version = '1.0',
    author = 'Yours Truly',
    description = 'Remove all tokens of a certain kind, [AQUIFER] tokens by default.',
    arguments = {
        'token': 'The kind of token to remove.',
    },
)
def myscript(df, token='AQUIFER'):
    # Find and remove each token
    for aquifer in df.all(token):
        aquifer.remove()
        
    # All done, now let PyDwarf know the script did its job successfully.
    return pydwarf.success()
```

You can assign some value to anything you want in that decorator! You could write `@pydwarf.urist(foo = 'bar')` if you felt so inclined and then wehn PyDwarf was asked to provide information about your script, it would go ahead and tell you that foo is equal to bar. But there are several things other than `foo` that PyDwarf gives special treatment to. Here are the really important ones. 

* `name` gives your script a name, and that should be something descriptive. You might be wondering what dots and `mynamespace` mean when they're in there. Everything preceding the final dot is the namespace, and everything following is the name. The namespace is for organization, makes it so both PyDwarf and users of your script can tell how it might be related to others. For the scripts packaged with PyDwarf, the namespace corresponds to the author of the script. So, for example, all the scripts in the `pineapple` namespace were written by yours truly.
* `version` identifies the verison of your script. If you were to improve and rerelease your script you might want to increment the version number for the new script.
* `author` tells people who actually wrote the script.
* `description` is to help people understand the purpose of your script. It should, of course, be as descriptive as possible.
* `arguments` describes the purpose of each of your script's arguments, in case it accepts any.

## Running Your Script

### Running PyDwarf

So at this point you've come up with a great idea, you've written your script and done things in such a way that PyDwarf knows all about it. It's time to run your script and see how it goes!

There are a few ways to do this, the most familiar might be to add your script `mynamespace.myscript` to the `scripts` list in your configuration file. We'll cover a slightly different way to do this, though.

Go ahead and open a command line in your PyDwarf directory and run the command `python manager.py -s mynamespace.myscript`. The result should look a lot like this.

``` bash
client-170:PyDwarf pineapple$ python manager.py -s mynamespace.myscript
2015.07.30.09.26.40: INFO: Applying yaml configuration from config.yaml.
2015.07.30.09.26.40: INFO: Running PyDwarf manager version 1.1.0.
2015.07.30.09.26.40: INFO: Configuring session using raws input directory /Users/pineapple/Desktop/games/df/df_osx_40_24_original/.
2015.07.30.09.26.43: INFO: Backing up raws to desination /Users/pineapple/Desktop/games/df/df_osx_40_24_bak/.
2015.07.30.09.26.43: INFO: Running script mynamespace.myscript.
2015.07.30.09.26.44: INFO: SUCCESS: Ran successfully.
2015.07.30.09.26.44: INFO: Writing output to destination /Users/pineapple/Desktop/games/df/df_osx_40_24/.
2015.07.30.09.26.45: INFO: All done!
```

### Aftermath

Now you can open up the files in your Dwarf Fortress directory and see the results! In vanilla Dwarf Fortress raws, `raw/objects/inorganic_stone_soil.txt` contains a bunch of `[AQUIFER]` tokens. But not in yours.

``` bash
client-170:PyDwarf pineapple$ grep AQUIFER /Users/pineapple/Desktop/games/df/df_osx_40_24_original/raw/objects/inorganic_stone_soil.txt
[SOIL][AQUIFER]
[SOIL][AQUIFER]
[SOIL][AQUIFER]
[SOIL][AQUIFER]
[SOIL][AQUIFER]
[SOIL][AQUIFER]
[SOIL][AQUIFER]
[SOIL][AQUIFER][SOIL_SAND]
[SOIL][AQUIFER][SOIL_SAND]
[SOIL][AQUIFER][SOIL_SAND]
[SOIL][AQUIFER][SOIL_SAND]
[SOIL][AQUIFER][SOIL_SAND]
[SOIL][AQUIFER]
[SOIL_OCEAN][AQUIFER]
[SOIL_OCEAN][AQUIFER]
[SOIL_OCEAN][AQUIFER]
client-170:PyDwarf pineapple$ grep AQUIFER /Users/pineapple/Desktop/games/df/df_osx_40_24/raw/objects/inorganic_stone_soil.txt
```

Congratulations on making your first mod with PyDwarf! I hope things go smoothly for you from here. In case you want much more in-depth documentation you can always refer to the [html docs](index.html), and you can post in the GitHub repository's [issue tracker](https://github.com/pineapplemachine/PyDwarf/issues) or on the [Bay12 forum topic](http://www.bay12forums.com/smf/index.php?topic=150857.0).
