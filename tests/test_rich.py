from __future__ import annotations

import builtins
import importlib
import importlib.util
from typing import Any

import pytest

import net_misc.macaddress as macaddress_module
from net_misc.macaddress import MacAddress


@pytest.mark.skipif(importlib.util.find_spec("rich") is None, reason="rich is not installed")
def test_rich_console_renders_mac_address() -> None:
    """Test Rich renders a MacAddress using its string representation."""
    from rich.console import Console
    from rich.text import Text

    mac = MacAddress("00:1a:2b:3c:4d:5e")
    rendered = list(mac.__rich_console__(Console(), Console().options))

    assert len(rendered) == 1
    assert isinstance(rendered[0], Text)
    assert rendered[0].plain == "00:1a:2b:3c:4d:5e"


@pytest.mark.skipif(importlib.util.find_spec("rich") is None, reason="rich is not installed")
def test_rich_measure_returns_mac_address_widths() -> None:
    """Test Rich receives the minimum and maximum MacAddress widths."""
    from rich.console import Console

    mac = MacAddress("00:1a:2b:3c:4d:5e")
    measurement = mac.__rich_measure__(Console(), Console().options)

    assert measurement.minimum == 12
    assert measurement.maximum == 17


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
