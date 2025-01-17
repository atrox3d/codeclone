from pathlib import Path
import subprocess
import os
import shlex
import logging

logger = logging.getLogger(__name__)

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


# def parse(cmdline:str):
    # return shlex.split(cmdline)
# 
# 
# @pushd
# def run(cmdline:str, dry_run:bool=True):
    # cmd, *params = parse(cmdline)
    # 
    # 
    # if not dry_run:
        # print(f'running {cmd} {" ".join(params)}')
    # else:
        # print(f'DRY_RUN | running {cmd} {" ".join(params)}')


def run(command:str, path:str=None, pushd:bool=False, dry_run:bool=True) -> subprocess.CompletedProcess:
    
    cwd = os.getcwd()
    logger.debug(f'{cwd = }')
    
    if path is not None:
        logger.debug(f'changing dir to {path = }')
        os.chdir(Path(path).resolve())

    # shlex.split breaks on windows paths
    # use Path(path).as_posix()
    # https://stackoverflow.com/a/63534016
    args = shlex.split(command)
    logger.debug(f'{command = }')
    logger.debug(f'{args = }')

    if dry_run:
        logger.info(f'dry_run | {args = }')
    else:
        try:
            logger.debug(f'run | {args = }')
            completed = subprocess.run(args, check=True, shell=False, capture_output=True, text=True)
            logger.debug(f'{completed = }')
            
            return completed
            
        except subprocess.CalledProcessError as cpe:
            # raise GitCommandException(**vars(cpe), path=path)
            logger.exception(cpe)
            raise
        
        finally:
            if path is not None and pushd:
                logger.debug(f'changing back to {cwd = }')
                os.chdir(cwd)


