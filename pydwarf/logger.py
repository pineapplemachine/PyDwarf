#!/usr/bin/env python
# coding: utf-8

'''
    This module is super simple: just make a default, shared logger object.
'''

import sys
import logging
from datetime import datetime

log = logging.getLogger()

log.setLevel(logging.DEBUG)

datetimeformat = '%Y.%m.%d.%H.%M.%S'
timestamp = datetime.now().strftime(datetimeformat)

stdouthandler = logging.StreamHandler(sys.stdout)
stdouthandler.setLevel(logging.DEBUG)
stdouthandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datetimeformat))
log.addHandler(stdouthandler)

logfilehandler = logging.FileHandler.__new__(logging.FileHandler) # Constructor won't work without a filepath, so skip it for now
logfilehandler.setLevel(logging.DEBUG)
logfilehandler.setFormatter(logging.Formatter('%(asctime)s: %(filename)s[%(lineno)s]: %(levelname)s: %(message)s', datetimeformat))
