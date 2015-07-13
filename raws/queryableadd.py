import queryable



class rawsqueryableadd(queryable.rawsqueryable):
    
    # Inheriting classes must implement an add method
    
    def set(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settoken = self.get(exact_value=value)
        if settoken is None:
            return self.add(value=value, args=args)
        else:
            settoken.args.reset(args)
            return settoken
            
    def setprop(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settoken = self.getprop(exact_value=value)
        if settoken is None:
            return self.addprop(value=value, args=args)
        else:
            settoken.args.reset(args)
            return settoken
            
    def setall(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settokens = self.all(exact_value=value)
        settokens.each(lambda token: token.args.reset(args))
        return settokens
            
    def setallprop(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settokens = self.allprop(exact_value=value)
        settokens.each(lambda token: token.args.reset(args))
        return settokens
        
    @staticmethod
    def argsset(*args, **kwargs):
        settoken = token.token.autosingular(*args, **kwargs)
        return settoken.value, settoken.args



import objects
import token
