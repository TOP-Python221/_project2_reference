from pytest import mark, fixture

from src.model.files_io import PersistenceManager as PM
from src.utils.constants import DATA_DIR


def active_empty_files():
    return (DATA_DIR / 'tests').rglob('**/active_empty*.json')

def active_full_files():
    return (DATA_DIR / 'tests').rglob('**/active_full*.json')


@fixture
def active_state():
    return 'last_state'

@fixture
def active_keys(active_state):
    return {'kind', 'name', 'birthdate', active_state}


@fixture
def active_state_keys():
    return {'timestamp', 'health', 'stamina', 'hunger', 'thirst', 'intestine', 'joy', 'activity', 'anger', 'anxiety'}



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

    @mark.parametrize('file_path', active_full_files())
    def test_keys(self, file_path, active_keys, active_state, active_state_keys):
        data = PM.read_active(file_path)
        assert set(data) == active_keys, f'{file_path.name}'
        assert set(data[active_state]) == active_state_keys, f'{file_path.name}'


class TestActiveWrite:
    pass

