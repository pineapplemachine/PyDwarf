# Disclaimer: This is a shitty WIP

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

import inspect

import raws
import pydwarf

output = 'index.html'

items = {
    'raws.token': raws.token,
    'raws.file': raws.file,
    'raws.dir': raws.dir,
    'raws.color': raws.color,
    'raws.tokenfilter': raws.tokenfilter,
    'raws.boolfilter': raws.boolfilter,
    'pydwarf.session': pydwarf.session,
    'pydwarf.urist': pydwarf.urist
}

alldoc = {}
for itemname, item in items.iteritems():
    itemdoc = {}
    alldoc[itemname] = itemdoc
    
    for membername, member in inspect.getmembers(item):
        memdoc = {}
        itemdoc[membername] = member
    
with open(output, 'wb') as html:
    css = 'pre { background-color: #ddd; color: #113 }'
    html.write('<html><head><title>%(title)s</title><style>%(style)s</style></head><body>' % {'title': 'PyDwarf docs', 'style': css})
    html.write('<h1 style="font-size: 50; color: #800">Warning: This is a shitty WIP.</h1>')
    for itemname in sorted(alldoc.iterkeys()):
        itemdoc = alldoc[itemname]
        html.write('<h1>%s</h1>' % itemname)
        for membername in sorted(itemdoc.iterkeys()):
            member = itemdoc[membername]
            if callable(member) and membername not in ('__module__', '__str__', '__repr__', '__doc__'):
                html.write('<p><b>%s</b><br><pre>%s</pre></p>' % (membername, member.__doc__))
    html.write('</body></html>')

    



