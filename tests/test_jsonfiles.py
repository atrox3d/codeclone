from pathlib import Path
import tempfile
import pytest

import jsonfiles as jf


def test_save(test_temp_dir):
    jsonpath = Path(test_temp_dir, 'test.json')
    jf.save({}, jsonpath)
    assert jsonpath.exists()


def test_load(test_temp_dir):
    jsonpath = Path(test_temp_dir, 'test.json')
    jf.save({}, jsonpath)
    data = jf.load(jsonpath)
    assert data == {}
