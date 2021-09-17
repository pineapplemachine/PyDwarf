import pydwarf

@pydwarf.urist(
    name = 'charcoalapple.testscript',
    version = '0.0',
    auther = 'CharcoalApple',
    description = '...',
    arguments = {
        'arg1':'something',
    },
)
def myscript(df):
    pass
    return pydwarf.success()
