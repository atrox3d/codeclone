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
        #
        dry_run:bool=False, 
        raise_for_errors:bool=False,
        shell:bool=False,
        #
        ask_confirmation:bool=False,
        make_sure:bool=False,
) -> subprocess.CompletedProcess|None:
    '''wraps _run managing directory context and other actions/options'''

    if ask_confirmation:
        if not confirm(make_sure=make_sure):
            return None

    if dry_run:
        logger.info(f'DRY_RUN | {command = }')
        return None
    else:
        save_cwd = os.getcwd()
        logger.debug(f'{save_cwd = }')

        if path is not None:
            logger.debug(f'changing dir to {path = }')
            os.chdir(Path(path).resolve())

        try:
            completed = _run(command=command, check=raise_for_errors, shell=shell)
            return completed
        
        except subprocess.CalledProcessError as cpe:
            logger.exception(cpe)
            raise
        
        finally:
            if pushd:
                logger.debug(f'changing back to {save_cwd = }')
                os.chdir(save_cwd)


def _run(
        command:str, 
        check:bool=False,
        shell:bool=False
) -> subprocess.CompletedProcess|None:
    ''' runs the command if dry_run is False, raises exception if check is True '''
    options = locals()
    print(options)
    logger.debug(f'{command = }')

    # shlex.split breaks on windows paths
    # use Path(path).as_posix()
    # https://stackoverflow.com/a/63534016
    args = shlex.split(command)
    logger.debug(f'{args = }')

    logger.info(f'RUN     | {args = }')
    completed = subprocess.run(args, check=check, shell=shell, capture_output=True, text=True)
    logger.debug(f'{completed = }')
        
    return completed


def confirm(
        prompt:str='do you wish to continue? (y/n) : ',
        make_sure:bool=False,
        sure_prompt:str='are you sure ? (y/n) : ',
        yes:str='y',
        no:str='n',
) -> bool:
    yesno = ''.join([yes, no])
    while (answer := input(prompt)).lower() not in yesno:
        pass
    
    if answer == yes and make_sure:
        while (answer := input(sure_prompt)).lower() not in yesno:
            pass
        
    return answer == yes
