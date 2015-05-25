import os
import re

class rawsqueryable:
    
    def query(self, filters, tokeniter=None, **kwargs):
        '''Executes a query on some iterable containing tokens.
        filters: A dict or other iterable containing rawstokenfilter-like objects.
        tokeniter: The query runs along this iterable until either a filter has hit its limit or the tokens have run out.
        range: The query will stop when it has iterated over this many tokens. If None, the query will not be stopped in this way.
        **kwargs: If tokeniter is not given, then the object's token method will be called with these arguments and used instead.
        '''
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
        
    def get(self, pretty=None, range=None, include_self=False, reverse=False, **kwargs):
        '''Get the first matching token.'''
        filters = (
            rawstokenfilter(pretty=pretty, limit=1, **kwargs)
        ,)
        result = self.query(filters, range=range, include_self=include_self, reverse=reverse)[0].result
        return result[0] if result and len(result) else None
    
    def getlast(self, pretty=None, range=None, include_self=False, reverse=False, **kwargs):
        '''Get the last matching token.'''
        filters = (
            rawstokenfilter(pretty=pretty, **kwargs)
        ,)
        result = self.query(filters, range=range, include_self=include_self, reverse=reverse)[0].result
        return result[-1] if result and len(result) else None
    
    def all(self, pretty=None, range=None, include_self=False, reverse=False, **kwargs):
        '''Get a list of all matching tokens.'''
        filters = (
            rawstokenfilter(pretty=pretty, **kwargs)
        ,)
        return self.query(filters, range=range, include_self=include_self, reverse=reverse)[0].result
    
    def until(self, pretty=None, range=None, include_self=False, reverse=False, **kwargs):
        '''Get a list of all tokens up to a match.'''
        filters = (
            rawstokenfilter(),
            rawstokenfilter(pretty=pretty, limit=1, **kwargs)
        )
        return self.query(filters, range=range, include_self=include_self, reverse=reverse)[0].result
        
    def getuntil(self, pretty=None, until_pretty=None, range=None, include_self=False, reverse=False, **kwargs):
        '''Get the first matching token, but abort when a token matching arguments prepended with 'until_' is encountered.'''
        until_args, condition_args = self.argsuntil(**kwargs)
        filters = (
            rawstokenfilter(pretty=until_pretty, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, limit=1, **condition_args)
        )
        result = self.query(filters, range=range, include_self=include_self, reverse=reverse)[1].result
        return result[0] if result and len(result) else None
    
    def getlastuntil(self, pretty=None, until_pretty=None, range=None, include_self=False, reverse=False, **kwargs):
        '''Get the last matching token, up until a token matching arguments prepended with 'until_' is encountered.'''
        until_args, condition_args = self.argsuntil(**kwargs)
        filters = (
            rawstokenfilter(pretty=until_pretty, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, **condition_args)
        )
        result = self.query(filters, range=range, include_self=include_self, reverse=reverse)[1].result
        return result[-1] if result and len(result) else None
     
    def alluntil(self, pretty=None, until_pretty=None, range=None, include_self=False, reverse=False, **kwargs):
        '''Get a list of all matching tokens, but abort when a token matching arguments prepended with 'until_' is encountered.'''
        until_args, condition_args = self.argsuntil(**kwargs)
        filters = (
            rawstokenfilter(pretty=until_pretty, limit=1, **until_args),
            rawstokenfilter(pretty=pretty, **condition_args)
        )
        return self.query(filters, range=range, include_self=include_self, reverse=reverse)[1].result
        
    def argsuntil(self, **kwargs):
        # utility function for handling arguments of getuntil and alluntil methods
        until_args, condition_args = {}, {}
        for arg, value in kwargs.iteritems():
            if arg.startswith('until_'):
                until_args[arg[6:]] = value
            else:
                condition_args[arg] = value
        return until_args, condition_args

