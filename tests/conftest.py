import tempfile
import pytest
from pathlib import Path
import commands
import subprocess


@pytest.fixture(scope='module')
def test_temp_dir():
    # print('FIXTURE | TEST_TEMP_DIR | start')
    with tempfile.TemporaryDirectory() as tdname:
        print(tdname, type(tdname))
        td = Path(tdname)
        assert td.exists()
        assert td.is_dir
        yield tdname

    assert not td.exists()
    # print('FIXTURE | TEST_TEMP_DIR | end')


@pytest.fixture(scope='module')
def clone_repo(test_temp_dir: str) -> subprocess.CompletedProcess:
    # print('FIXTURE | CLONE_REPO | start')
    # print('FIXTURE | CLONE_REPO | end')
    return commands.run(
        f'git clone . {test_temp_dir}/testclone',
        raise_for_errors=True
    )


@pytest.fixture
def jsonpath(test_temp_dir: str) -> str:
    # print('FIXTURE | JSONPATH | start')
    # print('FIXTURE | JSONPATH | end')
    return str(Path(test_temp_dir, 'repos.json'))


@pytest.fixture
def restore_root(test_temp_dir) -> Path:
    # print('FIXTURE | RESTORE_ROOT | start')
    restore_root = Path(test_temp_dir, 'restore_root')
    restore_root.mkdir()
    assert restore_root.exists()
    assert restore_root.is_dir()
    
    # print('FIXTURE | RESTORE_ROOT | end')
    return restore_root


@pytest.fixture
def restore_repo_relative(restore_root) -> str:
    # print('FIXTURE | RESTORE_REPO_RELATIVE | start')
    # print('FIXTURE | RESTORE_REPO_RELATIVE | end')
    return str(restore_root / 'testclone')


@pytest.fixture
def restore_repo_absolute(test_temp_dir) -> str:
    # print('FIXTURE | RESTORE_REPO_ABSOLUTE | start')
    # print('FIXTURE | RESTORE_REPO_ABSOLUTE | END')
    return str(Path(test_temp_dir) / 'testclone')


@pytest.fixture(scope='module')
def test_temp_content(test_temp_dir):
    td = Path(test_temp_dir)
    dirs = [Path(td, dir) for dir in 'one two three'.split()]
    [dir.mkdir() for dir in dirs]
    tmpfile = Path(dirs[-1], 'tmpfile')
    tmpfile.touch()
    dirs.append(tmpfile)
    yield dirs

