import argparse
from pathlib import Path
import sys


def __verbose():
    ''' https://code.google.com/archive/p/argparse/issues/54 '''
    
    verbose_parser = argparse.ArgumentParser(add_help=False) 
    verbose_parser.add_argument('--verbose', action='store_true')
    
    parser = argparse.ArgumentParser(parents=[verbose_parser]) 
    subparsers = parser.add_subparsers() 
    foo_parser = subparsers.add_parser('foo', parents=[verbose_parser])


def _add_backup_args(backup:argparse.ArgumentParser) -> argparse.ArgumentParser:
    
    backup.add_argument(
            '-x', '--exclude',
            # dest='array',
            action='extend',
            nargs='+',
            type=str,
            default=[]
    )
    backup.add_argument('-a', '--absolute', action='store_true')
    backup.add_argument('-i', '--indent', type=int, default=2)
    backup.add_argument('-n', '--skip-no-remote', action='store_true', default=False)
    
    return backup


def _add_restore_args(restore:argparse.ArgumentParser) -> argparse.ArgumentParser:
    
    restore.add_argument('-r', '--run', action='store_true', default=False)
    restore.add_argument('-s', '--skip-existing', action='store_true', default=True)
    restore.add_argument('-n', '--skip-no-remote', action='store_true', default=False)
    restore.add_argument('-i', '--ignore-existing', action='store_true', default=False)
    restore.add_argument('-w', '--suppress-warnings', action='store_true', default=False)
    restore.add_argument('-l', '--just-list', action='store_true', default=False)
    restore.add_argument('-W', '--list-path-width', type=int, default=100)
    
    return restore


def _add_common_args(parser:argparse.ArgumentParser) -> argparse.ArgumentParser:
    ''' TODO: use parents= '''
    
    parser.add_argument('-j', '--json', required=True)
    parser.add_argument('-p', '--path', required=True)
    
    return parser


def _build_parser() -> argparse.ArgumentParser:
    
    common = argparse.ArgumentParser(add_help=False)
    _add_common_args(common)
    
    # https://code.google.com/archive/p/argparse/issues/54
    parser = argparse.ArgumentParser(
                # parents=[common], 
                add_help=False
            )

    subcommands = parser.add_subparsers(dest='command', required=True)
    
    backup = subcommands.add_parser( 'backup', parents=[common])
    backup = _add_backup_args(backup)
    
    restore  = subcommands.add_parser('restore', parents=[common])
    restore = _add_restore_args(restore)

    return parser


def _sort(args:argparse.Namespace, *name_index:str) -> list[str]:
    
    result = []
    
    for name in name_index:
        if name in vars(args):
            result.append(name)
    
    for name in vars(args):
        if name not in result:
            result.append(name)
    
    return result


def get(args=sys.argv[1:]) -> argparse.Namespace:
    
    parser = _build_parser()
    print(f'{args = }')
    args = parser.parse_args(args)
    
    # if args.command == 'restore':
        # if args.run and args.ignore_existing:
            # parser.error('--run and --ignore_existing cannot be both true')
    # 
    return args


def display(args:argparse.Namespace) -> bool:
    
    print('-' * 60)
    print('SELECTED OPTIONS')
    print('-' * 60)
    
    dargs = vars(args)
    print(f'{dargs = }')
    for option in _sort(args, 'command', 'path', 'json'):
        if option == 'path':
            print(f'{option:20}: {str(dargs[option]):20}          --> {Path(dargs[option]).expanduser()}')
        elif option == 'run':
            if dargs[option]:
                print(f'{option:20}: {str(dargs[option]):20}          --> * EXECUTE *')
            else:
                print(f'{option:20}: {str(dargs[option]):20}          --> DRY_RUN')
        else:
            print(f'{option:20}: {str(dargs[option]):20}')


def confirm() -> bool:
    
    while (yn := input('do you wish to continue? (y/n) : ')).lower() not in 'yn':
        pass
    
    if yn == 'y':
        while (yn := input('are you sure ? (y/n) : ')).lower() not in 'yn':
            pass
        
    return yn == 'y'


if __name__ == "__main__":
    print(get())