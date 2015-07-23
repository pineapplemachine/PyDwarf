import inspect
import itertools



def copy(item):
    if hasattr(item, 'copy'):
        return item.copy()
    elif inspect.isgenerator(item) or inspect.isgeneratorfunction(item):
        return icopytokens(item)
    else:
        return lcopytokens(item)
        
def equal(a, b): 
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
        


def copytokens(tokens, iter=False):
    return icopytokens(tokens) if iter else lcopytokens(tokens)
    
def lcopytokens(tokens):
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
    prevtoken = None
    for sourcetoken in tokens:
        copytoken = sourcetoken.copy()
        copytoken.prev = prevtoken
        if prevtoken is not None: prevtoken.next = copytoken
        prevtoken = copytoken
        yield copytoken



def tokensequal(atokens, btokens):
    return all(
        atoken.equals(btoken) for atoken, btoken in itertools.izip_longest(
            atokens, btokens, fillvalue=token.token.nulltoken
        )
    )



import token
import tokenlist
