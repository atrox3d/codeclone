from pathlib import Path
import tempfile

import data as dtx


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
    pass