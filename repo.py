from pathlib import Path

from paths import filter_excluded_paths, filter_only_dirs, make_relative_paths
from data import add_descriptor, add_remote, add_to_dict, get_data, get_descriptor, load, parse, save


def scan(
        root:str,
        *exclude:str,
        default_exclude:tuple=('.venv', '.git'),
        relative:bool=True
) -> list[Path]:
    '''
    scan root path and returns a list of repo paths
    
    if relative is True the paths start relative to root
    
    exclude and additional_excludes are joined and used to check which paths to exclude
    '''
    
    # expand ~ and check if valid path
    root = Path(root).expanduser()
    assert root.exists(), f'path {root} does not exist'
    
    # create exclude list
    exclude_paths = [*default_exclude, *exclude]
    
    # scan all git repos
    git_repos = root.glob('**/.git/')
    
    repo_dirs = filter_only_dirs(git_repos)
    repo_dirs = filter_excluded_paths(repo_dirs, exclude_paths)
    
    if relative:
        repo_dirs = make_relative_paths(root, *repo_dirs)
    
    return repo_dirs


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


def backup(json_path:str, root:str, *exclude:str, relative:bool, data:dict=None, indent:int=2) -> None:
    ''' compound function: scans path and saves json'''
    
    data = build_data(root, *exclude, relative=True)
    save(data, json_path, indent)


def restore(json_path:str, root:str, dry_run:bool=True, skip_existing:bool=True):
    
    data = load(json_path)
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
    
