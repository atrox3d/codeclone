from pathlib import Path

import paths
import data as dtx
import files
import commands

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
    
    repo_dirs = paths.filter_only_dirs(git_repos)
    repo_dirs = paths.filter_excluded_paths(repo_dirs, exclude_paths)
    
    if relative:
        repo_dirs = paths.make_relative_paths(root, *repo_dirs)
    
    return repo_dirs


def backup(
        json_path:str, 
        root:str, 
        *exclude:str, 
        relative:bool, 
        data:dict=None, 
        indent:int=2,
        skip_no_remote:bool=False,
) -> None:
    ''' compound function: scans path and saves json'''
    total = remotes = locals = 0

    for repo in scan(root, *exclude, relative=relative):
        data = dtx.add_to_dict(repo, data)
        remote = dtx.add_remote(repo, data, root)
        total += 1
        if remote is not None:
            remotes += 1
        else:
            locals += 1
            if skip_no_remote:
                continue
    
    data = dtx.add_descriptor(
            data,
            root, 
            *exclude, 
            relative=relative, 
            total=total,
            remotes=remotes,
            locals=locals,
    )

    files.save(data, json_path, indent)


def restore(
        json_path:str, 
        root:str, 
        dry_run:bool=True, 
        skip_existing:bool=True,
        skip_no_remote:bool=False,
        ignore_existing:bool=False,
        suppress_warnings:bool=False,
        just_list:bool=False,
        list_path_width:int=100
):
    
    data = files.load(json_path)
    descriptor = dtx.get_descriptor(data)
    data = dtx.get_data(data)
    
    repos = dtx.parse(data)
    assert len(repos) == descriptor['total'], (
        f'total json repos ({descriptor['total']}) '
        f'differ from actual repos ({len(repos)})'
    )
    
    skipped = {}
    created = {}
    for path, remote in repos.items():
        
        if skip_no_remote and remote is None:
            continue
        
        path = Path(path)
        if descriptor['relative']:
            path = Path(root).expanduser() / path
        
        git_path = (path / '.git/')
        if git_path.exists():
            if ignore_existing and dry_run:
                pass
            elif skip_existing:
                if not suppress_warnings:
                    print(f'WARNING | SKIPPING | path exists: {git_path}')
                # print(f'WARNING | skipping...')
                skipped[path] = remote
                continue
            else:
                raise FileExistsError(git_path)
        
        if just_list:
            print(f'{path!s:{list_path_width}} {remote}')
            continue
        
        
        commands.run(f'mkdir -p {path}', dry_run)
        
        created[path] = remote
        if remote is not None:
            # commands.run(f'cd {path}', dry_run)
            commands.run(f'git clone {remote} .', dry_run)
            # commands.run(f'cd {cwd}', dry_run)
    
    assert skipped != created
    
