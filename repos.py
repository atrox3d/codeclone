from pathlib import Path
from atrox3d import simplegit

    
def scan(start_path:str, relative:bool=True) -> list[Path]:
    
    start = Path(start_path).expanduser()
    assert start.exists(), f'path {start_path} does not exist'
    
    repos = start.glob('**/.git/')
    repo_dirs =  [d.parent for d in repos if d.is_dir() and '.venv' not in d.parts]
    
    if relative:
        repo_dirs = [Path(d).relative_to(start) for d in repo_dirs]
    
    return repo_dirs


def add_to_dict(path:Path, d:dict=None) -> dict:
    
    d = d if d is not None else {}
    c = d

    for part in path.parts:
        c[part] = c.get(part, {})
        c = c[part]
    
    return d


def add_remote(path:Path, root:str=None, d:dict=None) -> dict:
    
    if root is not None:
        git_path = Path(root).expanduser() / path
    
    remote = simplegit.git.get_remote(git_path)
    
    *parents, repo = path.parts
    for part in parents:
        d = d[part]
    d[repo] = remote
