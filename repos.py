import json
from operator import add
from pathlib import Path
from atrox3d import simplegit


def scan(
        root:str,
        *exclude:str,
        default_exclude:tuple=('.venv',), 
        relative:bool=True
) -> list[Path]:
    '''
    scan root path and returns a list of repo paths
    
    if relative is True the paths start relative to root
    
    exclude and additional_excludes are joined and used to check which paths to exclude
    '''
    
    # expand ~ and check if valid path
    start = Path(root).expanduser()
    assert start.exists(), f'path {root} does not exist'
    
    # create exclude list
    # exclude = [] if exclude is None else exclude
    exclude_paths = [*default_exclude, *exclude]
    
    # scan all git repos
    repos = start.glob('**/.git/')
    repo_dirs =  [
            d.parent for d in repos                     # save parent
            if d.is_dir()                               # if d is a dir
            and not any(                                # and does not contain
                p in exclude_paths for p in d.parts     # any of excluded names
            )
    ]
    
    # cut the root part if relative
    if relative:
        repo_dirs = [Path(d).relative_to(start) for d in repo_dirs]
    
    return repo_dirs


def add_to_dict(path:Path, d:dict=None) -> dict:
    ''' create or add paths to dice as keys:dict with the last being {} '''
    
    # create dict if not passed
    d = d if d is not None else {}
    
    cursor = d

    for part in path.parts:
        cursor[part] = cursor.get(part, {})
        cursor = cursor[part]
    
    return d


def add_remote(path:Path, d:dict, root:str=None) -> None:
    ''' add git repo remote to the last key or None '''
    
    if root is not None:
        git_path = Path(root).expanduser() / path
    
    remote = simplegit.git.get_remote(git_path)
    
    *parents, repo = path.parts
    for part in parents:
        d = d[part]
    d[repo] = remote


def build_data(root:str, *exclude:str, relative:bool, data:dict=None) -> dict:
    ''' compound function: scans path and returns dict '''

    for repo in scan(root, *exclude, relative=relative):
        data = add_to_dict(repo, data)
        add_remote(repo, data, root)
    
    return data


def save_to_json(jsonpath:str, root:str, *exclude:str, relative:bool, data:dict=None) -> None:
    ''' compound function: scans path and saves json'''
    
    data = build_data(root, *exclude, relative=True)
    
    with open(jsonpath, 'w') as fp:
        json.dump(data, fp, indent=2)

