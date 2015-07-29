# Disclaimer: This is a shitty WIP

'''
    Automatically build html documentation using docstrings and code examples as
    a basis.
'''

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

import inspect
import itertools

import raws
import pydwarf

from examples import examples



output = '../index.html'



def methodclass(method):
    for cls in inspect.getmro(method.im_class):
        if method.__name__ in cls.__dict__: 
            return cls
    return None
    



items = [
    raws,
    pydwarf
]



def document(item, parents=None, skipinternal=True):
    nameparts = [item.__name__]
    itemexamples = None
    subs = None
    
    if parents:
        for parent in reversed(parents):
            nameparts.append(parent.__name__)
            
    nameparts.reverse()
    name = '.'.join(nameparts)
    
    print 'Documenting item: %s' % name
    
    if inspect.isclass(item) or inspect.ismodule(item):
        if parents:
            memberparents = parents + [item]
        else:
            memberparents = [item]
        
        subs = []
        
        if parents is None:
            for member in item.__dict__.itervalues():
                if (
                    (inspect.ismodule(member) and member.__name__ not in ('os', 'sys', 're')) or
                    inspect.isclass(member) or inspect.isfunction(member)
                ):
                    subs.append(document(member, memberparents[1:]))
        else:
            memberpredicate = lambda member: (
                (inspect.ismethod(member) and methodclass(member) is item) or inspect.isfunction(member)
            )
            for membername, member in inspect.getmembers(item, predicate=memberpredicate):
                if skipinternal and member.__doc__ and member.__doc__.startswith('Internal'): continue
                subs.append(document(member, memberparents))
        
    itemexamples = []
    for example in examples:
        for high in example['high']:
            highparts = high.split('.')
            try:
                if highparts[-1] == nameparts[-1] and highparts[-2] == nameparts[-2]:
                    itemexamples.append(example)
            except:
                pass
        
    return (name, item, itemexamples, subs)
    
def dedupedocs(docs, alldocs=None, conflicts=None, root=True):
    if root:
        alldocs = docs
        conflicts = {}
    
    for name, item, itemexamples, subs in docs:
        for subname in docdupes(name, item, alldocs):
            if name not in conflicts: conflicts[name] = []
            conflicts[name].append(subname)
        if subs:
            dedupedocs(subs, alldocs, conflicts, False)
            
    if root:
        return dedupeconflicts(alldocs, conflicts)
        
def dedupeconflicts(docs, conflicts):
    newdocs = []
    for name, item, itemexamples, subs in docs:
        ignore = False
        if name in conflicts:
            for conflictname in conflicts[name]:
                if len(name) < len(conflictname):
                    ignore = True
                    break
        if not ignore:
            if subs:
                subs = dedupeconflicts(subs, conflicts)
            newdocs.append((name, item, itemexamples, subs))
        else:
            print 'Ignoring item: %s' % name
    return newdocs

def docdupes(name, item, docs):
    for subname, subitem, subexamples, subsubs in docs:
        if item is subitem and name != subname:
            yield subname
        if subsubs:
            for dupe in docdupes(name, item, subsubs):
                yield dupe
            



documented = {}

def htmldoc(docs, h=1):
    bodies = []
    for name, item, itemexamples, subs in docs:
        header = '<h%d id="%s">%s</h%d>' % (h, name, name, h)
        
        docbody = ''
        argsbody = ''
        examplesbody = ''
        subsbody = ''
        
        try:
            args = inspect.getargspec(item)
        except:
            args = None
        if item.__doc__:
            docbody = '<div class="docstring documented">%s</div>' % item.__doc__
        if args:
            outer = '<div class="arguments">Arguments: %s</div>'
            delim = '<span class="argument-separator">,</span>'
            item = '<span class="%s">%s</span>'
            inner = []
            
            for index, arg in enumerate(args.args):
                if args.defaults and index >= len(args.args) - len(args.defaults):
                    default = args.defaults[index - (len(args.args) - len(args.defaults))]
                    if isinstance(default, basestring):
                        defaultfmt = '"%s"' % default
                    else:
                        defaultfmt = default
                    itemtext = item % (
                        'argument has-default',
                        '<span class="argument-name %s">%s</span><span class="argument-equals">=</span><span class="argument-default %s %s">%s</span>' % (
                            arg,
                            arg,
                            type(default).__name__,
                            default,
                            defaultfmt
                        )
                    )
                else:
                    itemtext = item % (
                        'argument no-default',
                        '<span class="argument-name %s">%s</span>' % (arg, arg)
                    )
                inner.append(itemtext)
            if args.varargs:
                itemtext = item % ('argument varargs', '*args')
                inner.append(itemtext)
            if args.keywords:
                itemtext = item % ('argument keywords', '**kwargs')
                inner.append(itemtext)
            
            argsbody = outer % delim.join(inner)
            
        if itemexamples:
            examplesbody = (
                '<div class="examples">%s</div>' %
                '<div class="example-separator"></div>'.join(
                    (
                        '<pre class="example">%s</pre>' % example['text']
                    ) for example in itemexamples
                )
            )
            
        if not(examplesbody or docbody):
            docbody = '<div class="docstring undocumented">Undocumented</div>'
            documented[name] = False
        else:
            documented[name] = True
        
        if subs:
            subsbody = '<div class="subs">%s</div>' % htmldoc(subs, h+1)
        
        body = '<div class="item-header">%s</div><div class="item-body">%s</div>' % (header, docbody + argsbody + examplesbody + subsbody)
        bodies.append('<div class="item">%s</div>' % body)
    bodiestext = '<div class="level level-%d">%s</div>' % (h, '\n'.join(sorted(bodies)))
    return bodiestext
    
