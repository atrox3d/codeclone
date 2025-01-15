from pathlib import Path
import subprocess
import os
import shlex


def pushd(fn):
    ''' changes back to cwd after execution '''
    
    def wrapper(*args, **kwargs):
        cwd = os.getcwd()
        try:
            result = fn(*args, **kwargs)
            return result
        finally:
            os.chdir(cwd)
    return wrapper


def parse(cmdline:str):
    return shlex.split(cmdline)


@pushd
def run(cmdline:str, dry_run:bool=True):
    cmd, *params = parse(cmdline)
    
    
    if not dry_run:
        print(f'running {cmd} {" ".join(params)}')
    else:
        print(f'DRY_RUN | running {cmd} {" ".join(params)}')
