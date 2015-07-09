def declare(item):
    declare.__dict__[item.__name__] = item
    return item
