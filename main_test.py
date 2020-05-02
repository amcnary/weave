import mock
import os
import pytest

from main import (
	InvalidPathError,
	concat_paths,
	list_files,
	describe_file,
	read_file,
)


TEST_USER = 'test_user'
TEST_FILENAME = 'test_name'
TEST_SIZE = 100
TEST_MODE = 111


class TestInvalidPathError:
	@pytest.fixture(scope="function")
	def invalid_path_error_impl(self):
		yield InvalidPathError('Test error')

	def test_to_dict(self, invalid_path_error_impl):
		expected = {
			'message': 'Test error'
		}
		assert invalid_path_error_impl.to_dict() == expected


def test_concat_paths():
	assert concat_paths('a','b') == 'a/b'


def test_read_file():
  mock_open = mock.mock_open(read_data='test contents')
  with mock.patch('__builtin__.open', mock_open):
    result = read_file('test_path')
  assert result['file'] == 'test contents'


class FakeStat:
	st_size = TEST_SIZE
	st_mode = TEST_MODE
	st_uid = 1


class FakePwuId:
	pw_name = TEST_USER


class TestListFiles:
	def test_exception_when_empty(self):
	  with pytest.raises(InvalidPathError):
	  	list_files('empty_dir')

	def test_nonempty_path(self):
		with mock.patch('os.listdir') as fake_listdir, \
				mock.patch('os.stat') as fake_stat, \
				mock.patch('main.getpwuid') as fake_getpwuid:
			fake_listdir.return_value = [TEST_FILENAME]
			fake_stat.return_value = FakeStat
			fake_getpwuid.return_value = FakePwuId
			result = list_files('dir')
		expected = {
			'files': [{
				'filename': TEST_FILENAME,
				'sizeBytes': TEST_SIZE,
				'owner': TEST_USER,
				'permissions': oct(TEST_MODE),
			}],
		}
		assert result == expected


def test_describe_file():
	with mock.patch('os.stat') as fake_stat, \
			mock.patch('main.getpwuid') as fake_getpwuid:
		fake_stat.return_value = FakeStat
		fake_getpwuid.return_value = FakePwuId
		result = describe_file('path', TEST_FILENAME)
	expected = {
		'filename': TEST_FILENAME,
		'sizeBytes': TEST_SIZE,
		'owner': TEST_USER,
		'permissions': oct(TEST_MODE),
	}
	assert result == expected

