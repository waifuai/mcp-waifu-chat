import os
from pathlib import Path

import pytest

from mcp_waifu_chat.config import Config


def _write(path: Path, content: str):
    path.write_text(content, encoding="utf-8")


@pytest.fixture(autouse=True)
def clear_env(monkeypatch: pytest.MonkeyPatch):
    # Clear relevant env vars between tests
    for k in [
        "DEFAULT_PROVIDER",
        "OPENROUTER_MODEL_NAME",
        "GEMINI_MODEL_NAME",
        "OPENROUTER_API_KEY",
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
    ]:
        monkeypatch.delenv(k, raising=False)
    yield


def test_default_provider_is_openrouter():
    cfg = Config.load()
    assert cfg.default_provider == "openrouter"


def test_env_overrides_default_provider(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DEFAULT_PROVIDER", "gemini")
    cfg = Config.load()
    assert cfg.default_provider == "gemini"


def test_openrouter_model_env_overrides(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("OPENROUTER_MODEL_NAME", "openrouter/horizon-beta-override")
    cfg = Config.load()
    assert cfg.openrouter_model_name == "openrouter/horizon-beta-override"


def test_openrouter_model_dotfile_used_when_env_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    fake_home = tmp_path
    _write(fake_home / ".model-openrouter", "openrouter/horizon-beta-file")
    monkeypatch.setenv("HOME", str(fake_home))
    # On Windows, Path.home() may use USERPROFILE
    monkeypatch.setenv("USERPROFILE", str(fake_home))
    cfg = Config.load()
    assert cfg.openrouter_model_name == "openrouter/horizon-beta-file"


def test_openrouter_model_default_when_no_env_or_file(monkeypatch: pytest.MonkeyPatch):
    cfg = Config.load()
    assert cfg.openrouter_model_name == "openrouter/horizon-beta"


def test_gemini_model_env_overrides(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("GEMINI_MODEL_NAME", "gemini-2.5-flash")
    cfg = Config.load()
    assert cfg.gemini_model_name == "gemini-2.5-flash"


def test_gemini_model_dotfile_used_when_env_missing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    fake_home = tmp_path
    _write(fake_home / ".model-gemini", "gemini-2.5-ultra")
    monkeypatch.setenv("HOME", str(fake_home))
    monkeypatch.setenv("USERPROFILE", str(fake_home))
    cfg = Config.load()
    assert cfg.gemini_model_name == "gemini-2.5-ultra"