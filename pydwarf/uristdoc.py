#!/usr/bin/env python
# coding: utf-8



'''Generate formatted documentation for registered scripts based on their metadata.'''



import os
import textwrap



def __main__():
    '''Internal: Set up default templates.'''
    template.format['txt'] = txttemplate()
    template.format['md'] = mdtemplate()
    template.format['html'] = htmltemplate()
    
    

class template(object):
    '''Internal: Helpful class for handling different formats used by the urist.doc method.'''
    
    format = {}
        
    def preprocess(self, item):
        if isinstance(item, basestring):
            return self.preprocesstext(item)
        elif isinstance(item, list) or isinstance(item, tuple):
            return [self.preprocess(i) for i in item]
        elif isinstance(item, dict):
            return {self.preprocess(key): self.preprocess(value) for key, value in item.iteritems()}
        else:
            return item
    def preprocesstext(self, text):
        return text
        
    def concat(self, items):
        return '\n\n'.join(items)
        
    def join(self, items, delimiter=',', natural=False):
        if not items:
            return None
        elif isinstance(items, basestring):
            return items
        elif len(items) == 1:
            return items[0]
        elif natural:
            if len(items) == 2:
                return ' and '.join(str(item) for item in items)
            else:
                return '%s%s and %s' % (
                    ('%s ' % delimiter).join(str(item) for item in items[:-1]),
                    delimiter,
                    items[-1]
                )
        else:
            return delimiter.join(str(item) for item in items)
    def fmt(self, string, format):
        return string % format if string and format else None
        
    def header(self, **kwargs):
        return None
    def arguments(self, **kwargs):
        return None
    def metadata(self, **kwargs):
        return None
        
    def norm(self, text):
        return ' '.join([line.strip() for line in str(text).split('\n')])
    def wrap(self, text):
        return textwrap.fill(text) if self.wraptext else text
        
    def full(self, delimiter=None, arguments=None, metadata=None, **kwargs):
        if delimiter is None: delimiter = self.delimiter
        
        kwargs = {key: self.preprocess(value) for key, value in kwargs.iteritems()}
        arguments = self.preprocess(arguments)
        metadata = self.preprocess(metadata)
        
        body = delimiter.join(item for item in (
            self.header(**kwargs),
            self.arguments(arguments) if arguments else None,
            self.metadata(metadata) if metadata else None
        ) if item)
        return '\n'.join(self.wrap(line) for line in body.split('\n')) if self.wraptext else body
        


class txttemplate(template):
    def __init__(self):
        self.delimiter = '\n\n'
        self.wraptext = True
        
    def header(self, name=None, version=None, author=None, description=None, **kwargs):
        headeritems = (
            name,
            self.fmt('version %s', version),
            self.fmt('by %s', self.join(author))
        )
        header = 'Script %s:' % ' '.join(item for item in headeritems if item)
        return '%s\n\n%s' % (header, self.norm(description)) if description else header
    
    def arguments(self, arguments):
        return 'Arguments:\n%s' % '\n'.join(('  %s: %s' % (key, self.norm(value)) for key, value in arguments.iteritems()))
    def metadata(self, metadata):
        return 'Metadata:\n%s' % '\n'.join(('  %s: %s' % (key, self.norm(value)) for key, value in metadata.iteritems()))



class mdtemplate(template):
    def __init__(self):
        self.delimiter = '\n\n'
        self.wraptext = False
        
    def preprocesstext(self, text):
        return text.replace('*', '\*').replace('#', '\#')
        
    def concat(self, items):
        return '''# Scripts\n\n%s''' % '\n\n'.join(items)
        
    def header(self, name=None, version=None, author=None, description=None, title=None, **kwargs):
        headeritems = (
            self.fmt('## %s', name),
            #self.fmt('Version %s', version),
            self.fmt('%sCreated by %s.', (title + '. ' if title else '', self.join(author, natural=True))),
            self.norm(description)
        )
        return '\n\n'.join(item for item in headeritems if item)
    
    def arguments(self, arguments):
        return '#### Arguments:\n\n%s' % '\n\n'.join(('* **%s:** %s' % (key, self.norm(value)) for key, value in arguments.iteritems()))
    def metadata(self, metadata):
        return '#### Metadata:\n\n%s' % '\n\n'.join(('* **%s:** %s' % (key, self.norm(value)) for key, value in metadata.iteritems()))
    
    
        
class htmltemplate(template):
    def __init__(self):
        self.delimiter = '\n'
        self.wraptext = False
        
    def preprocesstext(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
    def concat(self, items):
        return '''
            <html>
                <head>
                    <meta charset="utf-8">
                    <title>Scripts</title>
                    <link rel="shortcut icon" href="../images/favicon.png"/>
                    <style>
                        body {
                            font-family: sans-serif;
                            color: #aaa;
                            background-color: #000;
                        }
                        .script {
                            margin: 20px 6px;
                            padding: 8px;
                            padding-left: 24px;
                            background-color: #111;
                        }
                    </style>
                </head>
                <body>
                    <h1>Scripts</h1>
                    %s
                </body>
            </html>
        ''' % '\n\n'.join('<div class="script">%s</div>' % item for item in items)
        
    def header(self, name=None, version=None, author=None, description=None, **kwargs):
        headeritems = (
            self.fmt('<h2>%s</h2>', name),
            #self.fmt('<p>Version %s</p>', version),
            self.fmt('<p>Created by %s.</p>', self.join(author, natural=True)),
            self.norm(description)
        )
        return '\n'.join(item for item in headeritems if item)
    
    def arguments(self, arguments):
        return '<h3>Arguments</h3>\n<ul>%s</ul>' % '\n'.join(('<li><strong>%s:</strong> %s</li>' % (key, self.norm(value)) for key, value in arguments.iteritems()))
    def metadata(self, metadata):
        return '<h3>Metadata</h3>\n<ul>%s</ul>' % '\n'.join(('<li><strong>%s:</strong> %s</li>' % (key, self.norm(value)) for key, value in metadata.iteritems()))



__main__()
