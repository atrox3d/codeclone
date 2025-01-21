from pathlib import Path
import tempfile
import pytest
import paths


def test_make_relative_paths(test_temp_dir, test_temp_content):
    relatives = paths.make_relative_paths(Path(test_temp_dir), *test_temp_content)
    assert relatives == [
            Path('one'), 
            Path('two'), 
            Path('three'), 
            Path('three/tmpfile')
    ]


def test_filter_excluded_path(test_temp_dir, test_temp_content):
    filtered = paths.filter_excluded_paths(
        paths.make_relative_paths(Path(test_temp_dir), *test_temp_content),
        ['one', 'two']
    )
    assert filtered == [
            Path('three'), 
            Path('three/tmpfile')
    ]


def test_filter_only_parent_of_dirs(test_temp_dir, test_temp_content):
    od = paths.filter_only_parent_of_dirs(test_temp_content)
    assert od == [Path(test_temp_dir) for _ in range(3)]


