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
    ('token.__init__', 'token.nargs', '''
        >>> token = raws.token('EXAMPLE:0:1:2:3:4')
        >>> print 'Token has %d arguments.' % token.nargs()
        Token has 5 arguments.
        >>> print token.nargs(2)
        False
        >>> print token.nargs(5)
        True
    '''),
    ('token.__init__', 'tokenargs.set', 'tokenargs.clear', 'tokenargs.add', '''
        >>> token = raws.token('EXAMPLE:a:b:c')
        >>> print token
        [EXAMPLE:a:b:c]
        >>> token.args.set(2, 500)
        >>> print token
        [EXAMPLE:a:b:500]
        >>> token.args.set('hi!')
        >>> print token
        [EXAMPLE:hi!:b:500]
        >>> token.args.clear()
        >>> print token
        [EXAMPLE]
        >>> token.args.add('X')
        >>> print token
        [EXAMPLE:X]
        >>> token.args.add('Y', 'Z')
        >>> print token
        [EXAMPLE:X:Y:Z]
    '''),
    ('token.__init__', 'tokenargs.__contains__', '''
        >>> token = raws.token('EXAMPLE:ONE:TWO:FOUR')
        >>> print 'ONE' in token.args
        True
        >>> print 'THREE' in token.args
        False
    '''),
    ('token.__init__', 'tokenargs.__str__', 'tokenargs.__repr___', '''
        >>> token = raws.token('EXAMPLE:a:b:c')
        >>> print str(token.args)
        a:b:c
        >>> print repr(token.args)
        a:b:c
    '''),
    ('token.__init__', 'token.getprefix', 'token.getsuffix', 'token.__repr__', '''
        >>> token = raws.token('This is a comment [EXAMPLE] so is this')
        >>> print token
        [EXAMPLE]
        >>> print token.getprefix()
        This is a comment 
        >>> print token.getsuffix()
         so is this
        >>> token.setprefix('Hi ')
        >>> token.setsuffix(' there')
        >>> print repr(token)
        Hi [EXAMPLE] there
    '''),
]
