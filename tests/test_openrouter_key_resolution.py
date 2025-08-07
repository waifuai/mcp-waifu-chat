from importlib import reload
from pathlib import Path

import pytest

import mcp_waifu_chat.ai as ai


@pytest.fixture(autouse=True)
def reset_ai_and_env(monkeypatch: pytest.MonkeyPatch):
    # Clear env and reload module to reset caches before each test
    for k in ["OPENROUTER_API_KEY"]:
        monkeypatch.delenv(k, raising=False)
    reload(ai)
    yield


def test_openrouter_key_from_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "env-key")
    reload(ai)  # ensure module picks env after cache reset
    key = ai._resolve_openrouter_api_key()  # type: ignore[attr-defined]
    assert key == "env-key"


def test_openrouter_key_from_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    fake_home = tmp_path
    (fake_home / ".api-openrouter").write_text("file-key", encoding="utf-8")
    # Point home resolution to our temp directory for Path.home()
    monkeypatch.setenv("HOME", str(fake_home))
    # On Windows, Path.home() may use USERPROFILE
    monkeypatch.setenv("USERPROFILE", str(fake_home))
    reload(ai)
    key = ai._resolve_openrouter_api_key()  # type: ignore[attr-defined]
    assert key == "file-key"