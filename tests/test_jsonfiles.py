from pathlib import Path
import tempfile
import pytest

import jsonfiles as jf


@pytest.fixture(scope='module')
def test_temp_dir():
    with tempfile.TemporaryDirectory() as tdname:
        print(tdname, type(tdname))
        td = Path(tdname)
        assert td.exists()
        assert td.is_dir
        yield tdname

    assert not td.exists()


def test_save(test_temp_dir):
    jsonpath = Path(test_temp_dir, 'test.json')
    jf.save({}, jsonpath)
    assert jsonpath.exists()


def test_load(test_temp_dir):
    jsonpath = Path(test_temp_dir, 'test.json')
    data = jf.load(jsonpath)
    assert data == {}
