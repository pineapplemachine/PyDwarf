import inspect
from filters import *



class rawsqueryable:
    '''Classes which contain raws tokens should inherit from this in order to provide querying functionality.'''
    
    query_tokeniter_docstring = '''
        tokeniter: The query runs along this iterable until either a filter has hit
            its limit or the tokens have run out.'''
    
    quick_query_args_docstring = '''
        %s
        pretty: Convenience argument which acts as a substitute for directly
            assigning a filter's exact_value and exact_args arguments. Some methods
            also accept an until_pretty argument which acts as a substitute for
            until_exact_value and until_exact_args.
        **kwargs: If no tokeniter is specified, then arguments which correspond to
            named arguments of the object's tokens method will be passed to that
            method. All other arguments will be passed to the appropriate filters,
            and for accepted arguments you should take a look at the rawstokenfilter
            constructor's docstring. Some quick query methods support arguments
            prepended with 'until_' to distinguish tokens that should be matched
            from tokens that should terminate the query. (These methods are getuntil,
            getlastuntil, and alluntil. The arguments for the until method should be
            named normally.)
    ''' % query_tokeniter_docstring
    
    def __getitem__(self, pretty): return self.get(pretty=pretty)
    def __iter__(self): return self.tokens()
    def __contains__(self, pretty): return self.get(pretty=pretty) is not None
    
    def query(self, filters, tokeniter=None, **kwargs):
        '''Executes a query on some iterable containing tokens.
        
        %s
        filters: A dict or other iterable containing rawstokenfilter-like objects.
        **kwargs: If tokeniter is not given, then the object's token method will be
            called with these arguments and used instead.
        ''' % rawsqueryable.query_tokeniter_docstring
        
        if tokeniter is None: tokeniter = self.tokens(**kwargs)
        filteriter = (filters.itervalues() if isinstance(filters, dict) else filters)
        limit = False
        for filter in filteriter: filter.result = rawstokenlist()
        for token in tokeniter:
            for filter in filteriter:
                if (not filter.limit) or len(filter.result) < filter.limit:
                    if filter.match(token): filter.result.append(token)
                    if filter.limit_terminates and len(filter.result) == filter.limit: limit = True; break
            if limit: break
        return filters
        
    def get(self, pretty=None, tokeniter=None, **kwargs):
        '''Get the first matching token.
        %s''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, limit=1, **filter_args)
        ,)
        result = self.query(filters, tokeniter, **tokens_args)[0].result
        return result[0] if result and len(result) else None
    
    def getlast(self, pretty=None, tokeniter=None, **kwargs):
        '''Get the last matching token.
        %s''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, **filter_args)
        ,)
        result = self.query(filters, tokeniter, **tokens_args)[0].result
        return result[-1] if result and len(result) else None
    
    def all(self, pretty=None, tokeniter=None, **kwargs):
        '''Get a list of all matching tokens.
        %s''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, **filter_args)
        ,)
        return self.query(filters, tokeniter, **tokens_args)[0].result
    
    def until(self, pretty=None, tokeniter=None, **kwargs):
        '''Get a list of all tokens up to a match.
        %s''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, limit=1, **filter_args),
            rawstokenfilter()
        )
        return self.query(filters, tokeniter, **tokens_args)[1].result
        
    def getuntil(self, pretty=None, until_pretty=None, tokeniter=None, **kwargs):
        '''Get the first matching token, but abort when a token matching arguments prepended with 'until_' is encountered.
        %s''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        filters = (
            rawstokenfilter(pretty=until_pretty, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, limit=1, **condition_args)
        )
        result = self.query(filters, tokeniter, **tokens_args)[1].result
        return result[0] if result and len(result) else None
    
    def getlastuntil(self, pretty=None, until_pretty=None, tokeniter=None, **kwargs):
        '''Get the last matching token, up until a token matching arguments prepended with 'until_' is encountered.
        %s''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        filters = (
            rawstokenfilter(pretty=until_pretty, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, **condition_args)
        )
        result = self.query(filters, tokeniter, **tokens_args)[1].result
        return result[-1] if result and len(result) else None
     
    def alluntil(self, pretty=None, until_pretty=None, tokeniter=None, **kwargs):
        '''Get a list of all matching tokens, but abort when a token matching arguments prepended with 'until_' is encountered.
        %s''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        filters = (
            rawstokenfilter(pretty=until_pretty, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, **condition_args)
        )
        return self.query(filters, tokeniter, **tokens_args)[1].result
    
    def argsuntil(self, kwargs):
        # Utility function for handling arguments of getuntil and alluntil methods
        until_args, condition_args = {}, {}
        for arg, value in kwargs.iteritems():
            if arg.startswith('until_'):
                until_args[arg[6:]] = value
            else:
                condition_args[arg] = value
        return until_args, condition_args
        
    def argstokens(self, tokeniter, kwargs):
        # Utility function for separating arguments to pass on to a tokens iterator from arguments to pass to filters
        if tokeniter is None and hasattr(self, 'tokens'):
            filter_args, tokens_args = {}, {}
            args = inspect.getargspec(self.tokens)[0]
            for argname, argvalue in kwargs.iteritems():
                (token_args if argname in args else filter_args)[argname] = argvalue
            return filter_args, tokens_args
        else:
            return kwargs, {}



class rawsqueryable_obj(rawsqueryable):
    def __init__(self):
        self.files = None
    
    def getobjheadername(self, type):
        if type == 'WORD' or type == 'SYMBOL':
            return 'LANGUAGE'
        elif type.startswith('ITEM_'):
            return 'ITEM'
        elif type == 'COLOR' or type == 'SHAPE':
            return 'DESCRIPTOR_%s' % type
        elif type == 'COLOR_PATTERN':
            return 'DESCRIPTOR_PATTERN'
        else:
            return type
    
    def getobjheaders(self, type):
        '''Gets OBJECT:X tokens where X is type. Is also prepared for special cases
        like type=ITEM_PANTS matching OBJECT:ITEM. Current as of DF version 0.40.24.'''
        match_type = self.getobjheadername(type)
        results = []
        for rfile in self.files.itervalues():
            root = rfile.root()
            if root and root.value == 'OBJECT' and root.nargs() == 1 and root.args[0] == match_type:
                results.append(root)
        return results
    
    def getobj(self, type, id):
        '''Get the first object token matching a given type and id. (If there's more 
            than one result for any given query then I'm afraid you've done something
            silly with your raws.) This method should work properly with things like
            CREATURE:X tokens showing up in entity_default.'''
        for objecttoken in self.getobjheaders(type):
            obj = objecttoken.get(exact_value=type, exact_args=(id,))
            if obj: return obj
        return None
        
    def allobj(self, type, exact_id=None, re_id=None):
        '''Gets all objects matching a given type and optional id or id regex.'''
        results = []
        for objecttoken in self.getobjheaders(type):
            for result in objecttoken.all(exact_value=type, exact_args=(exact_id,) if exact_id else None, re_args=(re_id,) if re_id else None):
                results.append(result)
        return results
        
    def objdict(self, *args, **kwargs):
        return {token.args[0]: token for token in self.allobj(*args, **kwargs)}



class rawstokenlist(list, rawsqueryable):
    '''Extends builtin list with token querying functionality.'''
    
    def tokens(self, range=None, include_self=False, reverse=False):
        if include_self: raise ValueError
        for i in xrange(self.__len__()-1, -1, -1) if reverse else xrange(0, self.__len__()):
            if range is not None and range <= count: break
            yield self.__getitem__(i)