class raws:
    '''Represents as a whole all the raws contained within a directory.'''
    
    def __init__(self):
        '''Constructor for raws object.'''
        self.files = {}
        
    def getfile(self, filename):
        return self.files.get(filename)
    def addfile(self, filename=None, rfile=None):
        if rfile and not filename: filename = rfile.header
        if filename in self.files: raise KeyError
        if not rfile: rfile = rawsfile(header=filename)
        self.files[filename] = rfile
        return rfile
    def setfile(self, filename=None, rfile=None):
        if rfile and not filename: filename = rfile.header
        self.files[filename] = rfile
    def removefile(self, filename=None, rfile=None):
        if rfile and not filename: filename = rfile.header
        del self.files[filename]
    def __getitem__(self, name): return self.getfile(name)
    def __setitem__(self, name, value): return self.setfile(name, value)
    
    '''
    Read raws from some directory.
    If no directory is specified, reads from a dfrawsdir attribute that can be indirectly specified in the constructor.
    '''
    def read(self, dir, log=None):
        for filename in os.listdir(dir):
            path = os.path.join(dir, filename)
            if filename.endswith('.txt') and os.path.isfile(path):
                if log: log.debug('Reading file %s...' % path)
                with open(path, 'rb') as rfile:
                    filenamekey = os.path.splitext(os.path.basename(path))[0]
                    self.files[filenamekey] = rawsfile(path=path, rfile=rfile)
        return self
                
    '''
    Save raws to some directory.
    If no directory is specified, saves to a dfrawsdir attribute that can be indirectly specified in the constructor.
    Be careful! You should back up your raws before overwriting them in this way.
    '''
    def write(self, dir, log=None):
        for filename in self.files:
            path = os.path.join(dir, filename)
            if not path.endswith('.txt'): path += '.txt'
            with open(path, 'wb') as rfile:
                if log: log.debug('Writing file %s...' % path)
                self.files[filename].write(rfile)
        return self
    
    '''
    Get the first matching token.
    '''
    def get(self, pretty=None, **kwargs):
        for filename in self.files:
            got = self.files[filename].get(pretty=pretty, **kwargs)
            if got: return got
        return None
        
    '''
    Get a list of all matching tokens.
    '''
    def all(self, pretty=None, **kwargs):
        got = []
        for filename in self.files:
            got += self.files[filename].all(pretty=pretty, **kwargs)
        return got
    
    '''
    Iterate through all tokens in order.
    '''
    def tokens(self):
        for filename in self.files:
            for token in self.files[filename].tokens():
                yield token
             
    @staticmethod
    def pretty(data, implicitbraces=True):
        tokens = [] # maintain a sequential list of tokens
        pos = 0     # byte position in data
        if data.find('[') == -1 and data.find(']') == -1:
            if implicitbraces:
                tokenparts = data.split(':')
                token = rawstoken(
                    value=tokenparts[0],
                    args=tokenparts[1:],
                )
                return [token]
            else:
                raise ValueError
        else:
            while pos < len(data):
                token = None
                open = data.find('[', pos)
                if open >= 0 and open < len(data):
                    close = data.find(']', pos)
                    if close >= 0 and close < len(data):
                        prefix = data[pos:open]
                        tokentext = data[open+1:close]
                        tokenparts = tokentext.split(':')
                        token = rawstoken(
                            value=tokenparts[0],
                            args=tokenparts[1:],
                            prefix=prefix,
                            prev=tokens[-1] if len(tokens) else None
                        )
                        pos = close+1
                if token:
                    if len(tokens): tokens[-1].next = token
                    tokens.append(token)
                else:
                    break
            if len(tokens) and pos<len(data):
                tokens[-1].suffix = data[pos:]
            return tokens

