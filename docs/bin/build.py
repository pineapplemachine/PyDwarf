# Disclaimer: This is a shitty WIP

'''
    Automatically build html documentation using docstrings and code examples as
    a basis.
'''

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../lib'))

import inspect
import itertools

try:
    raise ValueError # TODO: make this highlighting suck less maybe
    import pygments
    import pygments.lexers
    import pygments.formatters
except:
    print('Failed to load dependency pygments. In its absence code examples will lack syntax highlighting.')
    pygments = None

import raws
import pydwarf

from examples import examples



output = '../index.html'



def methodclass(method):
    for cls in inspect.getmro(method.im_class):
        if method.__name__ in cls.__dict__: 
            return cls
    return None
    


class doc:
    defaultskips = ('Internal:', 'Deprecated:')
    
    def document(self, skips=defaultskips):
        if self.item:
            self.fullname = self.buildfullname(self.parents)
            print 'Documenting: %s' % self.fullname
            if inspect.isclass(self.item) or inspect.ismodule(self.item):
                self.documentmembers(skips)
            
    def documentmembers(self, skips=defaultskips):
        if self.parents[-1].item is None:
            for member in self.item.__dict__.itervalues():
                if (
                    (inspect.ismodule(member) and member.__name__ not in ('os', 'sys', 're')) or
                    inspect.isclass(member) or inspect.isfunction(member)
                ):
                    if not doc.skip(member.__doc__, skips): self.children.append(doc(member))
        
        else:
            memberpredicate = lambda member: (
                (inspect.ismethod(member) and methodclass(member) is self.item) or inspect.isfunction(member)
            )
            for membername, member in inspect.getmembers(self.item, predicate=memberpredicate):
                if not doc.skip(member.__doc__, skips): self.children.append(doc(member))
        
        self.documentchildren(skips)
                
    def documentchildren(self, skips=defaultskips):
        memberparents = self.parents + [self]
        for child in self.children:
            child.parents = memberparents
            child.document(skips)
    
    @staticmethod
    def skip(docstring, skips=defaultskips):
        if docstring:
            for skip in skips:
                if docstring.strip().startswith(skip):
                    return True
    
    def __init__(self, item):
        self.item = item
        self.fullname = None
        self.examples = []
        self.children = []
        self.parents = []
        self.documented = False
        self.duplicate = False
        
    def __iter__(self):
        if self.children:
            for child in self.children:
                yield child
        
    def __str__(self):
        return self.fullname
        
    def iterall(self):
        if self.children:
            for child in self.children:
                yield child
                for item in child.iterall():
                    yield item
    
    def itemname(self):
        if self.item is None:
            return ''
        elif inspect.ismodule(self.item):
            return self.item.__name__.split('.')[-1]
        else:
            return self.item.__name__
            
    def buildfullname(self, parents):
        parts = [self.itemname()]
        if parents:
            for parent in reversed(parents):
                if parent.item:
                    parts.append(parent.itemname())
        parts.reverse()
        return '.'.join(parts)
        
    def findexamples(self, examples):
        self.examples = []
        nameparts = self.fullname.split('.')
        for example in examples:
            for high in example['high']:
                highparts = high.split('.')
                try:
                    if highparts[-1] == nameparts[-1] and highparts[-2] == nameparts[-2]:
                        self.examples.append(example)
                except:
                    pass
                    
    def getfile(self):
        path = os.path.abspath(inspect.getfile(self.item))
        parts = path.replace('\\', '/').split('/')
        for index, part in reversed(list(enumerate(parts))):
            if part == 'pydwarf' or part == 'raws':
                path = '/'.join(parts[index:])
                if path.endswith('.pyc'): path = path[:-1]
                return path
        return None
                    
    def getsupers(self):
        if inspect.isclass(self.item):
            mro = inspect.getmro(self.item)
            supers = []
            for item in mro:
                if item is not self.item:
                    docitem = self.getroot().getforitem(item)
                    if docitem: supers.append(docitem)
            return supers
        else:
            return []
    
    def getroot(self):
        return self.parents[0]
        
    def getforitem(self, item):
        for child in self.iterall():
            if child.item is item:
                return child
        return None
                    
    def htmlbody(self, h=1):
        self.documented = bool(self.item.__doc__ or self.examples)
        
        if self.item is None:
            return self.htmlchildren(h)
        else:
            return '<div class="item-header">%s</div><div class="item-body">%s</div>' % (
                self.htmlheader(h), self.htmldocbase() + self.htmlarguments() + self.htmlexamples() + self.htmlchildren(h)
            )
    
    def htmlheader(self, h=1):
        srcpath = ''
        if self.item is not None:
            srcpath = self.getfile()
            if srcpath: srcpath = '../%s' % srcpath
            
        inherits = ''
        supers = sorted(self.getsupers(), key=lambda super: super.fullname)
        if supers:
            inherits = '<span class="inherits-from">inherits from</span>%s' % (
                '<span class="superclass-delimeter">,</span>'.join(
                    '<a class="superclass" href="#%s">%s</a>' % (
                        item.fullname,
                        item.fullname
                    ) for item in supers
                )
            )
            
        return '<h%(h)d class="item-title" id="%(id)s"><a href="%(srcpath)s">%(name)s</a></h%(h)d>%(supers)s' % {
            'h': h,
            'id': self.fullname,
            'srcpath': srcpath,
            'supers': inherits,
            'name': self.fullname,
        }
    
    def htmldocbase(self):
        if not(self.item.__doc__) and not(self.examples):
            return '<div class="docstring undocumented">Undocumented</div>'
        else:
            return '<div class="docstring documented">%s</div>' % self.item.__doc__
    
    def htmlchildren(self, h=1):
        if self.children:
            return '<div class="subs">%s</div>' % ''.join(
                child.htmlbody(h=h+(self.item is not None)) for child in sorted(self.children, key=lambda c: c.fullname)
            )
        else:
            return ''
        
    def htmlarguments(self):
        try:
            args = inspect.getargspec(self.item)
        except:
            return ''
        else:
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
                            arg, arg, type(default).__name__, default, defaultfmt
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
            
            return outer % delim.join(inner)
        
    def htmlexamples(self):
        if self.examples:
            examples = (self.formathtmlexample(example['text']) for example in self.examples)
            element = 'pre' if pygments is None else 'div'
            return (
                '<div class="examples">%s</div>' %
                '<div class="example-separator"></div>'.join(
                    ('<%s class="highlight-example">%s</%s>' % (element, example, element)) for example in examples
                )
            )
        else:
            return ''
            
    def formathtmlexample(self, example):
        if pygments is not None:
            return pygments.highlight(example, pygments.lexers.PythonLexer(), pygments.formatters.HtmlFormatter())
        else:
            return example.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
    def htmlcontents(self):
        content = '<a class="%s" href="#%s">%s</a>' % (
            ('contents-undocumented', 'contents-documented')[self.documented],
            self.fullname, self.itemname()
        )
        
        contents = (child.htmlcontents() for child in sorted(self.children, key=lambda c: c.fullname))
            
        contentstext = '<ul>%s</ul>' % '\n'.join(('<li>%s</li>' % item) for item in contents)
        return content + repr(self.item) + contentstext
        
    def dedupe(self):
        newchildren = []
        for child in self.children:
            if not child.duplicate:
                child.dedupe()
                newchildren.append(child)
        self.children = newchildren
    
    def markdupes(self):
        reprs = {}
        for child in self.iterall():
            key = repr(child.item)
            if key not in reprs: reprs[key] = []
            reprs[key].append(child)
        for childlist in reprs.itervalues():
            if len(childlist) > 1:
                childlist.sort(key=lambda child: -len(child.fullname))
                for i in xrange(1, len(childlist)): childlist[i].duplicate = True
                
    
    
