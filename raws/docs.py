import inspect
import doctest

import forward



examples = [
    ('token.__init__', '''
        >>> print raws.token('DISPLAY_COLOR:6:0:1')
        [DISPLAY_COLOR:6:0:1]
        >>> print raws.token(value='DISPLAY_COLOR', args=['6', '0', '1'])
        [DISPLAY_COLOR:6:0:1]
        >>> print repr(raws.token(value='EXAMPLE', arg='TOKEN', suffix=' hiya'))
        [EXAMPLE:TOKEN] hiya
    '''),
    ('token.__init__', 'token.__str__', 'token.__repr__', '''
        >>> token = raws.token('prefix [HI] suffix')
        >>> print str(token)
        [HI]
        >>> print repr(token)
        prefix [HI] suffix
    '''),
    ('token.__init__', 'token.__eq__', 'token.__ne__', '''
        >>> example_a = raws.token('EXAMPLE')
        >>> example_b = raws.token('EXAMPLE')
        >>> example_c = raws.token('ANOTHER_EXAMPLE')
        >>> example_d = raws.token('ANOTHER_EXAMPLE')
        >>> example_a == example_a
        True
        >>> example_a == example_b
        True
        >>> example_a == example_c
        False
        >>> example_c == example_d
        True
        >>> print example_a != example_b
        False
        >>> print example_a != example_c
        True
        >>> example_a is example_a
        True
        >>> example_a is example_b
        False
    '''),
    ('dir.getfile', 'queryable.get', 'token.__gt__', 'token.__lt__', 'token.__ge__', 'token.__le__', '''
        >>> creature_standard = df.getfile('creature_standard')
        >>> elf = creature_standard.get('CREATURE:ELF')
        >>> goblin = creature_standard.get('CREATURE:GOBLIN') # goblins are defined after elves in creature_standard
        >>> print elf > goblin
        False
        >>> print elf < goblin
        True
        >>> print elf > elf
        False
        >>> print elf >= elf
        True
        >>> print elf < elf
        False
        >>> print elf <= elf
        True
    '''),
    ('token.__init__', 'token.__add__', 'token.__radd__', '''
        >>> one = raws.token('NUMBER:ONE')
        >>> two = raws.token('NUMBER:TWO')
        >>> three = raws.token('NUMBER:THREE')
        >>> tokens = one + two + three
        >>> print tokens
        [NUMBER:ONE][NUMBER:TWO][NUMBER:THREE]
        >>> zero = raws.token('NUMBER:ZERO')
        >>> print zero + tokens
        [NUMBER:ZERO][NUMBER:ONE][NUMBER:TWO][NUMBER:THREE]
    '''),
    ('token.__init__', 'token.__mul__', '''
        >>> token = raws.token('EXAMPLE')
        >>> print token * 2
        [EXAMPLE][EXAMPLE]
        >>> print token * 6
        [EXAMPLE][EXAMPLE][EXAMPLE][EXAMPLE][EXAMPLE][EXAMPLE]
    '''),
    ('token.__init__', 'token.__iadd__', 'token.__isub__', '''
        >>> token = raws.token('EXAMPLE')
        >>> print token
        [EXAMPLE]
        >>> token += 'ONE'
        >>> print token
        [EXAMPLE:ONE]
        >>> token += 'TWO'
        >>> token += 'THREE'
        >>> print token
        [EXAMPLE:ONE:TWO:THREE]
        >>> token -= 1
        >>> print token
        [EXAMPLE:ONE:TWO]
        >>> token += ['HOWDY', 'DO']
        >>> print token
        [EXAMPLE:ONE:TWO:HOWDY:DO]
    '''),
]



examplesdict = {}
for example in examples:
    if len(example) > 1:
        exampletext = example[-1]
        for classname, membername in (item.split('.') for item in example[:-1]):
            if classname not in examplesdict: examplesdict[classname] = {}
            if membername not in examplesdict[classname]: examplesdict[classname][membername] = []
            examplesdict[classname][membername].append(exampletext)

def getexamples(classname, membername):
    exampleslist = examplesdict.get(classname, {}).get(membername)
    if exampleslist:
        return '\n\n'.join(exampleslist)
    else:
        return ''
    
def getclass(method):
    for cls in inspect.getmro(method.im_class):
        if method.__name__ in cls.__dict__: return  cls
    return None
    
def docclass(cls):
    members = inspect.getmembers(cls, predicate=inspect.ismethod)
    for member in members: docmember(member[1], cls)
    return cls
    
def docmember(member, cls=None):
    classname, membername = (cls if cls else getclass(member)).__name__, member.__name__
    description = member.__doc__.strip() if member.__doc__ else ''
    examples = getexamples(classname, membername)
    docstring = '\n\n'.join(i for i in (description, examples) if i)
    try:
        member.__doc__ = docstring
    except:
        member.__func__.__doc__ = docstring
    return member
    
def test(df, raws):
    globs = {'df': df, 'raws': raws}
    docparser = doctest.DocTestParser()
    docrunner = doctest.DocTestRunner()
    results = []
    testnum = 0
    for example in examples:
        testnum += 1
        test = docparser.get_doctest(
            string = example[-1],
            globs = globs,
            name = 'doctest %d' % testnum,
            filename = None,
            lineno = None
        )
        docrunner.run(
            test = test,
            out = lambda result: results.append(result),
            clear_globs = False
        )
    return results
    
@forward.declare
def doc(item):
    if inspect.isclass(item):
        return docclass(item)
    else:
        return docmember(item)
    