class rawsfile(rawsqueryable):
    def __init__(self, header=None, data=None, path=None, tokens=None, rfile=None):
        if rfile:
            self.read(rfile)
            if header is not None: self.header = header
            if data is not None: self.data = data
        else:
            self.header = header
            self.data = data
        self.path = path
        self.roottoken = None
        self.tailtoken = None
        if self.data:
            tokens = raws.pretty(self.data, implicitbraces=False)
        if tokens:
            self.settokens(tokens)
    def settokens(self, tokens):
        self.roottoken, self.tailtoken = rawstoken.firstandlast(tokens)
    def __str__(self):
        return '%s\n%s' %(self.header, ''.join([str(o) for o in self.tokens()]))
    def __repr__(self):
        return '%s\n%s' %(self.header, ''.join([repr(o) for o in self.tokens()]))
        
    def root(self):
        while self.roottoken and self.roottoken.prev: self.roottoken = self.roottoken.prev
        return self.roottoken
    def tail(self):
        while self.tailtoken and self.tailtoken.next: self.tailtoken = self.tailtoken.next
        return self.tailtoken
        
    def tokens(self, range=None, include_self=False, reverse=False):
        if include_self: raise ValueError
        count = 0
        itrtoken = self.tail() if reverse else self.root()
        while itrtoken and (range is None or range > count):
            yield itrtoken
            itrtoken = itrtoken.prev if reverse else itrtoken.next
            count += 1
            
    def read(self, rfile):
        self.header, self.data = rfile.readline().strip(), rfile.read()
    def write(self, rfile):
        rfile.write(self.__repr__())
    
    def add(self, auto=None, pretty=None, token=None, tokens=None, **kwargs):
        tail = self.tail()
        if tail:
            return tail.add(auto=auto, pretty=pretty, token=token, tokens=tokens, **kwargs)
        else:
            pretty, token, tokens = rawstoken.auto(auto, pretty, token, tokens)
            if pretty:
                tokens = raws.pretty(tokens)
                if len(tokens) == 1: token = tokens
            if token:
                self.headtoken = token
                self.tailtoken = token
                return token
            elif tokens:
                self.settokens(tokens)
                return tokens
        
class rawstoken(rawsqueryable):
    @staticmethod
    def auto(auto, pretty, token, tokens):
        # Convenience function for handling method arguments
        if auto is not None:
            if isinstance(auto, basestring): pretty = auto
            elif isinstance(auto, rawstoken): token = auto
            elif isinstance(auto, rawsfile) or isinstance(auto, raws): tokens = auto.tokens()
            else: tokens = auto
        return pretty, token, tokens
        
    def __init__(self, auto=None, pretty=None, token=None, value=None, args=None, prefix=None, suffix=None, prev=None, next=None):
        pretty, token, tokens = rawstoken.auto(auto, pretty, token, None)
        if tokens is not None: raise ValueError
        if pretty:
            prettytokens = raws.pretty(pretty, implicitbraces=True)
            if len(prettytokens) != 1: raise ValueError
            token = prettytokens[0]
        if token:
            value = token.value
            args = list(token.args) if token.args else []
            prefix = token.prefix
            suffix = token.suffix
        # tokens look like this: [value:arg1:arg2:...:argn]
        self.prev = prev            # previous token sequentially
        self.next = next            # next token sequentially
        self.value = value          # value for the token
        self.args = args            # arguments for the token
        self.prefix = prefix        # non-token text between the preceding token and this one
        self.suffix = suffix        # between this token and the next/eof (should typically apply to eof)
        if not self.args: self.args = []
    
    def nargs(self):
        '''Returns the number of arguments the token has. (Length of arguments list.)'''
        return len(self.args)
        
    def __str__(self):
        return '[%s%s]' %(self.value, (':%s' % ':'.join([str(a) for a in self.args])) if self.args and len(self.args) else '')
    def __repr__(self):
        return '%s%s%s' % (self.prefix if self.prefix else '', str(self), self.suffix if self.suffix else '')
    
    @staticmethod
    def copy(subject=None):
        '''Copies some token or iterable collection of tokens.'''
        if isinstance(subject, rawstoken):
            return rawstoken(token=subject)
        elif subject is not None:
            copied = []
            prevtoken = None
            for token in subject:
                newtoken = rawstoken(token=token)
                copied.append(newtoken)
                newtoken.prev = prevtoken
                if prevtoken: prevtoken.next = newtoken
                prevtoken = newtoken
            return copied
        else:
            raise ValueError
        
    def tokens(self, range=None, include_self=False, reverse=False):
        count = 0
        itertoken = self if include_self else (self.prev if reverse else self.next)
        while itertoken and (range is None or range > count):
            yield itertoken
            itertoken = itertoken.prev if reverse else itertoken.next
            count += 1
            
    def match(self, pretty=None, **kwargs):
        '''Returns True if this method matches some rawstokenfilter, false otherwise.'''
        return rawstokenfilter(pretty=pretty, **kwargs).match(self)
        
    def add(self, auto=None, pretty=None, token=None, tokens=None, reverse=False):
        '''Adds a token or tokens nearby this one. If reverse is False the token 
        or tokens are added immediately after. If it's True, they are added before.
        
        auto: When the first argument is specified the intended assignment will be
            detected automatically. If a rawstoken is specified it will be treated
            as a token argument. If a string, pretty. If anything else, tokens.
        pretty: Parses the string and adds the tokens within it.
        token: Adds this one token.
        tokens: Adds all of these tokens.
        '''
        pretty, token, tokens = rawstoken.auto(auto, pretty, token, tokens)
        if pretty:
            return self.addall(raws.pretty(pretty), reverse)
        elif tokens:
            return self.addall(tokens, reverse)
        elif token:
            return self.addone(token if token else rawstoken(pretty=pretty), reverse)
        else:
            raise ValueError
    
    @staticmethod
    def firstandlast(tokens):
        # Utility method for getting the first and last items of some iterable
        try:
            return tokens[0], tokens[-1]
        except:
            first, last = None, None
            for token in tokens:
                if first is not None: first = token
                last = token
            return first, last            
        
    def addone(self, token, reverse=False):
        # Utility method called by add when adding a single token
        if reverse:
            token.next = self
            token.prev = self.prev
            if self.prev: self.prev.next = token
            self.prev = token
        else:
            token.prev = self
            token.next = self.next
            if self.next: self.next.prev = token
            self.next = token
        return token
    def addall(self, tokens, reverse=False):
        # Utility method called by add when adding multiple tokens
        first, last = rawstoken.firstandlast(tokens)
        if reverse:
            last.next = self
            first.prev = self.prev
            if self.prev: self.prev.next = first
            self.prev = last
        else:
            first.prev = self
            last.next = self.next
            if self.next: self.next.prev = tokens[-1]
            self.next = first
        return tokens
    
    def remove(self, count=0, reverse=False):
        '''Removes this token and the next count tokens in the direction indicated by reverse.'''
        left = self.prev
        right = self.next
        if count:
            token = self.prev if reverse else self.next
            while count and token:
                count -= 1
                token = token.prev if reverse else token.next
            if reverse:
                left = token
            else:
                right = token
        if left: left.next = right
        if right: right.prev = left
        return self

