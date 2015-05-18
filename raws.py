import os
import re

class raws:
    def __init__(self, dfdir=None):
        self.dfdir = dfdir
        self.dfrawsdir = os.path.join(dfdir, 'raw/objects')
        self.files = {}
        
    def readfile(self, path):
        with open(path, 'rb') as rfile:
            self.files[os.path.basename(path)] = rawsfile(path, rfile)
    def addfile(self, filename):
        self.files[filename] = rawsfile(parse=False)
    
    '''
    Read raws from some directory.
    If no directory is specified, reads from a dfrawsdir attribute that can be indirectly specified in the constructor.
    '''
    def read(self, dir=None, verbose=None):
        if not dir: dir = self.dfrawsdir
        for filename in os.listdir(dir):
            path = os.path.join(dir, filename)
            if filename.endswith('.txt') and os.path.isfile(path):
                if verbose: print verbose % path
                self.readfile(path)
        return self
                
    '''
    Save raws to some directory.
    If no directory is specified, saves to a dfrawsdir attribute that can be indirectly specified in the constructor.
    Be careful! You should back up your raws before overwriting them in this way.
    '''
    def write(self, dir=None, verbose=None):
        if not dir: dir = self.dfrawsdir
        for filename in self.files:
            path = os.path.join(dir, filename)
            with open(path, 'wb') as rfile:
                if verbose: print verbose % path
                rfile.write(repr(self.files[filename]))
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

class rawsfile:
    def __init__(self, path=None, rfile=None):
        self.path = path
        self.objects, self.objecttypes, self.data, self.header = None, None, None, None
        if rfile: self.header, self.data = rfile.readline().strip(), rfile.read()
        if self.data:
            self.tokenslist = self.tokenize(self.data)
            self.roottoken, self.tailtoken = (self.tokenslist[0], self.tokenslist[-1]) if (self.tokenslist and len(self.tokenslist)) else (None, None)
        else:
            self.tokenslist = []
            self.roottoken, self.tailtoken = None, None
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
    def tokens(self):
        itrtoken = self.root()
        while itrtoken:
            yield itrtoken
            itrtoken = itrtoken.next
    
    def get(self, pretty=None, **kwargs):
        root = self.root()
        return root.get(pretty=pretty, **kwargs) if root else None
    def all(self, pretty=None, **kwargs):
        root = self.root()
        return root.all(pretty=pretty, **kwargs) if root else []
    def add(self, pretty=None, **kwargs):
        tail = self.tail()
        tail.next = tail.add(pretty=pretty, **kwargs)
        tail = tail.next
        return tail
        
    def tokenize(self, data):
        tokens = [] # maintain a sequential list of tokens
        pos = 0     # byte position in data
        while pos < len(data):
            token = None
            open = self.findnextchar(data, '[', pos)        # find the start of the next token
            if open < len(data):
                close = self.findnextchar(data, ']', open)  # find the close of this token
                if close < len(data):
                    prefix = data[pos:open]
                    tokentext = data[open+1:close]
                    tokenparts = tokentext.split(':')
                    token = rawstoken(tokenparts[0], tokenparts[1:], prefix, None, tokens[-1] if len(tokens) else None)
                    pos = close+1
            if token:
                if len(tokens): tokens[-1].next = token
                tokens.append(token)
            else:
                break
        if len(tokens) and pos<len(data):
            tokens[-1].suffix = data[pos:]
        return tokens
    def findnextchar(self, data, char, start=0):
        while start < len(data) and data[start] != char: start += 1
        return start
        
