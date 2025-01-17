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
        raise_for_errors:bool=False
) -> subprocess.CompletedProcess|None:
    ''' wraps _run managing directory context '''
    
    save_cwd = os.getcwd()
    logger.debug(f'{save_cwd = }')
    
    if path is not None:
        logger.debug(f'changing dir to {path = }')
        os.chdir(Path(path).resolve())

    try:
        completed = _run(command=command, dry_run=dry_run, check=raise_for_errors)
        return completed
    
    except subprocess.CalledProcessError as cpe:
        logger.exception(cpe)
        raise
    finally:
        if path is not None and pushd:
            logger.debug(f'changing back to {save_cwd = }')
            os.chdir(save_cwd)


def _run(
        command:str, 
        dry_run:bool=True, 
        check:bool=False
) -> subprocess.CompletedProcess|None:
    ''' runs the command if dry_run is False, raises exception if check is True '''
    
    logger.debug(f'{command = }')

    # shlex.split breaks on windows paths
    # use Path(path).as_posix()
    # https://stackoverflow.com/a/63534016
    args = shlex.split(command)
    logger.debug(f'{args = }')

    if dry_run:
        logger.info(f'DRY_RUN | {args = }')
        return None
    else:
        logger.info(f'RUN     | {args = }')
        completed = subprocess.run(args, check=check, shell=False, capture_output=True, text=True)
        logger.debug(f'{completed = }')
        
        return completed
