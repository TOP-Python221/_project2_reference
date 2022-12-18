from pytest import mark

from src.model.files_io import PersistenceManager as PM
from src.utils.constants import DATA_DIR


def active_empty_files():
    return (DATA_DIR / 'tests').rglob('**/active_empty*.json')


class TestParametersRead:
    pass


class TestActiveRead:

    def test_not_existing(self):
        data = PM.read_active(DATA_DIR / 'tests/not_existing.json')
        assert data == {}

    @mark.parametrize('file_path', active_empty_files())
    def test_empty(self, file_path):
        data = PM.read_active(file_path)
        assert data == {}, f'{file_path.name}'


class TestActiveWrite:
    pass

