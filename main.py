import repos
import options


if __name__ == "__main__":
    args = options.get_options()

    data = {}

    if args.command == 'backup':
        repos.backup(args.json, args.root, relative=args.relative, indent=args.indent)
    
    elif args.command == 'restore':
        repos.restore(args.json, args.root, dry_run=not args.run, skip_existing=args.skipexisting)
    
    else:
        raise ValueError(f'unknown command {args.command}')

