import objects
from rawsqueryable import rawsqueryable

import forward



@forward.declare
class rawsqueryableadd(rawsqueryable):
    
    # Inheriting classes must implement an add method
    
    def set(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settoken = self.get(exact_value=value)
        if not settoken:
            return self.add(value=value, args=args)
        else:
            settoken.setargs(args)
            return settoken
            
    def setprop(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settoken = self.getprop(exact_value=value)
        if not settoken:
            return self.addprop(value=value, args=args)
        else:
            settoken.setargs(args)
            return settoken
            
    def setall(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settokens = self.all(exact_value=value)
        settokens.each(lambda token: token.setargs(args))
        return settokens
            
    def setallprop(self, *args, **kwargs):
        value, args = rawsqueryableadd.argsset(*args, **kwargs)
        settokens = self.allprop(exact_value=value)
        settokens.each(lambda token: token.setargs(args))
        return settokens
        
    @staticmethod
    def argsset(*args, **kwargs):
        token = forward.declare.rawstoken.autosingular(*args, **kwargs)
        return token.value, token.args
    