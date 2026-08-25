from __future__ import annotations

import builtins
import importlib
from typing import Any

import pytest

import net_misc.macaddress as macaddress_module


def test_rich_fallbacks_raise_when_rich_is_not_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test Rich hooks explain that the optional dependency is required."""

    original_import = builtins.__import__

    def reject_rich(
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name in {"rich.text", "rich.measure"}:
            raise ImportError("rich unavailable")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", reject_rich)
    importlib.reload(macaddress_module)

    try:
        mac = macaddress_module.MacAddress("00:1a:2b:3c:4d:5e")

        with pytest.raises(NotImplementedError, match="rich is required"):
            list(mac.__rich_console__(None, None))  # pyright: ignore[reportArgumentType]

        with pytest.raises(NotImplementedError, match="rich is required"):
            mac.__rich_measure__(None, None)  # pyright: ignore[reportArgumentType]
    finally:
        monkeypatch.undo()
        importlib.reload(macaddress_module)
