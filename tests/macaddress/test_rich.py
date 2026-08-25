from __future__ import annotations

import pytest

from net_misc.macaddress import MacAddress

try:
    from rich.console import Console
    from rich.text import Text

except ImportError:
    pytest.skip("rich is not installed", allow_module_level=True)


def test_rich_console_renders_mac_address() -> None:
    """Test Rich renders a MacAddress using its string representation."""

    mac = MacAddress("00:1a:2b:3c:4d:5e")
    rendered = list(mac.__rich_console__(Console(), Console().options))

    assert len(rendered) == 1
    assert isinstance(rendered[0], Text)
    assert rendered[0].plain == "00:1a:2b:3c:4d:5e"


def test_rich_measure_returns_mac_address_widths() -> None:
    """Test Rich receives the minimum and maximum MacAddress widths."""

    mac = MacAddress("00:1a:2b:3c:4d:5e")
    measurement = mac.__rich_measure__(Console(), Console().options)

    assert measurement.minimum == 12
    assert measurement.maximum == 17
