"""
Instead of using the 'az.cli' python package, which download complete Azure-CLI, assume 'az' is available on PATH.
"""
import json
import platform
import re
import subprocess  # nosec B404
from collections import namedtuple
from typing import List

AzCliResult = namedtuple("AzCliResult", ["exit_code", "result_dict", "logs"])


def az(command: str) -> AzCliResult:
    """
    Alternative to 'az.cli' to interact with Azure CLI. This implementation assumes 'az' is available on the Path.
    """
    cmd_list = _prepare_cmd_list(command)
    if platform.system() == "Windows":
        result = subprocess.run(cmd_list, capture_output=True, shell=True)  # noqa: S602 #nosec B602
        encoding = "ISO-8859-1"
    elif platform.system() in ("Linux", "Darwin"):
        result = subprocess.run(cmd_list, capture_output=True)  # noqa: S603 #nosec B603
        encoding = "utf-8"
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")

    return_code = result.returncode

    if return_code != 0:
        return AzCliResult(return_code, None, bytes.decode(result.stderr))

    # PATCH operation does not have result dict.
    if not result.stdout:
        return AzCliResult(return_code, None, None)

    data = bytes.decode(result.stdout, encoding=encoding)

    try:
        return AzCliResult(return_code, json.loads(data), None)
    except json.decoder.JSONDecodeError:
        # Not json? Not oke!
        return AzCliResult(1, None, data)


def _prepare_cmd_list(command: str) -> List[str]:
    """Flatten single-quoted literals into single line and split into list."""
    if not command.startswith("az "):
        command = "az " + command

    literals = re.findall(r"'((?:.|\n)+?)'", command)
    if not literals:
        return command.split()

    for _i, literal in enumerate(literals):
        command = command.replace(f"'{literal}'", f"${_i}", 1)

    parts = command.split()

    for _i, literal in enumerate(literals):
        for _j, part in enumerate(parts):
            if part == f"${_i}":
                parts[_j] = " ".join(literal.split())

    return parts
