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


def add_remote(path:Path, d:dict, root:str=None) -> str|None:
    ''' add git repo remote to the last key or None '''
    
    if root is not None:
        git_path = Path(root).expanduser() / path
    
    remote = simplegit.git.get_remote(git_path)
    
    *parents, repo = path.parts
    for part in parents:
        d = d[part]
    d[repo] = remote
    
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


def build_data(root:str, *exclude:str, relative:bool, data:dict=None) -> dict:
    ''' compound function: scans path and returns dict '''

    total = remotes = locals = 0

    for repo in scan(root, *exclude, relative=relative):
        data = add_to_dict(repo, data)
        remote = add_remote(repo, data, root)
        total += 1
        if remote is not None:
            remotes += 1
        else:
            locals += 1
    
    data = add_descriptor(
            data,
            root, 
            *exclude, 
            relative=relative, 
            total=total,
            remotes=remotes,
            locals=locals,
    )
    
    return data


def save(jsonpath:str, root:str, *exclude:str, relative:bool, data:dict=None) -> None:
    ''' compound function: scans path and saves json'''
    
    data = build_data(root, *exclude, relative=True)
    
    with open(jsonpath, 'w') as fp:
        json.dump(data, fp, indent=2)


def load(json_path:str) -> dict:
    with open(json_path) as fp:
        return json.load(fp)


def get_descriptor(data:dict) -> dict:
    return data['descriptor']


def get_data(data:dict) -> dict:
    return data['data']


def parse(data:dict, parents:list[str]=None, repos:dict=None, level:int=None):
    
    repos = repos if repos is not None else {}
    parents = parents if parents is not None else []
    level = level if level is not None else 0
    
    # print(f'{level*"  "}{parents = }')
    
    items = list(data.items())
    for folder, value in items:
        # print(f'{level*"  "}{folder = }')

        if isinstance(value, dict):
            level += 1
            # parents.append(folder)
            parse(data[folder], [*parents, folder], repos, level)
            # return result
        else:
            path = str(Path(*parents, folder))
            # print(path, value)
            repos[path] = value

    return repos


def restore(data:dict, root:str, dry_run:bool=True, skip_existing:bool=True):
    
    descriptor = get_descriptor(data)
    data = get_data(data)
    
    repos = parse(data)
    assert len(repos) == descriptor['total'], (
        f'total json repos ({descriptor['total']}) '
        f'differ from actual repos ({len(repos)})'
    )
    
    skipped = {}
    created = {}
    cwd = Path.cwd()
    for path, remote in repos.items():
        
        path = Path(path)
        if descriptor['relative']:
            path = Path(root).expanduser() / path
        
        git_path = (path / '.git/')
        if git_path.exists():
            if skip_existing:
                print(f'WARNING | path exists: {git_path}')
                print(f'WARNING | skipping...')
                skipped[path] = remote
                continue
            else:
                raise FileExistsError(git_path)
        
        mkdir = f'mkdir -p {path}'
        print(mkdir)
        
        created[path] = remote
        if remote is not None:
            cd = f'cd {mkdir}'
            print(cd)

            clone = f'git clone {remote} .'
            print(clone)
        
            cdback = f'cd {cwd}'
            print(cdback)
    
    print(created.keys())
    print()
    print()
    print()
    print(skipped.keys())
    
    assert skipped != created
    