class rawstoken:
    def __init__(self, value=None, args=None, prefix=None, suffix=None, prev=None, next=None, pretty=None):
        # tokens look like this: [value:arg1:arg2:...:argn]
        self.prev = prev            # previous token sequentially
        self.next = next            # next token sequentially
        self.value = value          # value for the token
        self.args = args            # arguments for the token
        self.prefix = prefix        # non-token text between the preceding token and this one
        self.suffix = suffix        # between this token and the next/eof (should typically apply to eof)
        if pretty: self.assign(pretty)
        self.nargs = len(args) if args else 0
        if not self.args: self.args = []
        if prefix:
            self.prefixlines = prefix.split('\n')
            self.tabs = self.prefixlines[-1].count('\t')
        else:
            self.prefixlines = []
            self.tabs = 0
            
    def __str__(self):
        return '[%s%s]' %(self.value, (':%s' % ':'.join(self.args)) if self.args and len(self.args) else '')
    def __repr__(self):
        return '%s%s%s' % (self.prefix if self.prefix else '', str(self), self.suffix if self.suffix else '')
    
    def assign(self, pretty):
        open = pretty.find('[')
        close = pretty.find(']')
        if not(open >= 0 or close >= 0):
            open = 0
            close = len(pretty)-1
            tokentext = pretty
        elif open == -1 or close == -1:
            raise ValueError('Could not parse string %s as a token' % pretty)
        else:
            self.prefix = pretty[:open]
            self.suffix = pretty[close:]
            tokentext = pretty[open+1:close]
        tokenparts = tokentext.split(':')
        self.value = tokenparts[0]
        self.args = tokenparts[1:]
    
    '''
    Starting with this token, execute some query until any of the included checks hits a limit or until there are no more tokens to check.
    '''
    def query(self, checks, reverse=False):
        token = self.prev if reverse else self.next
        limit = False
        for check in checks:
            check.result = []
        while token and (not limit):
            for check in checks:
                if check.match(token):
                    check.result.append(token)
                    if check.limit and len(check.result) >= check.limit:
                        limit = True
                        break
            token = token.prev if reverse else token.next
        return [check.result for check in checks]
    
    '''
    Get the first matching token.
    '''
    def get(self, pretty=None, reverse=False, **kwargs):
        checks = (
            rawstokenquery(pretty=pretty, limit=1, **kwargs)
        ,)
        result = self.query(checks, reverse)[0]
        return result[0] if result and len(result) else None
    
    '''
    Get a list of all matching tokens.
    '''
    def all(self, pretty=None, reverse=False, **kwargs):
        checks = (
            rawstokenquery(pretty=pretty, **kwargs)
        ,)
        return self.query(checks, reverse)[0]
    
    '''
    Get a list of all tokens up to a match.
    '''
    def until(self, pretty=None, reverse=False, **kwargs):
        checks = (
            rawstokenquery(),
            rawstokenquery(pretty=pretty, limit=1, **kwargs)
        )
        return self.query(checks, reverse)[0]
        
    '''
    Determine whether this token matches some constraints.
    '''
    def match(self, pretty=None, **kwargs):
        return rawstokenquery(pretty=pretty, **kwargs).match(self)
        
    '''
    Adds a token. If reverse is True, the token is added immediately before this one. If False, the token is added immediately after.
    '''
    def add(self, pretty=None, reverse=False, **kwargs):
        token = rawstoken(pretty=pretty, **kwargs)
        if reverse:
            token.next = self
            token.prev = self.prev
            self.prev.next = token
            self.prev = token
        else:
            token.prev = self
            token.next = self.next
            self.next.prev = token
            self.next = token
        return token
    
    '''
    Removes this token and the next count tokens in the direction indicated by reverse.
    '''
    def remove(self, count=0, reverse=False):
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

class rawstokenquery:
    def __init__(self, pretty=None, exact_token=None, exact_value=None, exact_args=None, exact_arg=None, re_value=None, re_args=None, re_arg=None, limit=None):
        self.pretty = pretty
        if pretty:
            token = rawstoken(pretty=pretty)
            exact_value = token.value
            exact_args = token.args
        self.exact_token = exact_token
        self.exact_value = exact_value
        self.exact_args = exact_args
        self.exact_arg = exact_arg
        self.re_value = re_value
        self.re_args = re_args
        self.re_arg = re_arg
        self.limit = limit
    def match(self, token):
        if self.exact_token == token:
            return False
        elif self.exact_value is not None and self.exact_value != token.value:
            return False
        elif self.re_value is not None and self.re_value.match(token.value) == None:
            return False
        if self.exact_args is not None:
            if not (len(self.exact_args) == len(token.args) and all([self.exact_args[i] == None or str(self.exact_args[i]) == token.args[i] for i in xrange(0, len(token.args))])):
                return False
        if self.exact_arg is not None:
            if not all([a[0]>=0 and a[0]<len(token.args) and token.args[a[0]] == str(a[1]) for a in self.exact_arg]):
                return False
        if self.re_args is not None:
            if not (len(self.re_args) == len(token.args) and all([self.re_args[i] == None or re.match(self.re_args[i], token.args[i]) for i in xrange(0, len(token.args))])):
                return False
        if self.re_arg is not None:
            if not all([a[0]>=0 and a[0]<len(token.args) and re.match(a[1], token.args[a[0]]) for a in self.re_arg]):
                return False
        return True
