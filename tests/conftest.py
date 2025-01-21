import tempfile
from typing import Generator
import pytest
from pathlib import Path
import commands
import subprocess


@pytest.fixture
def test_temp_dir() -> Generator[str, None, None]:
    '''creates a temp dir context and yields the path'''
    
    # print('FIXTURE | TEST_TEMP_DIR | start')
    with tempfile.TemporaryDirectory() as tdname:
        print(tdname, type(tdname))
        td = Path(tdname)
        assert td.exists()
        assert td.is_dir
        yield tdname

    assert not td.exists()
    # print('FIXTURE | TEST_TEMP_DIR | end')


@pytest.fixture
def clone_repo(test_temp_dir: str) -> subprocess.CompletedProcess:
    '''clones current repo inside temp dir'''
    
    # print('FIXTURE | CLONE_REPO | start')
    # print('FIXTURE | CLONE_REPO | end')
    return commands.run(
        f'git clone . {test_temp_dir}/testclone',
        raise_for_errors=True
    )


@pytest.fixture
def jsonpath(test_temp_dir: str) -> str:
    '''creates json path str inside temp dir'''
    
    # print('FIXTURE | JSONPATH | start')
    # print('FIXTURE | JSONPATH | end')
    return str(Path(test_temp_dir, 'repos.json'))


@pytest.fixture
def restore_root(test_temp_dir) -> Path:
    '''creates restore_root folder inside temp dir. returns path'''
    
    # print('FIXTURE | RESTORE_ROOT | start')
    restore_root = Path(test_temp_dir, 'restore_root')
    restore_root.mkdir()
    assert restore_root.exists()
    assert restore_root.is_dir()
    
    # print('FIXTURE | RESTORE_ROOT | end')
    return restore_root


@pytest.fixture
def restore_repo_relative(restore_root) -> str:
    '''returns testclone path inside temp dir/restore root as str'''
    
    # print('FIXTURE | RESTORE_REPO_RELATIVE | start')
    # print('FIXTURE | RESTORE_REPO_RELATIVE | end')
    return str(restore_root / 'testclone')


@pytest.fixture
def restore_repo_absolute(test_temp_dir) -> str:
    '''returns testclone path inside temp dir as str'''

    # print('FIXTURE | RESTORE_REPO_ABSOLUTE | start')
    # print('FIXTURE | RESTORE_REPO_ABSOLUTE | END')
    return str(Path(test_temp_dir) / 'testclone')


@pytest.fixture
def test_temp_content(test_temp_dir) -> Generator[Path, None, None]:
    '''creates 3 folders and 1 file inside temp dir, yields Path list'''
    
    td = Path(test_temp_dir)
    dirs = [Path(td, dir) for dir in 'one two three'.split()]
    [dir.mkdir() for dir in dirs]
    tmpfile = Path(dirs[-1], 'tmpfile')
    tmpfile.touch()
    dirs.append(tmpfile)
    yield dirs

