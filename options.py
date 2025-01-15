import argparse


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
    restore.add_argument('-i', '--ignore-existing', action='store_true', default=True)
    
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
