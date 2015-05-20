import os
import traceback
import logging

__version__ = 'alpha'

# Make a default log object if none exists already
if 'log' not in vars() and 'log' not in globals(): log = logging.getLogger()

# Convenience functions which scripts can use for returning success/failure responses
def success(status=None): return response(True, status)
def failure(status=None): return response(False, status)
def response(success=None, status=None):
    result = {}
    if success is not None: result['success'] = success
    if status is not None: result['status'] = status
    return result
    
# Functions in scripts must be decorated with this in order to be made available to PyDwarf
class urist:
    registered = {}
    def __init__(self, **kwargs):
        self.metadata = kwargs
    def __call__(self, fn):
        self.name = fn.__name__
        self.fn = fn
        urist.registered[self.name] = self.fn
        return fn
    @staticmethod
    def get(name):
        return urist.registered.get(name)
