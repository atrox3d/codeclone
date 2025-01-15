import argparse


def add_backup_parser(subcommands:argparse._SubParsersAction):
    
    backup = subcommands.add_parser('backup')
    backup.add_argument(
            '-x', '--exclude',
            # dest='array',
            action='extend',
            nargs='+',
            type=str,
            default=[]
    )
    backup.add_argument('-r', '--relative', action='store_true', default=False)
    backup.add_argument('-i', '--indent', type=int, default=2)


def add_restore_parser(subcommands:argparse._SubParsersAction):
    
    restore = subcommands.add_parser('restore')
    restore.add_argument('-r', '--run', action='store_true', default=False)
    restore.add_argument('-s', '--skipexisting', action='store_true', default=True)


def get_options() -> argparse.Namespace:
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', required=True)
    parser.add_argument('-r', '--root', required=True)
    
    subcommands = parser.add_subparsers(dest='command', required=True)
    add_backup_parser(subcommands)
    add_restore_parser(subcommands)
    
    return parser.parse_args()
