#!/usr/bin/env python
# coding: utf-8

'''
    Poor man's unit test which goes through each of the example doctests in
    docs/examples/ and makes sure they actually work as advertised.
'''

# import raws, pydwarf; df = pydwarf.df(raws)



import sys
import os

pydwarf_root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))
sys.path.append(pydwarf_root)
sys.path.append(os.path.join(pydwarf_root, 'lib'))

import inspect
import doctest
import re

import raws
import pydwarf

from examples import examples
                    

    
def verify(examples, **globs):
    docparser = doctest.DocTestParser()
    docrunner = doctest.DocTestRunner()
    results = []
    testnum = 0
    
    df = globs['df']
    dfcopy = df.copy()
    
    for example in examples:
        print 'Running example %s' % example['name']
        testnum += 1
        
        # Create the doctest object
        test = docparser.get_doctest(
            string = example['text'],
            globs = globs,
            name = example['name'],
            filename = None,
            lineno = None
        )
        
        # Actually run the test
        resultcount = len(results)
        docrunner.run(
            test = test,
            out = lambda result: results.append(result),
            clear_globs = False
        )
        
        # Handle flags
        if 'reset' in example['flags']:
            print 'Resetting df raws.'
            df = dfcopy
            dfcopy = df.copy()
        
    return results



doctest_pattern = (
    '(?s)\*+\n'
    'Line (?P<line>\d+), in (?P<name>.*)\n'
    'Failed example:\n'
        '(?P<text>.*)\n'
    '('
        'Expected:\n'
            '(?P<expected>.*)\n'
        'Got:\n'
            '(?P<got>.*?)'
    '|'
        'Exception raised:\n'
            '(?P<exception>.*)'
    ')'
    '\s*$'
)
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
    lastfailurein = None
    for result in results:
        match = doctest_result_re.match(result.expandtabs(4))
        groups = match.groupdict()
        if groups['got'] and groups['expected']:
            ignore = groups['got'].strip() == groups['expected'].strip()
        else:
            ignore = False
        if groups['name'] == lastfailurein:
            ignore = True
        else:
            lastfailurein = groups['name']
        if not ignore: realresults.append(result)
    
    if realresults:
        resultstext = '\n\n'.join(reversed(realresults))
        print resultstext
    else:
        print 'All examples ran successfully.'
