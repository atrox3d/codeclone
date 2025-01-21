from pathlib import Path
import subprocess

import repos
import jsonfiles


def test_fixture(test_temp_dir: str, clone_repo: subprocess.CompletedProcess):
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


def test_backup_todict_relative(test_temp_dir: str, clone_repo: subprocess.CompletedProcess):
    data = repos.backup(test_temp_dir, relative=True)
    print(data)
    
    assert list(data.keys()) == ['descriptor', 'data']
    assert list(data['descriptor'].keys()) == [
        'root', 'exclude', 'relative', 'total', 'remotes', 'locals'
    ]
    assert list(data['data'].keys()) == ['testclone']


def test_backup_todict_absolute(test_temp_dir: str, clone_repo: subprocess.CompletedProcess):
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


def test_backup_tojson_relative(
    test_temp_dir: str, 
    clone_repo: subprocess.CompletedProcess,
    jsonpath:str
):
    data = repos.backup(test_temp_dir, json_path=jsonpath, relative=True)
    jsondata = jsonfiles.load(jsonpath)
    
    assert jsondata == data


def test_backup_tojson_absolute(
    test_temp_dir: str, 
    clone_repo: subprocess.CompletedProcess,
    jsonpath:str
):
    data = repos.backup(test_temp_dir, json_path=jsonpath, relative=False)
    jsondata = jsonfiles.load(jsonpath)
    
    assert jsondata == data


def test_restore_relative_list(
    test_temp_dir: str, 
    clone_repo: subprocess.CompletedProcess,
    jsonpath:str,
    restore_root:Path,
    restore_repo_relative:str
):
    data = repos.backup(test_temp_dir, json_path=jsonpath, relative=True)
    results = repos.restore(
        jsonpath,
        restore_root,
        just_list=True
    )
    
    assert results.get(restore_repo_relative) is not None
    result = results[restore_repo_relative]
    
    assert 'remote' in result.keys()
    assert result['remote'] is not None
    
    assert 'status' in result.keys()
    status = result['status']
    assert sum(1 for k, v in status.items() if v is not None) == 1
    assert status['listed'] is True


def test_restore_absolute_list(
    test_temp_dir: str, 
    clone_repo: subprocess.CompletedProcess,
    jsonpath:str,
    restore_root:Path,
    restore_repo_absolute:str
):
    data = repos.backup(test_temp_dir, json_path=jsonpath, relative=False)
    results = repos.restore(
        jsonpath,
        restore_root,
        just_list=True
    )
    print(f'{results = }')
    print(f'{restore_repo_absolute = }')
    assert results.get(restore_repo_absolute) is not None
    result = results[restore_repo_absolute]
    
    assert 'remote' in result.keys()
    assert result['remote'] is not None
    
    assert 'status' in result.keys()
    status = result['status']
    assert sum(1 for k, v in status.items() if v is not None) == 1
    # assert status['listed'] is True
    
    