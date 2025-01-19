from pathlib import Path
import tempfile

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
    data = dtx.add_descriptor(
        {},
        'root',
        'exclude',
        somearg=None
    )
    
    assert data['data'] == {}
    assert data['descriptor'] == {
        'root': 'root',
        'exclude': ('exclude',),
        'somearg': None
    }
