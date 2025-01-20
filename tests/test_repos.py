from pathlib import Path
import tempfile
import pytest
import paths

import repos
import commands
import jsonfiles


@pytest.fixture(scope='module')
def test_temp_dir():
    with tempfile.TemporaryDirectory() as tdname:
        print(tdname, type(tdname))
        td = Path(tdname)
        assert td.exists()
        assert td.is_dir
        yield tdname

    assert not td.exists()


@pytest.fixture(scope='module')
def clone_repo(test_temp_dir):
    return commands.run(
        f'git clone . {test_temp_dir}/testclone',
        raise_for_errors=True
    )


def test_fixture(test_temp_dir, clone_repo):
    print([
        str(p.relative_to(test_temp_dir))
        for p in
        Path(test_temp_dir).glob('*/*')
    ])
    print(clone_repo.returncode)
    print(clone_repo.stdout)
    print(clone_repo.stderr)


def test_scan_relative():
    root = str(Path.cwd())

    scanned = repos.scan(root)
    assert scanned == [Path('.')]


def test_scan_absolute():
    root = Path.cwd()

    scanned = repos.scan(str(root), relative=False)
    assert scanned == [root]


def test_backup_todict_relative(test_temp_dir, clone_repo):
    data = repos.backup(test_temp_dir, relative=True)
    print(data)
    
    assert list(data.keys()) == ['descriptor', 'data']
    assert list(data['descriptor'].keys()) == [
        'root', 'exclude', 'relative', 'total', 'remotes', 'locals'
    ]
    assert list(data['data'].keys()) == ['testclone']


def test_backup_todict_absolute(test_temp_dir, clone_repo):
    data = repos.backup(test_temp_dir, relative=False)
    
    assert list(data.keys()) == ['descriptor', 'data']
    assert list(data['descriptor'].keys()) == [
        'root', 'exclude', 'relative', 'total', 'remotes', 'locals'
    ]
    
    cursor = data['data']
    parts = Path(test_temp_dir).parts
    for part in parts:
        cursor = cursor[part]
    assert list(cursor.keys()) == ['testclone']
    assert cursor['testclone'] != {}


def test_backup_tojson_relative(test_temp_dir, clone_repo):
    jsonpath = str(Path(test_temp_dir, 'repos.json'))
    data = repos.backup(test_temp_dir, json_path=jsonpath, relative=True)
    jsondata = jsonfiles.load(jsonpath)
    
    assert jsondata == data


def test_backup_tojson_absolute(test_temp_dir, clone_repo):
    jsonpath = str(Path(test_temp_dir, 'repos.json'))
    data = repos.backup(test_temp_dir, json_path=jsonpath, relative=False)
    jsondata = jsonfiles.load(jsonpath)
    
    assert jsondata == data

