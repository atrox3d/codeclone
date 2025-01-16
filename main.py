import repos
import options


if __name__ == "__main__":
    args = options.get_options()
    
    if not options.display(args):
        print('exiting...')
        exit()
    
    data = {}

    if args.command == 'backup':
        repos.backup(
                args.json, 
                args.path, 
                relative=not args.absolute, 
                indent=args.indent,
                skip_no_remote=args.skip_no_remote,
        )
    
    elif args.command == 'restore':
        repos.restore(
                args.json, 
                args.path, 
                dry_run=not args.run, 
                skip_existing=args.skip_existing,
                skip_no_remote=args.skip_no_remote,
                ignore_existing=args.ignore_existing,
                suppress_warnings=args.suppress_warnings,
                just_list=args.just_list,
                list_path_width=args.list_path_width
        )
    
    else:
        raise ValueError(f'unknown command {args.command}')

