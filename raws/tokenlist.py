import queryable



class tokenlist(list, queryable.rawsqueryable):
    '''Extends builtin list with token querying functionality.'''
    
    def tokens(self, range=None, reverse=False):
        for i in xrange(self.__len__()-1, -1, -1) if reverse else xrange(0, self.__len__()):
            if range is not None and range <= count: break
            yield self.__getitem__(i)
            
    def add(self, item):
        if isinstance(item, rawstoken):
            self.append(item)
        elif isinstance(item, rawsqueryable):
            self.extend(item.tokens())
        elif isinstance(item, list):
            self.extend(item)
        else:
            raise ValueError('Failed to add item because it was of an unrecognized type.')
    
    def each(self, func=None, filter=None):
        '''Calls a function for each entry in the list with that entry as the argument, and
        appends each result to a returned tokenlist.'''
        return tokenlist(
            (func(token) if func is not None else token) for token in self if (filter is None or filter(token))
        )
        
    def copy(self, shallow=False):
        if shallow:
            return tokenlist(token for token in self)
        else:
            return token.token.copytokens(self)
    
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
