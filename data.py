from pathlib import Path

from atrox3d import simplegit


def add_path(path:Path, data:dict) -> dict:
    ''' create or add paths to dice as keys:dict with the last being {} '''
    
    # if path == Path('.'):
        # raise ValueError('cannot scan current dir')
    if not len(path.parts):
        raise ValueError(f'path {str(path)!r} has no path components')
    
    cursor = data

    for part in path.parts:
        cursor[part] = cursor.get(part, {})
        cursor = cursor[part]

    return data


def add_remote(path:Path, data:dict, root:str=None) -> dict:
    ''' add git repo remote to the last key or None '''

    # need root for get_remote()
    if root is not None:
        git_path = Path(root).expanduser() / path
    else:
        git_path = path
    
    remote = simplegit.git.get_remote(git_path)

    # traverse tree dict
    *parents, repo = path.parts
    cursor = data
    # print(f'{parents = }')
    # print(f'{repo    = }')
    # print(f'{data    = }')
    for part in parents:
        cursor = cursor[part]
    cursor[repo] = remote

    return data


def add_descriptor(data:dict, root:str, *exclude:str, **kwargs) -> dict:
    descriptor = {
        'root':root,
        'exclude':exclude,
        **kwargs
    }
    new = {}
    new['descriptor'] = descriptor
    new['data'] = data

    return new


def get_descriptor(data:dict) -> dict:
    return data['descriptor']


def get_data(data:dict) -> dict:
    return data['data']


def parse(data_in:dict, parents:list[str]=None, data_out:dict=None):
    data_out = data_out if data_out is not None else {}
    parents = parents if parents is not None else []


    items = list(data_in.items())
    for folder, value in items:

        if isinstance(value, dict):
            parse(data_in[folder], [*parents, folder], data_out)
        else:
            path = str(Path(*parents, folder))
            data_out[path] = value

    return data_out