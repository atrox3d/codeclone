import repos
import options


if __name__ == "__main__":
    args = options.get_options()
    
    print(f'{args = }')

    data = {}

    if args.command == 'backup':
        repos.backup(args.json, args.path, relative=not args.absolute, indent=args.indent)
    
    elif args.command == 'restore':
        repos.restore(
                args.json, 
                args.path, 
                dry_run=not args.run, 
                skip_existing=args.skip_existing,
                ignore_existing=args.ignore_existing
        )
    
    else:
        raise ValueError(f'unknown command {args.command}')

