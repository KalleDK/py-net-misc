from __future__ import annotations

from typing import Annotated

import pytest

try:
    from pydantic import TypeAdapter

    from net_misc.macaddress import MacAddress, MacFormat
except ImportError:
    pytest.skip("pydantic is not installed", allow_module_level=True)


@pytest.mark.parametrize("format_type", MacFormat)
def test_get_pydantic_core_schema_validates_mac_address_with_format(format_type: MacFormat) -> None:
    adapter: TypeAdapter[MacAddress] = TypeAdapter(Annotated[MacAddress, format_type])

    result = adapter.validate_python("00:1a:2b:3c:4d:5e")

    assert result == MacAddress("00:1a:2b:3c:4d:5e")
    assert isinstance(result, MacAddress)


@pytest.mark.parametrize("format_type", MacFormat)
def test_get_pydantic_core_schema_serializes_mac_address_with_format(format_type: MacFormat) -> None:
    adapter: TypeAdapter[MacAddress] = TypeAdapter(Annotated[MacAddress, format_type])
    mac = MacAddress("00:1a:2b:3c:4d:5e")
    expected = format_type.serialize(mac)

    assert adapter.dump_python(mac, mode="json") == expected
    assert adapter.dump_json(mac) == f'"{expected}"'.encode()


def test_get_pydantic_core_schema_validates_mac_address() -> None:
    adapter: TypeAdapter[MacAddress] = TypeAdapter(MacAddress)

    result = adapter.validate_python("00:1a:2b:3c:4d:5e")

    assert result == MacAddress("00:1a:2b:3c:4d:5e")
    assert isinstance(result, MacAddress)


def test_get_pydantic_core_schema_serializes_using_format() -> None:
    adapter: TypeAdapter[MacAddress] = TypeAdapter(MacAddress)
    mac = MacAddress("00:1a:2b:3c:4d:5e")

    assert adapter.dump_python(mac, mode="json") == "00:1a:2b:3c:4d:5e"
    assert adapter.dump_json(mac) == b'"00:1a:2b:3c:4d:5e"'
