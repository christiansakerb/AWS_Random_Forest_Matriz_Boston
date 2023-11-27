import pytest

from model.config.core import config
from model.processing.data_manager import load_dataset_test


@pytest.fixture()
def sample_input_data():
    return load_dataset_test(file_name=config.app_config.test_data_file)
