import inspect
import itertools
import textwrap



def copy(item, *args, **kwargs):
    '''Copy a raws object.'''
    if hasattr(item, 'copy'):
        return item.copy(*args, **kwargs)
    elif inspect.isgenerator(item) or inspect.isgeneratorfunction(item):
        return icopytokens(item, *args, **kwargs)
    else:
        return lcopytokens(item, *args, **kwargs)
        
def equal(a, b): 
    '''Check for equivalency between two raws objects.'''
    if hasattr(a, 'equals'):
        return a.equals(b)
    elif hasattr(b, 'equals'):
        return b.equals(a)
    else:
        return tokensequal(a, b)
        
def ends(tokens, setfile=None):
    '''
        Utility method for getting the first and last tokens of some iterable.
    '''
    try:
        if setfile is not None: raise ValueError
        return tokens[0], tokens[-1]
    except:
        first, last = None, None
        for token in tokens:
            if first is None: first = token
            last = token
            if setfile is not None: token.file = setfile
        return first, last
        
def tokensstring(tokens, dedent=True):
    '''Get a fancy string representation of some collection of tokens.'''
    if len(tokens) == 0:
        return ''
    elif len(tokens) == 1:
        return str(tokens[0])
    else:
        parts = []
        minindent = None
        for token in tokens:
            prefix = ''
            text = str(token)
            suffix = ''
            if ((token.prefix and '\n' in token.prefix)): prefix += '\n'
            if token.prefix: prefix += token.prefix.split('\n')[-1]
            if token.suffix: suffix += token.suffix.split('\n')[0]
            if ((token.suffix and '\n' in token.suffix)): suffix += '\n'
            parts.extend((prefix, text, suffix))
        fulltext = ''.join(parts).strip('\n')
        if dedent: fulltext = textwrap.dedent(fulltext)
        return fulltext
        


def copytokens(tokens, iter=False):
    '''Copy tokens contained within some iterable.'''
    return tokengenerator.tokengenerator(icopytokens(tokens)) if iter else lcopytokens(tokens)
    
def lcopytokens(tokens):
    '''Internal: Copy tokens as a tokenlist.'''
    copiedtokens = tokenlist.tokenlist()
    prevtoken = None
    for sourcetoken in tokens:
        copytoken = sourcetoken.copy()
        copiedtokens.append(copytoken)
        copytoken.prev = prevtoken
        if prevtoken is not None: prevtoken.next = copytoken
        prevtoken = copytoken
    return copiedtokens
    
def icopytokens(tokens):
    '''Internal: Copy tokens as a generator.'''
    prevtoken = None
    for sourcetoken in tokens:
        copytoken = sourcetoken.copy()
        copytoken.prev = prevtoken
        if prevtoken is not None: prevtoken.next = copytoken
        prevtoken = copytoken
        yield copytoken



def tokensequal(atokens, btokens):
    '''Check equivalency between two iterables containing tokens.'''
    return all(
        atoken.equals(btoken) for atoken, btoken in itertools.izip_longest(
            atokens, btokens, fillvalue=token.token.nulltoken
        )
    )



import token
import tokenlist
import tokengenerator
