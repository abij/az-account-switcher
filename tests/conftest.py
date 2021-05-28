import os
import shutil

import pytest
from pathlib import Path


@pytest.fixture(autouse=True)
def azure_profile_dir(tmpdir):
    tmp_profile_dir = tmpdir.mkdir(".azure")
    os.environ['AZURE_CONFIG_DIR'] = str(tmp_profile_dir)

    fresh_profile = Path.cwd() / '.azure/test-azureProfile.json'

    shutil.copy(fresh_profile, tmp_profile_dir / 'azureProfile.json')