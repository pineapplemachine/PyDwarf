# vim:fileencoding=UTF-8

import inspect

import objects
from filters import rawstokenfilter



class rawsqueryable(object):
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
            and for accepted arguments you should take a look at the rawstokenfilter
            constructor's docstring. Some quick query methods support arguments
            prepended with 'until_' to distinguish tokens that should be matched
            from tokens that should terminate the query. (These methods are getuntil,
            getlastuntil, and alluntil. The arguments for the until method should be
            named normally.)
    ''' % query_tokeniter_docstring
            
    def __iter__(self): return self.tokens()
    
    def __contains__(self, item):
        if isinstance(item, basestring):
            return self.get(pretty=pretty) is not None
        elif isinstance(item, rawsqueryable):
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
            
    def getitems(self, items):
        result = []
        for item in items:
            ext = self.__getitem__(item)
            (result.extend if isinstance(ext, list) else result.append)(ext)
        return result
        
    def slice(self, slice):
        return rawstokenlist(self.islice(slice))
        
    def islice(self, slice):
        root = self.index(slice.start)
        tail = self.index(slice.stop)
        if root is not None and tail is not None:
            for token in root.tokens(include_self=True, step=slice.step, until_token=tail, reverse=root.follows(tail)):
                yield token
        else:
            return
    
    def query(self, filters, tokeniter=None, **kwargs):
        '''Executes a query on some iterable containing tokens.
        
        filters: A dict or other iterable containing rawstokenfilter-like objects.
        %s
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
        
        %s
        
        Example usage:
            >>> print df.get(exact_value='TRANSLATION')
            [TRANSLATION:HUMAN]
            >>> print df.get(exact_args=['6', '0', '1'])
            [PICKED_COLOR:6:0:1]
            >>> bear = df.get(match_token=raws.token('CREATURE:BEAR_GRIZZLY'))
            >>> print bear
            [CREATURE:BEAR_GRIZZLY]
            >>> print bear.get(exact_value='DESCRIPTION')
            [DESCRIPTION:A huge brown creature found in temperate woodland.  It is known for its ferocious attack, usually when it or its young are threatened.]
            >>> print bear.get(exact_value='CREATURE')
            [CREATURE:BEAR_BLACK]
        ''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, limit=1, **filter_args)
        ,)
        result = self.query(filters, tokeniter, **tokens_args)[0].result
        return result[0] if result and len(result) else None
    
    def getlast(self, pretty=None, tokeniter=None, **kwargs):
        '''Get the last matching token.
        
        %s
        
        Example usage:
            >>> dwarven = df['language_DWARF'].get('TRANSLATION:DWARF')
            >>> print dwarven.getlast('T_WORD')
            [T_WORD:PRACTICE:mubun]
        ''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, **filter_args)
        ,)
        result = self.query(filters, tokeniter, **tokens_args)[0].result
        return result[-1] if result and len(result) else None
    
    def all(self, pretty=None, tokeniter=None, **kwargs):
        '''Get a list of all matching tokens.
        
        %s
        
        Example usage:
            >>> dwarven = df['language_DWARF'].get('TRANSLATION:DWARF')
            >>> print dwarven.all(exact_value='T_WORD', re_args=['CR.*Y', None])
                [T_WORD:CRAZY:d�besh]
                [T_WORD:CREEPY:innok]
                [T_WORD:CRUCIFY:memrut]
                [T_WORD:CRY:cagith]
                [T_WORD:CRYPT:momuz]
                [T_WORD:CRYSTAL:zas]
            >>> intelligence = df.all('INTELLIGENT')
            >>> print len(intelligence)
            6
            >>> print [str(token.get('CREATURE', reverse=True)) for token in intelligence]
            ['[CREATURE:DWARF]', '[CREATURE:HUMAN]', '[CREATURE:ELF]', '[CREATURE:GOBLIN]', '[CREATURE:FAIRY]', '[CREATURE:PIXIE]']
        ''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, **filter_args)
        ,)
        return self.query(filters, tokeniter, **tokens_args)[0].result
    
    def until(self, pretty=None, tokeniter=None, **kwargs):
        '''Get a list of all tokens up to a match.
        
        %s
        
        Example usage:
            >>> hematite = df.getobj('INORGANIC:HEMATITE')
            >>> print hematite.until('INORGANIC')
            [USE_MATERIAL_TEMPLATE:STONE_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:hematite][DISPLAY_COLOR:4:7:0][TILE:156]
            [ENVIRONMENT:SEDIMENTARY:VEIN:100]
            [ENVIRONMENT:IGNEOUS_EXTRUSIVE:VEIN:100]
            [ITEM_SYMBOL:'*']
            [METAL_ORE:IRON:100]
            [SOLID_DENSITY:5260]
            [MATERIAL_VALUE:8]
            [IS_STONE]
            [MELTING_POINT:12736]
            >>> print hematite.until('ENVIRONMENT')
            [USE_MATERIAL_TEMPLATE:STONE_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:hematite][DISPLAY_COLOR:4:7:0][TILE:156]
        ''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        filters = (
            rawstokenfilter(pretty=pretty, limit=1, **filter_args),
            rawstokenfilter()
        )
        return self.query(filters, tokeniter, **tokens_args)[1].result
        
    def getuntil(self, pretty=None, until=None, tokeniter=None, **kwargs):
        '''Get the first matching token, but abort when a token matching arguments prepended with 'until_' is encountered.
        
        %s
        
        Example usage:
            >>> hematite = df.getobj('INORGANIC:HEMATITE')
            >>> print hematite.get('METAL_ORE:GOLD:100')
            [METAL_ORE:GOLD:100]
            >>> print hematite.getuntil('METAL_ORE:GOLD:100', 'INORGANIC')
            None
        ''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        filters = (
            rawstokenfilter(pretty=until, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, limit=1, **condition_args)
        )
        result = self.query(filters, tokeniter, **tokens_args)[1].result
        return result[0] if result and len(result) else None
    
    def getlastuntil(self, pretty=None, until=None, tokeniter=None, **kwargs):
        '''Get the last matching token, up until a token matching arguments prepended with 'until_' is encountered.
        
        %s
        
        Example usage:
            >>> hematite = df.getobj('INORGANIC:HEMATITE')
            >>> print hematite.getlast('STATE_NAME_ADJ')
            [STATE_NAME_ADJ:ALL_SOLID:slade]
            >>> print hematite.getlastuntil('STATE_NAME_ADJ', 'INORGANIC')
            [STATE_NAME_ADJ:ALL_SOLID:hematite]
        ''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        filters = (
            rawstokenfilter(pretty=until, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, **condition_args)
        )
        result = self.query(filters, tokeniter, **tokens_args)[1].result
        return result[-1] if result and len(result) else None
     
    def alluntil(self, pretty=None, until=None, tokeniter=None, **kwargs):
        '''Get a list of all matching tokens, but abort when a token matching
        arguments prepended with 'until_' is encountered.
        
        %s
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> print [str(token) for token in dwarf.all('INTELLIGENT')] # Gets all INTELLIGENT tokens following CREATURE:DWARF, including those belonging to other creatures
            ['[INTELLIGENT]', '[INTELLIGENT]', '[INTELLIGENT]', '[INTELLIGENT]', '[INTELLIGENT]', '[INTELLIGENT]']
            >>> print [str(token) for token in dwarf.alluntil('INTELLIGENT', 'CREATURE')] # Gets only the dwarf's INTELLIGENT token
            ['[INTELLIGENT]']
            >>> print [str(token) for token in dwarf.alluntil('INTELLIGENT', 'CREATURE:GOBLIN')]
            ['[INTELLIGENT]', '[INTELLIGENT]', '[INTELLIGENT]']
        ''' % rawsqueryable.quick_query_args_docstring
        
        filter_args, tokens_args = self.argstokens(tokeniter, kwargs)
        until_args, condition_args = self.argsuntil(filter_args)
        filters = (
            rawstokenfilter(pretty=until, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, **condition_args)
        )
        return self.query(filters, tokeniter, **tokens_args)[1].result
    
    def getprop(self, pretty=None, **kwargs):
        '''Gets the first token matching the arguments, but stops at the next
        token with the same value as this one. Should be sufficient in almost
        all cases to get a token representing a property of an object, when
        this method is called for a token representing an object. **kwargs
        are passed to the getuntil method.
        
        Example usage:
            >>> iron = df.getobj('INORGANIC:IRON')
            >>> print iron.get('WAFERS') # Gets the WAFERS token that's a property of adamantite
            [WAFERS]
            >>> print iron.getprop('WAFERS') # Stops at the next INORGANIC token, doesn't pick up adamantine's WAFERS token
            None
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        return self.getuntil(pretty=pretty, until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
        
    def getlastprop(self, pretty=None, **kwargs):
        '''Gets the last token matching the arguments, but stops at the next
        token with the same value as this one. Should be sufficient in almost
        all cases to get a token representing a property of an object, when
        this method is called for a token representing an object. **kwargs
        are passed to the getlastuntil method.
        
        Example usage:
            >>> iron = df.getobj('INORGANIC:IRON')
            >>> print iron.getlast(re_value='ITEMS_.+') # Gets the property of adamantite, the last ITEMS_ token in the file
            [ITEMS_SOFT]
            >>> print iron.getlastprop(re_value='ITEMS_.+') # Gets the last ITEMS_ token which belongs to iron
            [ITEMS_SCALED]
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        return self.getlastuntil(pretty=pretty, until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
            
    def allprop(self, pretty=None, **kwargs):
        '''Gets the all tokens matching the arguments, but stops at the next
        token with the same value as this one. Should be sufficient in almost
        all cases to get a token representing a property of an object, when
        this method is called for a token representing an object. **kwargs are
        passed to the alluntil method.
        
        Example usage:
            >>> hematite = df.getobj('INORGANIC:HEMATITE')
            >>> print len(hematite.all('ENVIRONMENT')) # Gets all ENVIRONMENT tokens following hematite
            38
            >>> print hematite.allprop('ENVIRONMENT') # Gets only the ENVIRONMENT tokens belonging to hematite
            [ENVIRONMENT:SEDIMENTARY:VEIN:100]
            [ENVIRONMENT:IGNEOUS_EXTRUSIVE:VEIN:100]
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        return self.alluntil(pretty=pretty, until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
            
    def propdict(self, always_list=True, value_keys=True, full_keys=True, **kwargs):
        '''Returns a dictionary with token values mapped as keys to the tokens
        themselves. If always_list is True then every item in the dict will be
        a list. If it's False then items in the dict where only one token was
        found will be given as individual rawstoken instances rather than as
        lists. **kwargs are passed to the alluntil method.
        
        Example usage:
            >>> hematite = df.getobj('INORGANIC:HEMATITE')
            >>> props = hematite.propdict()
            >>> print props.get('ENVIRONMENT')
            [ENVIRONMENT:SEDIMENTARY:VEIN:100]
            [ENVIRONMENT:IGNEOUS_EXTRUSIVE:VEIN:100]
            >>> print props.get('IS_STONE')
            [IS_STONE]
            >>> print props.get('TILE:156')
            [TILE:156]
            >>> print props.get('NOT_A_TOKEN')
            None
        '''
        
        until_exact_value, until_re_value, until_value_in = self.argsprops()
        props = self.alluntil(until_exact_value=until_exact_value, until_re_value=until_re_value, until_value_in=until_value_in, **kwargs)
        pdict = {}
        for prop in props:
            for key in (prop.value if value_keys else None, str(prop)[1:-1] if full_keys else None):
                if key is not None:
                    if key not in pdict:
                        if always_list:
                            pdict[key] = rawstokenlist()
                            pdict[key].append(prop)
                        else:
                            pdict[key] = prop
                    elif prop not in pdict[key]:
                        if isinstance(pdict[key], list):
                            pdict[key].append(prop)
                        else:
                            pdict[key] = rawstokenlist()
                            pdict[key].append(prop)
                            pdict[key].append(pdict[key], prop)
        return pdict
        
    def list(self, *args, **kwargs):
        '''Convenience method acts as a shortcut for raws.tokenlist(obj.tokens(*args, **kwargs)).
        
        Example usage:
            >>> elf = df.getobj('CREATURE:ELF')
            >>> print elf
            [CREATURE:ELF]
            >>> print elf.list(range=6, include_self=True)
            [CREATURE:ELF]
                [DESCRIPTION:A medium-sized creature dedicated to the ruthless protection of nature.]
                [NAME:elf:elves:elven]
                [CASTE_NAME:elf:elves:elven]
                [CREATURE_TILE:'e'][COLOR:3:0:0]
        '''
        
        return rawstokenlist(self.tokens(*args, **kwargs))
        
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
                (tokens_args if argname in args else filter_args)[argname] = argvalue
            return filter_args, tokens_args
        else:
            return kwargs, {}
            
    def argsprops(self):
        # Utility function for handling arguments of getprop, allprop, and propdict methods
        # TODO: refactor a bit so that the obviated until_exact_value and until_re_value are no longer returned
        until_exact_value = None
        until_re_value = None
        until_value_in = objects.objectsforheader(objects.headerforobject(self.value))
        return until_exact_value, until_re_value, until_value_in



class rawsqueryableobj(rawsqueryable):
    def __init__(self):
        self.files = None
    
    def getobjheadername(self, type):
        version = self if hasattr(self, 'config') or hasattr(self, 'version') else self.dir
        if type is None:
            return objects.headers(version)
        else:
            return objects.headerforobject(type, version)
    
    def getobj(self, pretty=None, type=None, exact_id=None):
        '''Get the first object token matching a given type and id. (If there's more 
            than one result for any given query then I'm afraid you've done something
            silly with your raws.) This method should work properly with things like
            CREATURE:X tokens showing up in entity_default. Should almost always be
            faster than an equivalent call to get, also.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> print dwarf.list(include_self=True, range=4)
                [CREATURE:DWARF]
                [DESCRIPTION:A short, sturdy creature fond of drink and industry.]
                [NAME:dwarf:dwarves:dwarven]
                [CASTE_NAME:dwarf:dwarves:dwarven]
            >>> not_dwarf = df.getlast('CREATURE:DWARF') # gets the CREATURE:DWARF token underneath ENTITY:MOUNTAIN instead
            >>> print not_dwarf.list(include_self=True, range=4)
                [CREATURE:DWARF]
                [TRANSLATION:DWARF]
                [DIGGER:ITEM_WEAPON_PICK]
                [WEAPON:ITEM_WEAPON_AXE_BATTLE]
        '''
            
        type, exact_id = rawsqueryableobj.objpretty(pretty, type, exact_id)
        for objecttoken in self.getobjheaders(type):
            obj = objecttoken.get(exact_value=type, exact_args=(exact_id,))
            if obj: return obj
        return None
        
    def allobj(self, pretty=None, type=None, exact_id=None, re_id=None, id_in=None):
        '''Gets all objects matching a given type and optional id or id regex.
        
        Example usage:
            >>> pants = df.allobj('ITEM_PANTS')
            >>> print pants
            [ITEM_PANTS:ITEM_PANTS_PANTS]
            [ITEM_PANTS:ITEM_PANTS_GREAVES]
            [ITEM_PANTS:ITEM_PANTS_LEGGINGS]
            [ITEM_PANTS:ITEM_PANTS_LOINCLOTH]
            [ITEM_PANTS:ITEM_PANTS_THONG]
            [ITEM_PANTS:ITEM_PANTS_SKIRT]
            [ITEM_PANTS:ITEM_PANTS_SKIRT_SHORT]
            [ITEM_PANTS:ITEM_PANTS_SKIRT_LONG]
            [ITEM_PANTS:ITEM_PANTS_BRAIES]
            >>> bears = df.allobj(type='CREATURE', re_id='BEAR_.+')
            >>> print bears
            [CREATURE:BEAR_GRIZZLY]
            [CREATURE:BEAR_BLACK]
            [CREATURE:BEAR_POLAR]
            [CREATURE:BEAR_SLOTH]
        '''
        
        type, exact_id = rawsqueryableobj.objpretty(pretty, type, exact_id)
        results = rawstokenlist()
        for objecttoken in self.getobjheaders(type):
            for result in objecttoken.all(
                exact_value = type,
                exact_args = (exact_id,) if exact_id else None,
                re_args = (re_id,) if re_id else None,
                arg_in = ((0, id_in),) if id_in else None,
                args_count = 1
            ):
                results.append(result)
        return results
        
    def objdict(self, *args, **kwargs):
        '''Calls allobj with the same arguments then adds each result to a dictionary
        associating object IDs with the tokens where they're declared.
        
        Example usage:
            >>> inorganics = df.objdict('INORGANIC')
            >>> print len(inorganics)
            263
            >>> print 'NOT_A_ROCK' in inorganics
            False
            >>> obsidian = inorganics.get('OBSIDIAN')
            >>> print obsidian.list(range=6, include_self=True)
            [INORGANIC:OBSIDIAN]
            [USE_MATERIAL_TEMPLATE:STONE_TEMPLATE]
                [MELTING_POINT:13600]
                [BOILING_POINT:16000]
                [IMPACT_YIELD:1000000]
                [IMPACT_FRACTURE:1000000]
        '''
        return {token.args[0]: token for token in self.allobj(*args, **kwargs)}
        
    @staticmethod
    def objpretty(pretty, type, id):
        '''Internal'''
        # Utility method for handling getobj/allobj arguments.
        if pretty is not None:
            if ':' in pretty:
                parts = pretty.split(':')
                if len(parts) != 2: raise ValueError('Failed to parse argument because there were too many or too few colons, there ought to be be just one.')
                return parts[0], parts[1]
            elif type is None:
                return pretty, id
            elif id is None:
                return pretty, type
        else:
            return type, id



class rawstokenlist(list, rawsqueryable):
    '''Extends builtin list with token querying functionality.'''
    
    def tokens(self, range=None, reverse=False):
        for i in xrange(self.__len__()-1, -1, -1) if reverse else xrange(0, self.__len__()):
            if range is not None and range <= count: break
            yield self.__getitem__(i)
            
    def __str__(self):
        if len(self) == 0:
            return ''
        elif len(self) == 1:
            return str(self[0])
        else:
            parts = []
            for token in self:
                if token is not self[0] and ((token.prefix and '\n' in token.prefix)): parts += '\n'
                if token.prefix: parts += token.prefix.split('\n')[-1]
                parts += str(token)
                if token.suffix: parts += token.suffix.split('\n')[0]
                if token is not self[-1] and ((token.suffix and '\n' in token.suffix)): parts += '\n'
            return ''.join(parts)
