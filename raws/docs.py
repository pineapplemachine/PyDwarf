import inspect
import doctest

import forward

from examples import examples



examplesdict = {}
for example in examples:
    if len(example) > 1:
        exampletext = example[-1]
        for classname, membername in (item.split('.') for item in example[:-1]):
            if classname not in examplesdict: examplesdict[classname] = {}
            if membername not in examplesdict[classname]: examplesdict[classname][membername] = []
            examplesdict[classname][membername].append(exampletext)

def getexamples(classname, membername):
    exampleslist = examplesdict.get(classname, {}).get(membername)
    if exampleslist:
        return '\n\n'.join(exampleslist)
    else:
        return ''
    
def getclass(method):
    for cls in inspect.getmro(method.im_class):
        if method.__name__ in cls.__dict__: return  cls
    return None
    
def docclass(cls):
    members = inspect.getmembers(cls, predicate=inspect.ismethod)
    for member in members: docmember(member[1], cls)
    return cls
    
def docmember(member, cls=None):
    classname, membername = (cls if cls else getclass(member)).__name__, member.__name__
    description = member.__doc__.strip() if member.__doc__ else ''
    examples = getexamples(classname, membername)
    docstring = '\n\n'.join(i for i in (description, examples) if i)
    try:
        member.__doc__ = docstring
    except:
        member.__func__.__doc__ = docstring
    return member
    
def test(**globs):
    docparser = doctest.DocTestParser()
    docrunner = doctest.DocTestRunner()
    results = []
    testnum = 0
    for example in examples:
        testnum += 1
        test = docparser.get_doctest(
            string = example[-1],
            globs = globs,
            name = 'doctest %d' % testnum,
            filename = None,
            lineno = None
        )
        docrunner.run(
            test = test,
            out = lambda result: results.append(result),
            clear_globs = False
        )
    return results
    
@forward.declare
def doc(item):
    if inspect.isclass(item):
        return docclass(item)
    else:
        return docmember(item)
    