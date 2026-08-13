from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any, Self

if TYPE_CHECKING:
    from pydantic import GetCoreSchemaHandler
    from pydantic_core import CoreSchema
else:
    type GetCoreSchemaHandler = object
    type CoreSchema = object

# region Exceptions


class InvalidMacAddressError(ValueError):
    def __init__(self, mac: str | bytes, reason: str) -> None:
        super().__init__(f"Invalid MAC address: {mac!r} ({reason})")


# endregion Exceptions

# region Validating

MAC_CLEANUP_TRANSLATION = str.maketrans(
    {
        ":": "",
        "-": "",
        "_": "",
        "#": "",
        ".": "",
    }
)


def validate_mac(value: str | bytes) -> bytes:
    if isinstance(value, str):
        try:
            value = bytes.fromhex(value.translate(MAC_CLEANUP_TRANSLATION))
        except ValueError as e:
            raise InvalidMacAddressError(value, "MAC address must be a valid hex string") from e

    if len(value) != 6:
        raise InvalidMacAddressError(value, "MAC address must be 6 bytes long")

    return value


# endregion Validating

# region Formatting


class MacFormat(enum.StrEnum):
    COLON_U = "U:"
    DASH_U = "U-"
    DOT_U = "U."
    POUND_U = "U#"
    COLON = ":"
    DASH = "-"
    DOT = "."
    POUND = "#"

    def serialize(self, value: MacAddress) -> str:
        match self:
            case MacFormat.DASH:
                # Example: 00-1a-2b-3c-4d-5e
                return "-".join(f"{b:02x}" for b in value)
            case MacFormat.DOT:
                # Example: 001a.2b3c.4d5e
                return ".".join(f"{value[i]:02x}{value[i + 1]:02x}" for i in range(0, len(value), 2))
            case MacFormat.COLON:
                # Example: 00:1a:2b:3c:4d:5e
                return ":".join(f"{b:02x}" for b in value)
            case MacFormat.POUND:
                # Example: 00#1a#2b#3c#4d#5e
                return "#".join(f"{b:02x}" for b in value)
            case MacFormat.DASH_U:
                # Example: 00-1A-2B-3C-4D-5E
                return "-".join(f"{b:02X}" for b in value)
            case MacFormat.DOT_U:
                # Example: 001A.2B3C.4D5E
                return ".".join(f"{value[i]:02X}{value[i + 1]:02X}" for i in range(0, len(value), 2))
            case MacFormat.COLON_U:
                # Example: 00:1A:2B:3C:4D:5E
                return ":".join(f"{b:02X}" for b in value)
            case MacFormat.POUND_U:
                # Example: 00#1A#2B#3C#4D#5E
                return "#".join(f"{b:02X}" for b in value)

    def __get_pydantic_core_schema__(
        self,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return get_pydantic_core_schema(self, _source_type, _handler)


DEFAULT_MAC_FORMAT = MacFormat.COLON

# endregion Formatting


class MacAddress(bytes):
    __slots__ = ()

    def __new__(cls, value: bytes | str) -> Self:
        value = validate_mac(value)
        return super().__new__(cls, value)

    def __format__(self, format_spec: str) -> str:
        format_type = DEFAULT_MAC_FORMAT
        for _format in MacFormat:
            if _format.value in format_spec:
                format_type = _format
                break

        line = format_type.serialize(self)

        if "r" in format_spec:
            line = f"{self.__class__.__name__}({line!r})"

        return line

    def __repr__(self) -> str:
        return self.__format__("r")

    def __str__(self) -> str:
        return self.__format__("")

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source_type: Any,
        _handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        return get_pydantic_core_schema(DEFAULT_MAC_FORMAT, _source_type, _handler)


# region Pydantic Core Schema


def get_pydantic_core_schema(
    format_type: MacFormat,
    _source_type: Any,
    _handler: GetCoreSchemaHandler,
) -> CoreSchema:
    try:
        from pydantic_core import core_schema
    except ImportError as e:
        raise RuntimeError(
            "pydantic_core is required for using MacFormat with Pydantic please install net-misc[pydantic]"
        ) from e

    str_schema = _handler(str)

    plain_schema = core_schema.no_info_plain_validator_function(
        MacAddress,
    )
    json_schema = core_schema.chain_schema(
        steps=[
            str_schema,
            plain_schema,
        ]
    )
    return core_schema.json_or_python_schema(
        json_schema=json_schema,
        python_schema=core_schema.union_schema(
            choices=[
                core_schema.is_instance_schema(_source_type),
                json_schema,
            ]
        ),
        serialization=core_schema.plain_serializer_function_ser_schema(
            format_type.serialize,
            return_schema=str_schema,
            when_used="json-unless-none",
        ),
    )


# endregion Pydantic Core Schema
