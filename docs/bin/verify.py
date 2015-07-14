#!/usr/bin/env python
# coding: utf-8

'''
    Poor man's unit test which goes through each of the example doctests in
    docs/examples/ and makes sure they actually work as advertised.
'''



import sys
import os

pydwarf_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
sys.path.append(pydwarf_root)

import inspect
import doctest
import re

import raws
import pydwarf



examples = []
examples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../examples')



for filename in os.listdir(examples_dir):
    if filename.endswith('.txt'):
        path = os.path.join(examples_dir, filename)
        with open(path, 'rb') as examplefile:
            examplebodies = [body.strip() for body in examplefile.read().split('---')]
            for index, body in enumerate(examplebodies):
                try:
                    high, low, text = body.split('\n', 2)
                    examples.append({
                        'high': high.split(' '),
                        'low': low.split(' '),
                        'text': text,
                        'name': '%s #%d' % (filename, index+1)
                    })
                except:
                    pass
                    

    
def verify(examples, **globs):
    docparser = doctest.DocTestParser()
    docrunner = doctest.DocTestRunner()
    results = []
    testnum = 0
    for example in examples:
        print 'Running example %s' % example['name']
        testnum += 1
        test = docparser.get_doctest(
            string = example['text'],
            globs = globs,
            name = example['name'],
            filename = None,
            lineno = None
        )
        docrunner.run(
            test = test,
            out = lambda result: results.append(result),
            clear_globs = False
        )
    return results



doctest_pattern = r'\*+\n(?s)Line (\d+), in (.*)\nFailed example:\n(.*)\nExpected:\n(.*)\nGot:(.*?)\s*$'
doctest_result_re = re.compile(doctest_pattern)



if __name__ == '__main__':
    print 'Initializing session.'
    conf = pydwarf.config.load(root=pydwarf_root, args={
        'log': ''
    })
    session = pydwarf.session(raws, conf)
    
    print 'Running examples.'
    results = verify(
        examples,
        df = session.df,
        raws = raws,
        pydwarf = pydwarf,
        session = session,
        conf = conf
    )
    
    realresults = []
    for result in results:
        match = doctest_result_re.match(result.expandtabs(4))
        if match.group(4).strip() != match.group(5).strip():
            realresults.append(result)
    
    if realresults:
        resultstext = '\n\n'.join(reversed(realresults))
        print resultstext
    else:
        print 'All examples ran successfully.'
