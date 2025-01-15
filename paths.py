from pathlib import Path


def make_relative_paths(root:Path, *paths:str|Path) -> list[Path]:
    ''' convert path from absolute to relative to root, cutting out root path '''

    return [path.relative_to(root) for path in paths]


def filter_excluded_paths(paths:list[Path], exclude:list[str]) -> list[Path]:
    '''  '''

    return [path for path in paths
                if not any(part in exclude for part in path.parts)]


def filter_only_dirs(paths:list[Path]) -> list[Path]:
    '''  '''

    return [path.parent for path in paths if path.is_dir()]