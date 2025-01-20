from pathlib import Path
import logging
import subprocess

import paths
import data as dtx
import jsonfiles
import commands


logger = logging.getLogger(__name__)


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
    root = Path(root).expanduser()#.resolve()
    assert root.exists(), f'path {root} does not exist'
    
    # create exclude list
    exclude_paths = [*default_exclude, *exclude]
    
    # scan all git repos
    git_repos = root.glob('**/.git/')
    
    repo_dirs = paths.filter_only_parent_of_dirs(git_repos)
    repo_dirs = paths.filter_excluded_paths(repo_dirs, exclude_paths)
    
    if relative:
        repo_dirs = paths.make_relative_paths(root, *repo_dirs)
    
    return repo_dirs


def backup(
        root:str, 
        *exclude:str, 
        json_path:str=None,
        relative:bool, 
        data:dict=None, 
        indent:int=2,
        skip_no_remote:bool=False,
) -> dict:
    ''' compound function: scans path and saves json'''
    total = remotes = locals = 0
    data = {} if data is None else data
    
    for repo in scan(root, *exclude, relative=relative):
        
        assert Path(root) != repo, f'repo path {repo!r} and root path {root!r} cannot be the same'
        
        data = dtx.add_path(repo, data)
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
    
    if json_path is not None:
        jsonfiles.save(data, json_path, indent)
    
    return data


def update_restore_status(
        results:dict,
        path:Path|str,
        remote:str=None,
        skipped_existing:bool=None,
        skipped_noremote:bool=None,
        listed:bool=None,
        created:bool=None,
        cloned:bool=None,
        completed:subprocess.CompletedProcess=None,
) -> dict:
    status_args = {k:v for k, v in locals().items() if k not in ['results', 'path', 'remote']}
    # print(status_args)
    path = str(path)
    results[path] = results.get(path, {
        'remote': remote,
        'status': {
            'skipped_existing': None,
            'skipped_noremote': None,
            'listed': None,
            'created': None,
            'cloned': None,
            'completed': None,
        }
    })
    
    status_update = {
        k: v if results[path]['status'][k] is None else results[path]['status'][k]
        for k, v in status_args.items()
    }
    
    results[path]['status'] = status_update
    return status_update


def restore(
        json_path:str, 
        root:str, 
        dry_run:bool=True, 
        skip_existing:bool=True,
        skip_no_remote:bool=False,
        # ignore_existing:bool=False,
        suppress_warnings:bool=False,
        just_list:bool=False,
        list_path_width:int=100
) -> dict:
    
    data = jsonfiles.load(json_path)
    descriptor = dtx.get_descriptor(data)
    data = dtx.get_data(data)
    
    repos = dtx.parse(data)
    assert len(repos) == descriptor['total'], (
        f'total json repos ({descriptor['total']}) '
        f'differ from actual repos ({len(repos)})'
    )
    
    # skipped_existing = {}
    # skipped_noremote = {}
    # created = {}
    # listed = {}
    # cloned = {}
    results = {}
    for path, remote in repos.items():
        if skip_no_remote and remote is None:
            update_restore_status(results, path, remote, skipped_noremote=True)
            # results[path]['skipped_noremote'] = True
            continue
        
        path = Path(path)
        if descriptor['relative']:
            path = Path(root).expanduser() / path
        
        git_path = (path / '.git/')
        if git_path.exists():
            # if ignore_existing and dry_run:
                # pass
            if skip_existing:
                if not suppress_warnings:
                    logger.warning(f'SKIPPING | path exists: {git_path}')
                update_restore_status(results, path, remote, skipped_existing=True)
                # skipped_existing[path] = remote
                continue
            else:
                raise FileExistsError(git_path)
        
        if just_list:
            update_restore_status(results, path, remote, listed=True)
            # listed[path] = remote
            print(f'{path!s:{list_path_width}} {remote}')
            continue
        
        
        commands.run(
                f'mkdir -p {path}', 
                dry_run=dry_run,
                raise_for_errors=True
                )
        update_restore_status(results, path, remote, created=True)
        # created[path] = remote
        
        if remote is not None:
            # commands.run(f'cd {path}', dry_run)
            completed = commands.run(
                        f'git clone {remote} .', 
                        dry_run=dry_run,
                        path=path,
                        pushd=True,
                        raise_for_errors=True
                    )
            update_restore_status(results, path, remote, 
                    cloned=True,
                    completed=completed
            )
            # cloned[path] = remote
            # commands.run(f'cd {cwd}', dry_run)
    
    # assert skipped != created
    # results['skipped_noremote'] = skipped_noremote
    # results['skipped_existing'] = skipped_existing
    # results['created'] = created
    # results['cloned'] = created
    # results['listed'] = listed
    
    return results


def describe(json_path:str):
    descriptor:dict = jsonfiles.load(json_path)['descriptor']
    
    print('-' * 60)
    print(f'backup descriptor of {json_path}')
    print('-' * 60)
    for k, v in descriptor.items():
        print(f'{k:20}: {v}')
    
    print('-' * 60)
