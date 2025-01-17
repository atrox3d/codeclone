from pathlib import Path
from subprocess import CalledProcessError
import pytest
import commands
import os


@pytest.fixture
def testingdir():
    DIRNAME = 'testingdir'
    d = Path(DIRNAME)
    ad = d.resolve()
    
    # print(f'TESTINGDIR | mkdir {d}')
    d.mkdir()
    yield d
    # print(f'TESTINGDIR | rmdir {ad}')
    ad.rmdir()


@pytest.fixture
def testingfile(testingdir: Path):
    FILENAME = 'testingfile'
    f = Path(testingdir,  FILENAME)
    af = f.resolve()
    
    # print(f'TESTINGFILE | touch {f}')
    f.touch()
    yield f
    # print(f'TESTINGFILE | rm {af}')
    af.unlink()


def test_dry_run(testingfile: Path):
    ret =commands.run('ls', dry_run=True)
    assert ret is None


def test_change_path_during_run_without_pushd(testingdir:Path, testingfile: Path):
    cwd = Path.cwd()
    ret = commands.run('ls', testingdir, dry_run=False)
    
    assert ret.args == ['ls']
    assert ret.returncode == 0
    assert ret.stderr == ''
    assert ret.stdout == f'{testingfile.name}\n'
    
    # resetting test process path
    os.chdir(cwd)


def test_change_path_during_run_with_pushd(testingdir:Path, testingfile: Path):
    ret = commands.run('ls', testingdir, dry_run=False, pushd=True)
    
    assert ret.args == ['ls']
    assert ret.returncode == 0
    assert ret.stderr == ''
    assert ret.stdout == f'{testingfile.name}\n'


def test_simple_ls(testingdir:Path, testingfile: Path):
    ret =commands.run(f'ls {testingdir}', dry_run=False)
    
    assert ret.args == ['ls', str(testingdir)]
    assert ret.returncode == 0
    assert ret.stderr == ''
    assert ret.stdout == f'{testingfile.name}\n'


def test_error_raise_ls(testingdir:Path):
    with pytest.raises(CalledProcessError) as cpe:
        ret =commands.run(f'ls {testingdir}WRONGNAME', dry_run=False)
    print(f'{cpe.value.returncode = }')
    print(f'{cpe.value.cmd = }')
    print(f'{cpe.value.stdout = }')
    print(f'{cpe.value.stderr = }')


def test_error_noraise_ls(testingdir:Path):
    ret =commands.run(f'ls {testingdir}WRONGNAME', dry_run=False)
    print(f'{ret = }')