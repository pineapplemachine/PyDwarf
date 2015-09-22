#!/usr/bin/env python
# coding: utf-8



class response(object):
    '''
        Response object recognized by sessions as an item to be returned by
        registered scripts to report their termination status.
    '''
    
    def __init__(self, success, status):
        '''Initialize a response object.'''
        self.success = success
        self.status = status
        
    def __str__(self):
        '''Get a string representation.'''
        return '%s: %s' % (
            'SUCCESS' if self.success else 'FAILURE',
            self.status if self.status else (
                'Ran %ssuccessfully.' % ('' if self.success else 'un')
            )
        )
        
    def __nonzero__(self):
        '''Return True if successful, False otherwise.'''
        return self.success
        
    @staticmethod
    def success(status=None):
        '''Initialize a successful response object.'''
        return response(True, status)
    
    @staticmethod
    def failure(status=None):
        '''Initialize a failed response object.'''
        return response(False, status)
