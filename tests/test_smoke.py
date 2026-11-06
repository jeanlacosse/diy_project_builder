import importlib.metadata
import sys

import shedguide
from shedguide import cli


def test_T1_console_script_resolves_to_cli_run() -> None:
    assert sys.version_info >= (3, 13)
    assert shedguide.__doc__
    eps = importlib.metadata.entry_points(group="console_scripts")
    ep = next(e for e in eps if e.name == "shedguide")
    assert ep.value == "shedguide.cli:run"
    assert ep.load() is cli.run


def test_T22_network_guard_blocks_sockets() -> None:
    import socket

    import pytest

    with pytest.raises(RuntimeError, match="Network access"):
        socket.create_connection(("127.0.0.1", 9))
