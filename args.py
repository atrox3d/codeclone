import argparse
import sys


def parse(args=sys.argv[2:]):
    ''' https://code.google.com/archive/p/argparse/issues/54 '''
    
    print(f'{args = }')
    
    verbose_parser = argparse.ArgumentParser(add_help=False) 
    verbose_parser.add_argument('-v', '--verbose', action='store_true')
    
    parser = argparse.ArgumentParser(parents=[verbose_parser]) 
    subparsers = parser.add_subparsers(dest='command') 
    
    foo = subparsers.add_parser('foo', parents=[verbose_parser])
    foo.add_argument('-f', '-foo')
    
    bar = subparsers.add_parser('bar', parents=[verbose_parser])
    bar.add_argument('-b', '-bar')
    
    return parser.parse_args(args)


if __name__ == "__main__":
    print(parse('-v foo'.split()))
    print(parse('foo -v'.split()))
    