from pathlib import Path
import pytest
import commands
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def testingdir():
    DIRNAME = 'testingdir'
    t = Path(DIRNAME)
    
    logger.info(f'mkdir {DIRNAME}')
    t.mkdir()
    yield t
    logger.info(f'rmdir {DIRNAME}')
    t.rmdir()


@pytest.fixture
def testingfile(testingdir: Path):
    FILENAME = 'testingfile'
    f = Path(testingdir,  FILENAME)
    
    logger.info(f'touch {FILENAME}')
    f.touch()
    yield f
    logger.info(f'rm {FILENAME}')
    f.unlink()


# def test_fixtures(testingfile: Path):
    # pass


def test_dry_run(testingfile: Path):
    ret =commands.run('ls', dry_run=True)
    print(ret)


def test_ls(testingdir:Path, testingfile: Path):
    ret =commands.run(f'ls {testingdir}', dry_run=False)
    
    print(ret)
    assert ret.args == ['ls', str(testingdir)]
    assert ret.returncode == 0
    assert ret.stderr == ''
    assert ret.stdout == f'{testingfile.name}\n'
