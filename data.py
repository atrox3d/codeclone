import json
from pathlib import Path

from atrox3d import simplegit


def save(data:dict, json_path:str, indent:int=2) -> dict:

    with open(json_path, 'w') as fp:
        json.dump(data, fp, indent=indent)


def load(json_path:str) -> dict:

    with open(json_path) as fp:
        return json.load(fp)


def add_to_dict(path:Path, data:dict=None) -> dict:
    ''' create or add paths to dice as keys:dict with the last being {} '''

    data = data if data is not None else {}

    cursor = data

    for part in path.parts:
        cursor[part] = cursor.get(part, {})
        cursor = cursor[part]

    return data


def add_remote(path:Path, data:dict, root:str=None) -> str|None:
    ''' add git repo remote to the last key or None '''

    # need root for relative paths
    if root is not None:
        git_path = Path(root).expanduser() / path

    remote = simplegit.git.get_remote(git_path)

    # traverse tree dict
    *parents, repo = path.parts
    for part in parents:
        data = data[part]

    data[repo] = remote

    return remote


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