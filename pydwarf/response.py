class response:
    def __init__(self, success, status):
        self.success = success
        self.status = status
        
    def __str__(self):
        return '%s: %s' % ('SUCCESS' if self.success else 'FAILURE', self.status if self.status else ('Ran %ssuccessfully.' % ('' if self.success else 'un')))
        
    @staticmethod
    def success(status=None):
        return response(True, status)
    @staticmethod
    def failure(status=None):
        return response(False, status)
    
# Convenience functions which scripts can use for returning success/failure responses
def success(status=None): return response.success(status)
def failure(status=None): return response.failure(status)
