def parseplural(data, implicit=False, **kwargs):
    '''Parses a string, turns it into a list of tokens.

    data: The string to be parsed.
    implicit: Determines behavior when there are no opening or closing braces.
        If True, then the input is assumed to be the contents of a token, e.g. [input].
        If False, an exception is raised.
    **kwargs: Extra named arguments are passed to the constructor each time a new
        rawstoken is distinguished and created.
    '''

    tokens = tokenlist.tokenlist() # maintain a sequential list of tokens
    pos = 0 # byte position in data
    if data.find('[') == -1 and data.find(']') == -1:
        if implicit:
            tokenparts = data.split(':')
            implicittoken = token.token(
                value = tokenparts[0],
                args = tokenparts[1:],
                **kwargs
            )
            tokens.append(implicittoken)
            return tokens
        else:
            raise ValueError('Failed to parse data string because it had no braces and because implicit was set to False.')
    else:
        while pos < len(data):
            parsetoken = None
            open = data.find('[', pos)
            if open >= 0 and open < len(data):
                close = data.find(']', open)
                if close >= 0 and close < len(data):
                    prefix = data[pos:open]
                    tokentext = data[open+1:close]
                    tokenparts = tokentext.split(':')
                    parsetoken = token.token(
                        value = tokenparts[0],
                        args = tokenparts[1:],
                        prefix = prefix,
                        prev = tokens[-1] if len(tokens) else None,
                        **kwargs
                    )
                    pos = close+1
            if parsetoken is not None:
                if len(tokens): tokens[-1].next = parsetoken
                tokens.append(parsetoken)
            else:
                break
        if len(tokens) and pos<len(data):
            tokens[-1].suffix = data[pos:]
        return tokens
        
        
        
def parsesingular(data, implicit=True, fail_on_multiple=True, apply=None, **kwargs):
    '''Parses a string containing exactly one token. **kwargs are passed on to the parse static method.
    '''
    if data.count('[') > 1:
        if fail_on_multiple:
            raise ValueError('Failed to parse token because there was more than one open bracket in the data string.')
        else:
            data = data[:data.find('[', data.find('[')+1)]
    open = data.find('[')
    close = data.find(']')
    prefix = None
    suffix = None
    tokenparts = None
    if open == -1 and close == -1 and implicit:
        pass
    elif open >= 0 and close >= 0:
        prefix = data[:open]
        suffix = data[close+1:]
        data = data[open+1:close]
    else:
        raise ValueError('Failed to parse token because data string contained mismatched brackets.')
    tokenparts = data.split(':')
    if apply:
        apply.setvalue(tokenparts[0])
        apply.setargs(tokenparts[1:])
        if prefix is not None: apply.setprefix(prefix)
        if suffix is not None: apply.setsuffix(suffix)
        return apply
    else:
        return token.token(
            value = tokenparts[0],
            args = tokenparts[1:],
            prefix = prefix,
            suffix = suffix,
            **kwargs
        )
        
        
        
def parsevariable(*args, **kwargs):
    kwargs['implicit'] = kwargs.get('implicit', True)
    tokens = parseplural(*args, **kwargs)
    return tokens[0] if tokens and len(tokens) == 1 else tokens
    


import token
import tokenlist