root = doc(None)
root.children = [doc(item) for item in (raws, pydwarf)]
root.documentchildren()
root.markdupes()
root.dedupe()
for item in root.iterall():
    item.findexamples(examples)



css = '''
    body {
        font-family: sans-serif;
        background-color: #1f1e1e;
        color: #ddd;
        padding: 2%;
    }
    
    .highlight-example {
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
        padding-left: 16px;
        border-top-style: solid;
        border-bottom-style: solid;
        border-width: 1px;
        border-color: #282828;
        padding-top: 6px;
        padding-bottom: 6px;
        margin-bottom: 12px;
    }
    .level {
        margin-top: 16px;
        border-left-style: solid;
        border-width: 2px;
        border-color: #444;
        padding: 8px 0px;
        padding-left: 20px;
    }
    
    .item-title {
        display: inline;
    }
    .item-header {
        padding-top: 12px;
        padding-bottom: 8px;
    }
    .inherits-from, .superclass, .superclass-delimeter {
        font-style: italic;
        font-size: 10pt;
    }
    .inherits-from {
        color: #bbb;
        padding-left: 12px;
        padding-right: 4px;
    }
    .superclass-delimeter {
        color: #bbb;
        padding-right: 3px;
    }
'''

if pygments is not None:
    css += pygments.formatters.HtmlFormatter().get_style_defs('.highlight-example')

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
    'body': root.htmlbody(h=2),
    'contents': root.htmlcontents(),
}



with open(output, 'wb') as htmlfile:
    htmlfile.write(html)
