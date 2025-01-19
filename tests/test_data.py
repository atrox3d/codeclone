from pathlib import Path

import data as dtx
from atrox3d import simplegit


def test_add_path():
    data = dtx.add_path(Path('/test/path/to/file'), {})
    assert data == {
        '/': {
            'test': {
                'path': {
                    'to': {
                        'file': {}
                    }
                }
            }
        }
    }


def test_add_remote():
    repo_path = Path('.').resolve()
    
    data = dtx.add_path(repo_path, {})
    
    remote = simplegit.git.get_remote(repo_path)
    data = dtx.add_remote(repo_path, data)
    
    for part in repo_path.parts:
        data = data[part]
    assert data == remote


def test_add_deascriptor():
    data = dtx.add_descriptor({}, 'root', 'exclude', somearg=None)
    assert data['data'] == {}
    assert data['descriptor'] == {
        'root': 'root',
        'exclude': ('exclude',),
        'somearg': None
    }


def test_get_deascriptor():
    data = dtx.add_descriptor({}, 'root', 'exclude', somearg=None)
    assert dtx.get_descriptor(data) == {
        'root': 'root',
        'exclude': ('exclude',),
        'somearg': None
    }


def test_get_data():
    data = dtx.add_descriptor({}, 'root', 'exclude', somearg=None)
    assert dtx.get_data(data) == {}


def test_parse():
    data = {
        '/': {
            'test': {
                'path': {
                    'torepo1': {
                        'repo1': 'https://repo.git',
                    },
                    'torepo2': {
                        'repo2': 'https://repo.git',
                    },
                }
            }
        }
    }
    parsed = dtx.parse(data)
    assert parsed == {
        '/test/path/torepo1/repo1': 'https://repo.git', 
        '/test/path/torepo2/repo2': 'https://repo.git'
    }