def register(item):
    declare.__dict__[item.__name__] = item
    return item
    
def declare(item):
    return register(item)
    