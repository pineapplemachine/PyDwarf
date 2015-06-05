# A bit of clever hackishness to make it possible to do things like:
# raws.color.blue == 1
# raws.color.lred == 12
# raws.color.blue() = (1, 0, 0)
# raws.color.lred() == (4, 0, 1)
# raws.color.blue.bg() = (0, 1, 0)
# raws.color.lred.bg() = (0, 12, 0)
# raws.color.lblue(pydwarf.color.red) == (1, 4, 1)
# raws.color.lblue(pydwarf.color.lred) == (1, 12, 1)

class color:
    def __init__(self, value):
        self.value = value
    def __call__(self, bg=0, i=0):
        return (str(self.value % 8), str(int(bg)), str(int(i or (self.value >= 8))))
    def __int__(self):
        return self.value
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self)
        
    def bg(self):
        return ('0', str(self.value), '0')
        
    # Overload common operators
    def __eq__(self, value): return self.value == value
    def __ne__(self, value): return self.value != value
    def __add__(self, value): return self.value + value
    def __sub__(self, value): return self.value - value
    def __mul__(self, value): return self.value * value
    def __div__(self, value): return self.value / value
    def __mod__(self, value): return self.value % value

black, blue, green, cyan, red, magenta, brown, lgray, dgray, lblue, lgreen, lcyan, lred, lmagenta, yellow, white = [color(i) for i in xrange(0, 16)]
