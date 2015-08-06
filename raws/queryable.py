#!/usr/bin/env python
# coding: utf-8

import numbers
import inspect



class queryable(object):
    '''Classes which contain raws tokens should inherit from this in order to provide querying functionality.'''
    
    def __iter__(self):
        '''Iterate through the object's tokens.'''
        return self.itokens()
    
    def __contains__(self, item):
        '''Check if some matching token can be found.'''
        if isinstance(item, basestring):
            return self.get(pretty=item) is not None
        elif isinstance(item, token.token):
            return any(item is checktoken for checktoken in self.itokens())
        elif callable(item):
            for result in self.query(filters=item, iter=True):
                if any(item is not None for item in result):
                    return True
            return False
        else:
            try:
                return all(self.__contains__(i) for i in item)
            except:
                raise ValueError('Failed to check for containment of object because its type %s was unrecognized.' % type(item))
    
    def __eq__(self, other):
        '''Check for equivalency.'''
        return self.equals(other)
    def __ne__(self, other):
        '''Check for inequivalency.'''
        return not self.equals(other)
    
    def __str__(self):
        '''Get a string representation.'''
        return helpers.tokensstring(self.itokens())
    
    def __reversed__(self):
        return self.tokens(reverse=True)
    
    def __getitem__(self, *args, **kwargs):
        return self.getitem(*args, **kwargs)
            
    def getitem(self, item, singular=True, plural=True):
        '''
            Accepts a number of different types for the item argument, each
            resulting in different behavior.
            
            An ellipsis returns self.list().
            A string returns self.get(str).
            A number returns self.index(number).
            A token returns self.get(match_token=token).
            A slice returns self.slice(slice).
            A callable object will be treated as a filter and the result of a
            query will be returned.
            Any other iterable returns a flattened list containing self[item]
            for each item in the iterable.
            Anything else will cause an exception.
        '''
        
        singularresult = None
        pluralresult = None
        
        if item is Ellipsis:
            pluralresult = self.list()
        elif item is None:
            if plural:
                pluralresult = tokenlist.tokenlist()
            else:
                singularresult = None
        elif isinstance(item, basestring):
            singularresult = self.get(pretty=item)
        elif isinstance(item, token.token):
            singularresult = self.get(match_token=item)
        elif isinstance(item, numbers.Number):
            singularresult = self.index(item)
        elif isinstance(item, slice):
            pluralresult = self.slice(item)
        elif callable(item):
            pluralresult = self.query(item)[0]
        elif hasattr(item, '__iter__') or hasattr(item, '__getitem__'):
            pluralresult = self.getitems(item)
        else:
            raise TypeError('Failed to get item because the argument was of an unrecognized type %s.' % type(item))
            
        if singularresult is not None:
            if singular:
                return singularresult
            else:
                tokens = tokenlist.tokenlist()
                tokens.append(singularresult)
                return tokens
                
        if pluralresult is not None:
            if plural:
                return pluralresult
            elif len(pluralresult) == 0:
                return None
            elif len(pluralresult) == 1:
                return pluralresult[0]
            else:
                raise ValueError('Failed to get item because a multiple items were found where a single return value was expected.')
          
    builders = {
        'get': (
            # The method's docstring
            'Get the first matching token.',
            
            # Use a generator query by default? Otherwise build a list.
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
        '''Internal: Dynamically builds convenience query methods.'''
        
        def querymethod(self, pretty=None, until=None, tokens=None, iter=None, filters=None, **kwargs):
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
            
            if filters is not None:
                if callable(filters): filters = (filters,)
                queryfilters = queryfilters + filters
                
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
        
        querymethod.__name__ = queryname
        return querymethod
        
    def argstokens(self, tokens, kwargs):
        '''
            Internal: Utility function for separating arguments to pass on to a
            tokens iterator from arguments to pass to filters.
        '''
        
        conditionargs = kwargs
        untilargs = {}
        tokens = tokens
        
        if tokens is None:
            if hasattr(self, 'tokens') and callable(self.itokens):
                conditionargs, tokensargs = {}, {}
                possibletokensargs = ('range', 'reverse', 'until', 'step', 'skip') # inspect.getargspec(self.itokens)[0]
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
        '''
            Internal: Used by getitem to flatten lists when an iterable, most
            relevant being tuples, are recieved as an argument.
        '''
        result = tokenlist.tokenlist()
        for item in items:
            result.append(self.getitem(item))
        return result
    
    def slice(self, slice, iter=False):
        '''Get tokens from one to another inclusive.'''
        return tokengenerator.tokengenerator(self.islice(slice)) if iter else self.lslice(slice)
        
    def lslice(self, *args, **kwargs):
        '''Internal: Get a slice as a tokenlist.'''
        return tokenlist.tokenlist(self.islice(*args, **kwargs))
        
    def islice(self, slice):
        '''Internal: Get a slice as a generator.'''
        root = self.getitem(slice.start, plural=False)
        tail = self.getitem(slice.stop, plural=False)
        if root is not None and tail is not None:
            for token in root.tokens(skip=False, step=slice.step, until=tail, reverse=root.follows(tail)):
                yield token

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
        '''Internal: Called by the query method when the iter argument is False.'''
        
        if callable(filters): filters = (filters,)
        
        try:
            results = {filterkey: tokenlist.tokenlist() for filterkey in filters.iterkeys()}
            filteriter = filters.items()
            resultcontainer = queryresult.queryresult(self, results, results.items())
        except:
            results = [tokenlist.tokenlist() for i in filters]
            filteriter = tuple(enumerate(filters))
            resultcontainer = queryresult.queryresult(self, results)
        
        limit = False    
        for token in tokens:
            for key, filter in filteriter:
                try:
                    returned = filter(token, len(results[key]))
                except:
                    returned = filter(token)
                try:
                    matches, terminate = returned
                except:
                    matches, terminate = returned, False
                if matches:
                    results[key].append(token)
                if terminate:
                    limit = True
                    break
            if limit: break
            
        return resultcontainer
        
    def iquery(self, filters, tokens):
        '''Internal: Called by the query method when the iter argument is True.'''
        
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
                try:
                    returned = filter(token, count[key])
                except:
                    returned = filter(token)
                try:
                    matches, terminate = returned
                except:
                    matches, terminate = returned, False
                if matches:
                    result[key] = token
                    count[key] += 1
                if terminate:
                    limit = True
                    break
            yield result
            if limit: break
            
    def tokens(self, *args, **kwargs):
        '''Get tokens as a tokengenerator.'''
        return tokengenerator.tokengenerator(self.itokens, *args, **kwargs)
            
    def list(self, *args, **kwargs):
        '''
            Returns the same as the object's tokens method, but in the form of
            a tokenlist instead of a generator.
        '''
        return tokenlist.tokenlist(self.itokens(*args, **kwargs))
        
    def each(self, func=None, filter=None, iter=None, output=None, none=False):
        '''
            Call a function for each entry in the list with that entry as the
            argument and return the results as the given output type or, if no
            such class is provided, as the same class as this object.
        '''
        
        if iter is None: iter = self.itokens()
        
        def gen():
            for token in iter:
                if filter is None or filter(token):
                    if func:
                        result = func(token)
                    else:
                        result = token
                    if none or result is not None:
                        yield result
        
        if output is None: output = type(self)
        return output(gen())
        
    def equals(self, other):
        '''Check for equivalency with another iterable of tokens.'''
        return helpers.tokensequal(self.itokens(), other)
            
    def removefirst(self, *args, **kwargs):
        '''Remove the first token matching a filter.'''
        token = self.get(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removelast(self, *args, **kwargs):
        '''Remove the last token matching a filter.'''
        token = self.last(*args, **kwargs)
        if token is not None: token.remove()
        return token
    def removeall(self, *args, **kwargs):
        '''Remove all tokens matching some filter.'''
        tokens = self.all(*args, **kwargs)
        for token in tokens: token.remove()
        return tokens
    
queryable.buildqueries()



import queryresult
import objects
import filters
import tokenlist
import tokengenerator
import token
import helpers
