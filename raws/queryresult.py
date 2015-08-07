import queryable



class queryresult(queryable.queryable):
    def __init__(self, source, results, resultiter=None):
        self.source = source
        self.results = results
        self.resultiter = results if resultiter is None else resultiter
    
    def __iter__(self):
        for result in self.resultiter:
            yield result
            
    def __getitem__(self, item):
        return self.results[item]
    
    def __len__(self):
        return sum(1 for i in self)
        
    def itokens(self, range=None):
        count = 0
        for result in self.resultiter:
            for token in result:
                if range is not None and range <= count: break
                yield token
                count += 1
                
    def each(self, *args, **kwargs):
        kwargs['output'] = kwargs.get('output', tokenlist.tokenlist)
        return queryable.queryable.each(self, *args, **kwargs)
        


import tokenlist
