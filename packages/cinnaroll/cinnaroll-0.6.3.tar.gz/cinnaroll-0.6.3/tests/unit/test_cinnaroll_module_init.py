import os
from unittest.mock import MagicMock

import pytest
from unittest import mock

import requests

import cinnaroll_internal.environment_check


@mock.patch("cinnaroll_internal.environment_check.requests.get")
@mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": ""})
@mock.patch.dict(os.environ, {"CINNAROLL_SKIP_VERSION_CHECK": "True"})
def test_module_import_without_api_key(mock_get: MagicMock) -> None:
    cinnaroll_internal.environment_check.find_disallowed_write_error = MagicMock(return_value=None)

    with mock.patch("builtins.open", mock.mock_open()):
        with pytest.raises(
            cinnaroll_internal.environment_check.CinnarollEnvironmentConfigurationError
        ):
            mock_get.return_value.status_code = requests.status_codes.codes.ok
            import cinnaroll


@mock.patch("cinnaroll_internal.environment_check.requests.get")
@mock.patch.dict(os.environ, {"CINNAROLL_API_KEY": "abc123"})
@mock.patch.dict(os.environ, {"CINNAROLL_SKIP_VERSION_CHECK": "True"})
def test_module_import_with_api_key_in_env(mock_get: MagicMock) -> None:
    cinnaroll_internal.environment_check.find_disallowed_write_error = MagicMock(return_value=None)
    with mock.patch("builtins.open", mock.mock_open()):
        mock_get.return_value.status_code = requests.status_codes.codes.ok
        import cinnaroll
