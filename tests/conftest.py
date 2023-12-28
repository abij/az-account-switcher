import os
import shutil

import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def azure_profile_dir(tmpdir):
    """
    Create a temp directory per test.
    Each dir has a '.azure'-folder with a fresh copy of the 'test-azureProfile.json'
    This dir is configured in the environment for the azure-cli.
    The tmpdir is automatically cleaned up.
    """
    tmp_profile_dir = tmpdir.mkdir(".azure")
    os.environ["AZURE_CONFIG_DIR"] = str(tmp_profile_dir)

    cwd = Path.cwd()

    # Huu? are we not running inside the project folder?
    if cwd.name == "az-account-switcher":
        cwd = cwd / "tests"

    source = cwd / ".azure/test-azureProfile.json"
    destination = tmp_profile_dir / "azureProfile.json"

    shutil.copy(source, destination)
