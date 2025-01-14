from pathlib import Path

    
def scan(start_path:str, relative:bool=True) -> list[Path]:
    
    start = Path(start_path).expanduser()
    assert start.exists(), f'path {start_path} does not exist'
    
    repos = start.glob('**/.git/')
    repo_dirs =  [d for d in repos if d.is_dir()]
    
    if relative:
        repo_dirs = [Path(d).relative_to(start) for d in repo_dirs]
    
    return repo_dirs
