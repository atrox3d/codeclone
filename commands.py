from pathlib import Path
import subprocess
import os
import shlex
import logging

logger = logging.getLogger(__name__)


def pushd(fn):
    ''' decorator that saves and changes back to cwd after execution '''
    
    def wrapper(*args, **kwargs):
        cwd = os.getcwd()
        try:
            result = fn(*args, **kwargs)
            return result
        finally:
            os.chdir(cwd)
    return wrapper


def run(
        command:str, 
        path:str=None, 
        pushd:bool=False, 
        dry_run:bool=True, 
        check:bool=False
) -> subprocess.CompletedProcess|None:
    '''  '''
    
    logger.debug(f'{command = }')
    
    save_cwd = os.getcwd()
    logger.debug(f'{save_cwd = }')
    
    if path is not None:
        logger.debug(f'changing dir to {path = }')
        os.chdir(Path(path).resolve())

    # shlex.split breaks on windows paths
    # use Path(path).as_posix()
    # https://stackoverflow.com/a/63534016
    args = shlex.split(command)
    logger.debug(f'{args = }')

    if dry_run:
        logger.info(f'dry_run | {args = }')
        return None
    else:
        try:
            logger.debug(f'run | {args = }')
            completed = subprocess.run(args, check=check, shell=False, capture_output=True, text=True)
            logger.debug(f'{completed = }')
            
            return completed
            
        except subprocess.CalledProcessError as cpe:
            logger.exception(cpe)
            raise
        
        finally:
            if path is not None and pushd:
                logger.debug(f'changing back to {save_cwd = }')
                os.chdir(save_cwd)