def htmlcontents(docs):
    contents = []
    for name, item, itemexamples, subs in docs:
        content = '<a class="%s" href="#%s">%s</a>' % (
            ('contents-undocumented', 'contents-documented')[documented.get(name, 0)],
            name, item.__name__
        )
        if subs:
            content += htmlcontents(subs)
        contents.append(content)
    contentstext = '<ul>%s</ul>' % '\n'.join(('<li>%s</li>' % item) for item in sorted(contents))
    return contentstext
        



docs = []
for item in items: docs.append(document(item))
docs = dedupedocs(docs)

css = '''
    body {
        font-family: sans-serif;
        background-color: #1f1e1e;
        color: #ddd;
        padding: 2%;
    }
    
    .example {
        background-color: #060606;
        color: #3c1;
        padding: 8px;
        margins: 0;
        white-space: pre-wrap;       /* CSS 3 */
        white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
        white-space: -pre-wrap;      /* Opera 4-6 */
        white-space: -o-pre-wrap;    /* Opera 7 */
        word-wrap: break-word;       /* Internet Explorer 5.5+ */
    }
    .example-separator {
        margins: 0;
    }
    
    ul {
        list-style-type: circle;
    }
    
    a {
        text-decoration: none;
        color: #ddd;
    }
    a:hover {
        text-decoration: underline;
    }
    
    .docstring {
        padding-bottom: 16px;
        font-style: italic;
        color: #bbb;
    }
    
    .arguments {
        font-size: 10pt;
        font-style: italic;
        color: #bbb;
        padding-left: 8px;
    }
    .argument-separator, .argument-equals {
        color: #555;
    }
    .argument-separator {
        margin-right: 6px;
    }
    .argument-equals {
        margin-left: 2px;
        margin-right: 2px;
    }
    .argument-default {
        color: #555;
    }
    .argument-default.str {
        color: #474;
    }
    .argument-default.int {
        color: #356;
    }
    .argument-name.self, .argument-default.bool, .argument-default.NoneType {
        color: #742;
    }
    .argument.varargs, .argument.keywords {
        color: #555;
    }
    
    .contents-undocumented {
        color: #888;
    }
    
    .item {
        padding: 6px;
    }
    .item-body {
        margin-left: 16px;
        border-top-style: solid;
        border-bottom-style: solid;
        border-width: 1px;
        border-color: #282828;
        padding-top: 6px;
        padding-bottom: 6px;
    }
    .level {
        margin-top: 16px;
        border-left-style: solid;
        border-width: 2px;
        border-color: #444;
        padding: 8px 0px;
        padding-left: 20px;
    }
'''

html = '''
    <html>
        <head>
            <link rel="shortcut icon" href="../images/favicon.png"/>
            <title>%(title)s</title>
            <style>%(style)s</style>
        </head>
        <body>
            <h1>Table of Contents</h1>
            <div class="indent">%(contents)s</div>
            <h1>Documentation</h1>
            <div class="indent">%(body)s</div>
        </body>
    </html>
''' % {
    'title': 'PyDwarf docs',
    'style': css,
    'body': htmldoc(docs, h=2),
    'contents': htmlcontents(docs),
}



with open(output, 'wb') as htmlfile:
    htmlfile.write(html)
