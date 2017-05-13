import os

import pydwarf
import raws



@pydwarf.urist(
    name = 'pineapple.easypatch',
    title = 'Easy Patch',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Given a path to a file, a directory, a content string, a tokenlist, a raws
        file object, or an iterable containing a combination of these, a file or files are added
        to the dir object, and these same objects can be permitted using the permitted_entities
        argument.''',
    arguments = {
        'files': '''The file or files to be added.''',
        '**kwargs': 'Passed on to pineapple.utils.permitobjects.',
    },
    compatibility = '.*'
)
def easypatch(df, files, **kwargs):
    if isinstance(files, basestring):
        if os.path.isfile(files):
            return easypatch_filepath(df, files, **kwargs)
        elif os.path.isdir(files):
            return easypatch_dirpath(df, files, collision_fails=False, **kwargs)
        else:
            return easypatch_content(df, files, **kwargs)
    elif isinstance(files, raws.tokenlist):
        return easypatch_tokens(df, files, **kwargs)
    elif isinstance(files, raws.rawfile):
        return easypatch_file(df, files, **kwargs)
    else:
        for file in files:
            response = easypatch(df, file, collision_fails=False, **kwargs)
            if not response: return response
        return pydwarf.success('Added %d files.' % len(files))



def easypatch_dirpath(df, path, loc=None, **kwargs):
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            response = easypatch_filepath(df, path=filepath, loc=loc, root=root, **kwargs)
            if not response: return response
    return pydwarf.success('Added files from directory %s.' % path)

def easypatch_filepath(df, path, loc=None, root=None, **kwargs):
    file = raws.rawfile(path=path, loc=loc, root=root)
    return easypatch_file(df, file, **kwargs)

def easypatch_content(df, content, loc, **kwargs):
    file = raws.rawfile(path=loc, content=content)
    return easypatch_file(df, file, **kwargs)
    
def easypatch_tokens(df, tokens, loc, **kwargs):
    file = raws.rawfile(path=loc, tokens=tokens)
    return easypatch_file(df, file, **kwargs)

def easypatch_file(df, file, collision_fails=True, replace=False, **kwargs):
    if replace or str(file) not in df:
        df.add(file, replace=replace)
        objects = file.allobj()
        response = pydwarf.urist.getfn('pineapple.utils.permitobjects')(
            df,
            objects = objects,
            **kwargs
        )
        return response
    elif collision_fails:
        return pydwarf.failure('Failed to add file because a file by the same name already exists in the dir.')
    else:
        return pydwarf.success('Didn\'t add the file because a file by the same name already exists in the dir.')
