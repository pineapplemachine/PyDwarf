#!/usr/bin/env python
# coding: utf-8

import inspect



class queryable(object):
    '''Classes which contain raws tokens should inherit from this in order to provide querying functionality.'''
    
    query_tokeniter_docstring = '''
        tokeniter: The query runs along this iterable until either a filter has hit
            its limit or the tokens have run out.'''
    
    quick_query_args_docstring = '''
        pretty: Convenience argument which acts as a substitute for directly
            assigning a filter's exact_value and exact_args arguments. Some methods
            also accept an until_pretty argument which acts as a substitute for
            until_exact_value and until_exact_args.
        %s
        **kwargs: If no tokeniter is specified, then arguments which correspond to
            named arguments of the object's tokens method will be passed to that
            method. All other arguments will be passed to the appropriate filters,
            and for accepted arguments you should take a look at the tokenfilter
            constructor's docstring. Some quick query methods support arguments
            prepended with 'until_' to distinguish tokens that should be matched
            from tokens that should terminate the query. (These methods are getuntil,
            getlastuntil, and alluntil. The arguments for the until method should be
            named normally.)
    ''' % query_tokeniter_docstring
            
    def __iter__(self):
        return self.tokens()
    
    def __contains__(self, item):
        if isinstance(item, basestring):
            return self.get(pretty=pretty) is not None
        elif isinstance(item, queryable):
            return item in self.tokens()
    
    def __getitem__(self, item):
        '''Overrides object[...] behavior. Accepts a number of different types for the item argument, each resulting in different behavior.
        
        object[...]
            Returns the same as object.list().
        object[str]
            Returns the same as object.get(str).
        object[int]
            Returns the same as object.index(int).
        object[slice]
            Returns the same as object.slice(slice).
        object[iterable]
            Returns a flattened list containing object[member] in order for each member of iterable.
        object[anything else]
            Raises an exception.
        '''
        if item is Ellipsis:
            return self.list()
        elif isinstance(item, basestring):
            return self.get(pretty=item)
        elif isinstance(item, int):
            return self.index(item)
        elif isinstance(item, slice):
            return self.slice(item)
        elif hasattr(item, '__iter__') or hasattr(item, '__getitem__'):
            return self.getitems(items)
        else:
            raise ValueError('Failed to get item because the argument was of an unrecognized type.')
            
            
            
    builders = {
        'get': (
            # The method's docstring
            'Get the first matching token.',
            
            # Use a generator query by default? Otherwise a list.
            True,
            
            # The first item is for queries without "until" arguments
            (
                # This is the filter index we care about
                0,
                # This is the result index we care about
                # Should be either 0 (the first result), -1 (the last result), or None (all results).
                0,
                # And this function returns the filters to be used with a query
                lambda pretty, conditionargs: (
                    filters.tokenfilter(pretty=pretty, limit=1, **conditionargs),
                ),
            ),
            
            # The second item is for queries which do have "until" arguments
            (
                1, 0, lambda pretty, until, conditionargs, untilargs: (
                    filters.tokenfilter(pretty=until, limit=1, **untilargs),
                    filters.tokenfilter(pretty=pretty, limit=1, **conditionargs)
                ),
            ),
        ),
        
        'last': (
            'Get the last matching token.', True,
            (
                0, -1, lambda pretty, conditionargs: (
                    filters.tokenfilter(pretty=pretty, **conditionargs),
                ),
            ),
            (
                1, -1, lambda pretty, until, conditionargs, untilargs: (
                    filters.tokenfilter(pretty=until, limit=1, **untilargs),
                    filters.tokenfilter(pretty=pretty, **conditionargs)
                ),
            ),
        ),
        
        'all': (
            'Get all matching tokens.', False,
            (
                0, None, lambda pretty, conditionargs: (
                    filters.tokenfilter(pretty=pretty, **conditionargs),
                ),
            ),
            (
                1, None, lambda pretty, until, conditionargs, untilargs: (
                    filters.tokenfilter(pretty=until, limit=1, **untilargs),
                    filters.tokenfilter(pretty=pretty, **conditionargs)
                ),
            ),
        ),
    }
    
    @staticmethod
    def buildqueries():
        '''Internal: Dynamically builds convenience query methods.'''
        
        for queryname, queryproperties in queryable.builders.iteritems():
            docstring, defaultiter, normalfilters, untilfilters = queryproperties
            
            if normalfilters[1] not in (0, -1, None) or untilfilters[1] not in (0, -1, None):
                raise ValueError('Encountered invalid result index %d for convenience query "%s". The accepted values are 0, -1, and None.' % (resultindex, queryname))
            
            querymethod = queryable.buildquerymethod(queryname, docstring, defaultiter, normalfilters, untilfilters)
            setattr(queryable, queryname, querymethod)
        
    @staticmethod
    def buildquerymethod(queryname, docstring, defaultiter, normalfilters, untilfilters):
        def querymethod(self, pretty=None, until=None, tokens=None, iter=None, **kwargs):
            '''%s''' % docstring
            
            tokens, conditionargs, untilargs = self.argstokens(tokens, kwargs)
            
            if iter is None:
                iter = defaultiter
            
            if until or untilargs:
                filterindex, resultindex, filterfunc = untilfilters
                queryfilters = filterfunc(pretty, until, conditionargs, untilargs)
            else:
                filterindex, resultindex, filterfunc = normalfilters
                queryfilters = filterfunc(pretty, conditionargs)
                
            result = self.query(
                filters = queryfilters,
                tokens = tokens, 
                iter = iter
            )
            
            if iter:
                if resultindex is None:
                    return (
                        resulttokens[filterindex] for resulttokens in result if resulttokens[filterindex] is not None
                    )
                        
                elif resultindex == -1:
                    lastresulttoken = None
                    for resulttokens in result:
                        resulttoken = resulttokens[filterindex]
                        if resulttoken is not None: lastresulttoken = resulttoken
                    return lastresulttoken
                        
                else: # resultindex == 0
                    for resulttokens in result:
                        resulttoken = resulttokens[filterindex]
                        if resulttoken is not None: return resulttoken
                    return None
                
            else:
                useresults = result[filterindex]
                if resultindex is None:
                    return useresults
                elif useresults:
                    return result[filterindex][resultindex]
                else:
                    return None
        return querymethod
        
    def argstokens(self, tokens, kwargs):
        '''Internal: Utility function for separating arguments to pass on to a tokens iterator from arguments to pass to filters.'''
        
        conditionargs = kwargs
        untilargs = {}
        tokens = tokens
        
        if tokens is None:
            if hasattr(self, 'tokens') and callable(self.tokens):
                conditionargs, tokensargs = {}, {}
                possibletokensargs = inspect.getargspec(self.tokens)[0]
                for argname, argvalue in kwargs.iteritems():
                    if argname in possibletokensargs:
                        tokensargs[argname] = argvalue
                    elif argname.startswith('until_'):
                        untilargs[argname[6:]] = argvalue
                    else:
                        conditionargs[argname] = argvalue
                tokens = self.tokens(**tokensargs)
            else:
                raise ValueError('Failed to understand query arguments because no tokens iterator could be found or constructed.')
        
        return tokens, conditionargs, untilargs
            
    def getitems(self, items):
        result = []
        for item in items:
            ext = self.__getitem__(item)
            (result.extend if isinstance(ext, list) else result.append)(ext)
        return result
        
    def slice(self, slice):
        return tokenlist.tokenlist(self.islice(slice))
        
    def islice(self, slice):
        root = self.index(slice.start)
        tail = self.index(slice.stop)
        if root is not None and tail is not None:
            for token in root.tokens(include_self=True, step=slice.step, until_token=tail, reverse=root.follows(tail)):
                yield token
        else:
            return

    def query(self, filters, tokens=None, iter=False, **kwargs):
        '''
            Executes a query on some iterable containing tokens.
            Filters are called with the token as the first argument and the number of matches so far for the second argument.
            Each filter should return a tuple with two elements.
            The first element: True if it matches, False if it doesn't.
            The second element: True if the query should be terminated, False to continue.
        '''
        if tokens is None: tokens = self.tokens(**kwargs)
        return self.iquery(filters, tokens) if iter else self.lquery(filters, tokens)
     
    def lquery(self, filters, tokens):
        if callable(filters): filters = (filters,)
        
        try:
            results = {filterkey: tokenlist.tokenlist() for filterkey in filters.iterkeys()}
            filteriter = filters.items()
        except:
            results = [tokenlist.tokenlist() for i in filters]
            filteriter = tuple(enumerate(filters))
        
        limit = False    
        for token in tokens:
            for key, filter in filteriter:
                matches, terminate = filter(token, len(results[key]))
                if matches:
                    results[key].append(token)
                if terminate:
                    limit = True
                    break
            if limit: break
            
        return results
        
    def iquery(self, filters, tokens):
        if callable(filters): filters = (filters,)
            
        try:
            count = {filterkey: 0 for filterkey in filters.iterkeys()}
            filteriter = filters.items()
            newresult = lambda: {}
        except:
            count = [0 for i in filters]
            filteriter = tuple(enumerate(filters))
            newresult = lambda: [None for i in filters]
            
        limit = False
        for token in tokens:
            result = newresult()
            for key, filter in filteriter:
                matches, terminate = filter(token, count[key])
                if matches:
                    result[key] = token
                    count[key] += 1
                if terminate:
                    limit = True
                    break
            yield result
            if limit: break
    
    def get(self, pretty=None, tokeniter=None, **kwargs):
        '''Get the first matching token.
        '''
        
        filter_args, tokens_args = self.oldargstokens(tokeniter, kwargs)
        queryfilters = (
            filters.tokenfilter(pretty=pretty, limit=1, **filter_args)
        ,)
        result = self.query(queryfilters, tokeniter, **tokens_args)[0]
        return result[0] if result else None
    
    def getlast(self, pretty=None, tokeniter=None, **kwargs):
        '''Get the last matching token.
        '''
        
        filter_args, tokens_args = self.oldargstokens(tokeniter, kwargs)
        queryfilters = (
            filters.tokenfilter(pretty=pretty, **filter_args)
        ,)
        result = self.query(queryfilters, tokeniter, **tokens_args)[0]
        return result[-1] if result else None
    
    def all(self, pretty=None, tokeniter=None, **kwargs):
        '''Get a list of all matching tokens.
        '''
        
        filter_args, tokens_args = self.oldargstokens(tokeniter, kwargs)
        queryfilters = (
            filters.tokenfilter(pretty=pretty, **filter_args)
        ,)
        return self.query(queryfilters, tokeniter, **tokens_args)[0]
    
    def until(self, pretty=None, tokeniter=None, **kwargs):
        '''Get a list of all tokens up to a match.
        '''
        
        filter_args, tokens_args = self.oldargstokens(tokeniter, kwargs)
        queryfilters = (
            filters.tokenfilter(pretty=pretty, limit=1, **filter_args),
            filters.tokenfilter()
        )
        return self.query(queryfilters, tokeniter, **tokens_args)[1]
        
    def getuntil(self, pretty=None, until=None, tokeniter=None, **kwargs):
        '''Get the first matching token, but abort when a token matching arguments prepended with 'until_' is encountered.
        '''
        
        filter_args, tokens_args = self.oldargstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        queryfilters = (
            filters.tokenfilter(pretty=until, limit=1, **until_args),
            filters.tokenfilter(pretty=pretty, limit=1, **condition_args)
        )
        result = self.query(queryfilters, tokeniter, **tokens_args)[1]
        return result[0] if result else None
    
    def getlastuntil(self, pretty=None, until=None, tokeniter=None, **kwargs):
        '''Get the last matching token, up until a token matching arguments prepended with 'until_' is encountered.
        '''
        
        filter_args, tokens_args = self.oldargstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        queryfilters = (
            filters.tokenfilter(pretty=until, limit=1, **until_args),
            filters.tokenfilter(pretty=pretty, **condition_args)
        )
        result = self.query(queryfilters, tokeniter, **tokens_args)[1]
        return result[-1] if result else None
     
    def alluntil(self, pretty=None, until=None, tokeniter=None, **kwargs):
        '''Get a list of all matching tokens, but abort when a token matching
        arguments prepended with 'until_' is encountered.
        '''
        
        filter_args, tokens_args = self.oldargstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        queryfilters = (
            filters.tokenfilter(pretty=until, limit=1, **until_args),
            filters.tokenfilter(pretty=pretty, **condition_args)
        )
        return self.query(queryfilters, tokeniter, **tokens_args)[1]
    
    def getprop(self, *args, **kwargs):
        '''Gets the first token matching the arguments, but stops at the next
        token with the same value as this one. Should be sufficient in almost
        all cases to get a token representing a property of an object, when
        this method is called for a token representing an object. **kwargs
        are passed to the getuntil method.
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        return self.get(*args, until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
        
    def getlastprop(self, *args, **kwargs):
        '''Gets the last token matching the arguments, but stops at the next
        token with the same value as this one. Should be sufficient in almost
        all cases to get a token representing a property of an object, when
        this method is called for a token representing an object. **kwargs
        are passed to the getlastuntil method.
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        return self.last(*args, until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
            
    def allprop(self, *args, **kwargs):
        '''Gets the all tokens matching the arguments, but stops at the next
        token with the same value as this one. Should be sufficient in almost
        all cases to get a token representing a property of an object, when
        this method is called for a token representing an object. **kwargs are
        passed to the alluntil method.
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        return self.all(*args, until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
            
    def propdict(self, always_list=True, value_keys=True, full_keys=True, **kwargs):
        '''Returns a dictionary with token values mapped as keys to the tokens
        themselves. If always_list is True then every item in the dict will be
        a list. If it's False then items in the dict where only one token was
        found will be given as individual rawstoken instances rather than as
        lists. **kwargs are passed to the alluntil method.
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        props = self.all(until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
        pdict = {}
        for prop in props:
            for key in (prop.value if value_keys else None, str(prop)[1:-1] if full_keys else None):
                if key is not None:
                    if key not in pdict:
                        if always_list:
                            pdict[key] = tokenlist.tokenlist()
                            pdict[key].append(prop)
                        else:
                            pdict[key] = prop
                    elif prop not in pdict[key]:
                        if isinstance(pdict[key], list):
                            pdict[key].append(prop)
                        else:
                            pdict[key] = tokenlist.tokenlist()
                            pdict[key].append(prop)
                            pdict[key].append(pdict[key], prop)
        return pdict
        
    def list(self, *args, **kwargs):
        '''Convenience method acts as a shortcut for raws.tokenlist.tokenlist(obj.tokens(*args, **kwargs)).
        '''
        return tokenlist.tokenlist(self.tokens(*args, **kwargs))
            
    def removefirst(self, *args, **kwargs):
        token = self.get(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removelast(self, *args, **kwargs):
        token = self.last(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removeall(self, *args, **kwargs):
        tokens = self.all(*args, **kwargs)
        for token in tokens: token.remove()
        return tokens
        
    def removeprop(self, *args, **kwargs):
        token = self.getprop(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removelastprop(self, *args, **kwargs):
        token = self.getlastprop(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removeallprop(self, *args, **kwargs):
        tokens = self.allprop(*args, **kwargs)
        for token in tokens: token.remove()
        return tokens
    
    def argsuntil(self, kwargs):
        '''Internal: Utility function for handling arguments of getuntil and alluntil methods.'''
        until_args, condition_args = {}, {}
        for arg, value in kwargs.iteritems():
            if arg.startswith('until_'):
                until_args[arg[6:]] = value
            else:
                condition_args[arg] = value
        return until_args, condition_args
        
    def oldargstokens(self, tokeniter, kwargs):
        '''Internal: Utility function for separating arguments to pass on to a tokens iterator from arguments to pass to filters.'''
        if tokeniter is None and hasattr(self, 'tokens'):
            filter_args, tokens_args = {}, {}
            args = inspect.getargspec(self.tokens)[0]
            args.append('iter')
            for argname, argvalue in kwargs.iteritems():
                (tokens_args if argname in args else filter_args)[argname] = argvalue
            return filter_args, tokens_args
        else:
            return kwargs, {}
            
    def argsprops(self):
        '''Internal: Utility function for handling arguments of getprop, allprop, and propdict methods.'''
        # TODO: refactor a bit so that the obviated until_exact_value and until_re_value are no longer returned
        until_exact_value = None
        until_re_value = None
        until_value_in = objects.objectsforheader(objects.headerforobject(self.value))
        return until_exact_value, until_re_value, until_value_in

queryable.buildqueries()



import objects
import filters
import tokenlist
