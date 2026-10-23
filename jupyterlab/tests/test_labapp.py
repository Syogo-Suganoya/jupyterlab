# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import pytest
from jupyter_server.serverapp import ServerApp

from jupyterlab.labapp import LabApp


@pytest.fixture
def broken_lab_config(jp_environ, jp_config_dir):
    (jp_config_dir / "jupyter_lab_config.py").write_text("c = get_config()\nnot valid python\n")


def test_launch_exits_on_config_file_error(broken_lab_config, monkeypatch):
    monkeypatch.setattr(LabApp, "_launched_as_app", False, raising=False)
    try:
        with pytest.raises(SystemExit) as exc_info:
            LabApp.initialize_server(argv=["--no-browser"])
    finally:
        ServerApp.clear_instance()
    assert exc_info.value.code == 1


def test_extension_ignores_config_file_error(broken_lab_config):
    app = LabApp()
    app.load_config_file()
    assert not app.raise_config_file_errors
