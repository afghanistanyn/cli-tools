import json
import pathlib
from typing import Dict

import pytest


@pytest.fixture
def api_bundle_id() -> Dict:
    mock_path = pathlib.Path(__file__).parent / 'mocks' / 'bundle_id.json'
    return json.loads(mock_path.read_text())


@pytest.fixture
def api_bundle_id_capability() -> Dict:
    mock_path = pathlib.Path(__file__).parent / 'mocks' / 'bundle_id_capability.json'
    return json.loads(mock_path.read_text())


@pytest.fixture
def api_certificate() -> Dict:
    mock_path = pathlib.Path(__file__).parent / 'mocks' / 'certificate.json'
    return json.loads(mock_path.read_text())


@pytest.fixture
def api_device() -> Dict:
    mock_path = pathlib.Path(__file__).parent / 'mocks' / 'device.json'
    return json.loads(mock_path.read_text())


@pytest.fixture
def api_error_response() -> Dict:
    mock_path = pathlib.Path(__file__).parent / 'mocks' / 'error_response.json'
    return json.loads(mock_path.read_text())


@pytest.fixture
def api_profile() -> Dict:
    mock_path = pathlib.Path(__file__).parent / 'mocks' / 'profile.json'
    return json.loads(mock_path.read_text())
