import re



# Hackish solution to cyclic import
def rawstoken():
    if 'token' not in globals(): import token
    return token.rawstoken



class rawsbasefilter:
    def __init__(self, invert=False):
        self.invert = invert
    def invert(self):
        self.invert = not self.invert
    def match(self, token):
        result = self.basematch(token)
        return not result if self.invert else result
    def basematch(self, token):
        return False



class rawstokenfilter(rawsbasefilter):
    '''Basic filter class for applying to rawstoken objects.'''
    
    def __init__(self,
        pretty=None,
        match_token=None, exact_token=None,
        exact_value=None, exact_args=None, exact_arg=None,
        exact_prefix=None, exact_suffix=None,
        re_value=None, re_args=None, re_arg=None, 
        re_prefix=None, re_suffix=None,
        except_value=None,
        value_in=None, value_not_in=None, args_contains=None, args_count=None,
        invert=None,
        limit=None, limit_terminates=True
    ):
        '''Constructs an element of a query which either matches or doesn't match a given rawstoken.
        Most arguments default to None. If some argument is None then that argument is not matched 
        on.
        
        These arguments regard which tokens match and don't match the filter:
        
        pretty: If specified, the string is parsed as a token and its value and arguments are used
            as exact_value and exact_args.
        match_token: If specified, its value and arguments are used as exact_value and exact_args.
        exact_token: If a token is not this exact object, then it doesn't match.
        exact_value: If a token does not have this exact value, then it doesn't match.
        exact_args: If every one of a token's arguments do not exactly match these arguments, then
            it doesn't match. None values within this tuple- or list-like object are treated as
            wildcards. (These None arguments match everything.)
        exact_arg: An iterable containing tuple- or list-like objects where the first element is
            an index and the second element is a string. If for any index/string pair a token's
            argument at the index does not exactly match the string, then the token doesn't match.
        exact_prefix: If a token does not have this exact prefix - meaning the previous token's
            suffix and its own prefix concatenated - then it doesn't match.
        exact_suffix: If a token does not have this exact suffix - meaning its own suffix and the
            next token's prefix concatenated - then it doesn't match.
        re_value: If a token's value does not match this regular expression, then it doesn't match.
        re_args: If every one of a token's arguments do not match these regular expressions, then
            it doesn't match. None values within this tuple- or list-like object are treated as
            wildcards. (These None arguments match everything.)
        re_arg: An iterable containing tuple- or list-like objects where the first element is an
            index and the second element is a regular expression string. If for any index/regex
            pair a token's argument at the index does not match the regular expression, then the
            token doesn't match.
        re_prefix: If a token's prefix - meaning the previous token's suffix and its own prefix 
            concatenated - does not match this regular expression string then it doesn't match.
        re_suffix: If a token's suffix - meaning its own suffix and the next token's prefix
            concatenated - does not match this regular expression string then it doesn't match.
        except_value: If a token has this exact value, then it doesn't match.
        value_in: If a token's value is not contained within this iterable, then it doesn't match.
        value_not_in: If a token's value is contained within this iterable, then it doesn't match.
        args_contains: If at least one of a token's arguments is not exactly this string, then it
            doesn't match.
        args_count: If a token's number of arguments is not exactly this, then it doesn't match.
        
        These arguments regard how the filter is treated in queries.
        
        invert: Acts like 'not': Inverts what this filter does and doesn't match.
        limit: After matching this many tokens, the filter will cease to accumulate results. If
            limit is None, then the filter will never cease as long as the query continues.
        limit_terminates: After matching the number of tokens indicated by limit, if this is set
            to True then the query of which this filter is a member is made to terminated. If
            set to False, then this filter will only cease to accumulate results. Defaults to
            True.
        '''
        self.pretty = pretty
        if pretty:
            token = rawstoken().parseone(pretty)
            exact_value = token.value
            exact_args = token.args
        if match_token:
            exact_value = match_token.value
            exact_args = match_token.args
        self.exact_token = exact_token
        self.exact_value = exact_value
        self.except_value = except_value
        self.exact_args = exact_args
        self.exact_arg = exact_arg
        self.exact_prefix = exact_prefix
        self.exact_suffix = exact_suffix
        self.re_value = re_value
        self.re_args = re_args
        self.re_arg = re_arg
        self.re_prefix = re_prefix
        self.re_suffix = re_suffix
        self.value_in = value_in
        self.value_not_in = value_not_in
        self.args_contains = args_contains
        self.args_count = args_count
        self.invert = invert
        self.limit = limit
        self.limit_terminates = limit_terminates
        
    def basematch(self, token):
        if (
            (self.exact_token is not None and self.exact_token is not token) or
            (self.except_value is not None and self.except_value == token.value) or
            (self.exact_value is not None and self.exact_value != token.value) or
            (self.args_count is not None and self.args_count != token.nargs()) or
            (self.value_in is not None and token.value not in self.value_in) or
            (self.value_not_in is not None and token.value in self.value_not_in) or
            (self.re_value is not None and re.match(self.re_value, token.value) == None) or
            (self.args_contains is not None and str(self.args_contains) not in [str(a) for a in token.args])
        ):
            return False
        if self.exact_args is not None:
            if not (len(self.exact_args) == token.nargs() and all([self.exact_args[i] == None or str(self.exact_args[i]) == token.args[i] for i in xrange(0, token.nargs())])):
                return False
        if self.exact_arg is not None:
            if not all([a[0]>=0 and a[0]<token.nargs() and token.args[a[0]] == str(a[1]) for a in self.exact_arg]):
                return False
        if self.re_args is not None:
            if not (len(self.re_args) == token.nargs() and all([self.re_args[i] == None or re.match(self.re_args[i], token.args[i]) for i in xrange(0, token.nargs())])):
                return False
        if self.re_arg is not None:
            if not all([a[0]>=0 and a[0]<token.nargs() and re.match(a[1], token.args[a[0]]) for a in self.re_arg]):
                return False
        if self.exact_prefix is not None or self.re_prefix is not None:
            match_prefix = (self.prev.suffix + self.prefix) if self.prev else self.prefix
            if (self.exact_prefix is not None and match_prefix != self.exact_prefix) or (self.re_prefix is not None and re.match(self.re_prefix, match_prefix)):
                return False
        if self.exact_suffix is not None or self.re_suffix is not None:
            match_suffix = (self.suffix + self.next.prefix) if self.next else self.suffix
            if (self.exact_suffix is not None and match_suffix != self.exact_suffix) or (self.re_suffix is not None and re.match(self.re_suffix, match_suffix)):
                return False
        return True
        


class rawsboolfilter(rawsbasefilter):
    '''Logical filter class for combining other filters.'''
    
    def __init__(self, subs, operand=None, invert=None):
        self.subs = subs
        self.operand = operand
        self.invert = invert
        self.args = args
        
    def basematch(self, token):
        if self.operand == 'one':
            count = 0
            for sub in subs:
                count += sub.match(token)
                if count > 1: return False
            return count == 1
        elif self.operand == 'any':
            for sub in subs:
                if sub.match(token): return True
        elif self.operand == 'all':
            for sub in subs:
                if not sub.match(token): return False
            return True
            
    @staticmethod
    def one(subs): return rawsboolfilter(subs, 'one')
    @staticmethod
    def any(subs): return rawsboolfilter(subs, 'any')
    @staticmethod
    def all(subs): return rawsboolfilter(subs, 'all')
    @staticmethod
    def none(subs): return rawsboolfilter(subs, 'all', invert=True)
    