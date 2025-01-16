import argparse
from pathlib import Path


def add_backup_parser(subcommands:argparse._SubParsersAction) -> argparse.ArgumentParser:
    
    backup:argparse.ArgumentParser = subcommands.add_parser('backup')
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
    
    return backup


def add_restore_parser(subcommands:argparse._SubParsersAction) -> argparse.ArgumentParser:
    
    restore:argparse.ArgumentParser  = subcommands.add_parser('restore')
    restore.add_argument('-r', '--run', action='store_true', default=False)
    restore.add_argument('-s', '--skip-existing', action='store_true', default=True)
    restore.add_argument('-n', '--skip-no-remote', action='store_true', default=False)
    restore.add_argument('-i', '--ignore-existing', action='store_true', default=False)
    restore.add_argument('-w', '--suppress-warnings', action='store_true', default=False)
    restore.add_argument('-l', '--just-list', action='store_true', default=False)
    restore.add_argument('-W', '--list-path-width', type=int, default=100)
    
    return restore


def add_common_args(parser:argparse.ArgumentParser) -> None:
    parser.add_argument('-j', '--json', required=True)
    parser.add_argument('-p', '--path', required=True)


def get_options() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser()
    
    subcommands = parser.add_subparsers(dest='command', required=True)
    backup = add_backup_parser(subcommands)
    add_common_args(backup)
    
    restore = add_restore_parser(subcommands)
    add_common_args(restore)
    
    args = parser.parse_args()
    
    if args.command == 'restore':
        if args.run and args.ignore_existing:
            parser.error('--run and --ignore_existing cannot be both true')
    
    return args


def sort_options(args:argparse.Namespace, *names:str) -> list[str]:
    
    result = []
    
    for name in names:
        if name in vars(args):
            result.append(name)
    
    for name in vars(args):
        if name not in result:
            result.append(name)
    
    return result


def display(args:argparse.Namespace) -> bool:
    print('-' * 60)
    print('SELECTED OPTIONS')
    print('-' * 60)
    
    dargs = vars(args)
    for option in sort_options(args, 'command', 'path', 'json'):
        if option == 'path':
            print(f'{option:20}: {str(dargs[option]):10}          --> {Path(dargs[option]).expanduser()}')
        elif option == 'run':
            print(f'{option:20}: {str(dargs[option]):10}          --> DRY_RUN')
        else:
            print(f'{option:20}: {str(dargs[option]):10}')
    
    print('-' * 60)
    while (yn := input('do you wish to continue? (y/n) : ')).lower() not in 'yn':
        pass
    
    if yn == 'y':
        while (yn := input('are you sure ? (y/n) : ')).lower() not in 'yn':
            pass
        
    return yn == 'y'

