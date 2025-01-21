from pathlib import Path
import subprocess

import repos
import jsonfiles


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