class rawstokenlist(list, rawsqueryable):
    '''Extends list with token querying functionality.'''
    def tokens(self, range=None, include_self=False, reverse=False):
        if include_self: raise ValueError
        for i in xrange(self.__len__()-1, -1, -1) if reverse else xrange(0, self.__len__()):
            if range is not None and range <= count: break
            yield self.__getitem__(i)

class rawstokenfilter:
    def __init__(self,
        pretty=None,
        match_token=None, exact_token=None,
        exact_value=None, exact_args=None, exact_arg=None,
        exact_prefix=None, exact_suffix=None,
        re_value=None, re_args=None, re_arg=None, 
        re_prefix=None, re_suffix=None,
        except_value=None,
        value_in=None, value_not_in=None, args_contains=None, args_count=None,
        anti=None,
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
        
        limit: After matching this many tokens, the filter will cease to accumulate results. If
            limit is None, then the filter will never cease as long as the query continues.
        limit_terminates: After matching the number of tokens indicated by limit, if this is set
            to True then the query of which this filter is a member is made to terminated. If
            set to False, then this filter will only cease to accumulate results. Defaults to
            True.
        '''
        self.pretty = pretty
        if pretty:
            token = rawstoken(pretty=pretty)
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
        self.anti = anti
        self.limit = limit
        self.limit_terminates = limit_terminates
    @staticmethod
    def anti(**kwargs): return rawstokenfilter(anti=True, **kwargs)
    def match(self, token):
        result = self.basematch(token)
        return not result if self.anti else result
    def basematch(self, token):
        if (
            (self.exact_token is not None and self.exact_token != token) or
            (self.except_value is not None and self.except_value == token) or
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

class rawsboolfilter(rawstokenfilter):
    def __init__(self, subs, operand=None, anti=None, *args):
        self.subs = subs
        self.operand = operand
        self.anti = anti
        self.args = args
    def basematch(self, token):
        if self.operand == 'one':
            count = 0
            for sub in subs:
                count += sub.match(token)
                if count > 1: return False
            return count == 1
        elif self.operand == 'count' and self.args and len(self.args) == 1:
            count = 0
            for sub in subs:
                count += sub.match(token)
                if count > self.args[0]: return False
            return count == self.args[0]
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
    def none(subs): return rawsboolfilter(subs, 'all', anti=True)
    @staticmethod
    def count(subs, number): return rawsboolfilter(subs, 'count', number)
    