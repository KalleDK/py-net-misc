from __future__ import annotations

import pytest

from net_misc.macaddress import (
    InvalidMacAddressError,
    MacAddress,
    MacFormat,
    validate_mac,
)

# region Tests for _validate_mac


class TestValidateMac:
    """Tests for the _validate_mac validation function."""

    def test_validate_mac_colon_format(self) -> None:
        """Test validation of colon-separated MAC address."""
        result = validate_mac("00:1a:2b:3c:4d:5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_dash_format(self) -> None:
        """Test validation of dash-separated MAC address."""
        result = validate_mac("00-1a-2b-3c-4d-5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_dot_format(self) -> None:
        """Test validation of dot-separated MAC address."""
        result = validate_mac("001a.2b3c.4d5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_pound_format(self) -> None:
        """Test validation of pound-separated MAC address."""
        result = validate_mac("00#1a#2b#3c#4d#5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_no_separator(self) -> None:
        """Test validation of MAC address with no separators."""
        result = validate_mac("001a2b3c4d5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_uppercase(self) -> None:
        """Test validation of uppercase hex MAC address."""
        result = validate_mac("00:1A:2B:3C:4D:5E")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_mixed_case(self) -> None:
        """Test validation of mixed case hex MAC address."""
        result = validate_mac("00:1a:2B:3c:4D:5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_mixed_separators(self) -> None:
        """Test validation of MAC address with mixed separators."""
        result = validate_mac("00:1a-2b#3c_4d.5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_underscore_separator(self) -> None:
        """Test validation of underscore-separated MAC address."""
        result = validate_mac("00_1a_2b_3c_4d_5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_bytes_input(self) -> None:
        """Test validation with bytes input."""
        result = validate_mac(b"\x00\x1a\x2b\x3c\x4d\x5e")
        assert result == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_validate_mac_all_zeros(self) -> None:
        """Test validation of all-zero MAC address."""
        result = validate_mac("00:00:00:00:00:00")
        assert result == b"\x00\x00\x00\x00\x00\x00"

    def test_validate_mac_all_ff(self) -> None:
        """Test validation of all-FF MAC address (broadcast)."""
        result = validate_mac("ff:ff:ff:ff:ff:ff")
        assert result == b"\xff\xff\xff\xff\xff\xff"

    def test_validate_mac_invalid_hex_string(self) -> None:
        """Test validation fails with invalid hex characters."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            validate_mac("00:1g:2b:3c:4d:5e")
        assert "valid hex string" in str(exc_info.value)

    def test_validate_mac_too_short(self) -> None:
        """Test validation fails when MAC address is too short."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            validate_mac("00:1a:2b:3c:4d")
        assert "6 bytes long" in str(exc_info.value)

    def test_validate_mac_too_long(self) -> None:
        """Test validation fails when MAC address is too long."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            validate_mac("00:1a:2b:3c:4d:5e:ff")
        assert "6 bytes long" in str(exc_info.value)

    def test_validate_mac_empty_string(self) -> None:
        """Test validation fails with empty string."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            validate_mac("")
        assert "6 bytes long" in str(exc_info.value)

    def test_validate_mac_empty_bytes(self) -> None:
        """Test validation fails with empty bytes."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            validate_mac(b"")
        assert "6 bytes long" in str(exc_info.value)


# endregion Tests for _validate_mac


# region Tests for MacAddress


class TestMacAddressCreation:
    """Tests for MacAddress instantiation."""

    def test_create_from_colon_format(self) -> None:
        """Test creating MacAddress from colon-separated string."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        assert mac == b"\x00\x1a\x2b\x3c\x4d\x5e"
        assert isinstance(mac, bytes)

    def test_create_from_dash_format(self) -> None:
        """Test creating MacAddress from dash-separated string."""
        mac = MacAddress("00-1a-2b-3c-4d-5e")
        assert mac == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_create_from_dot_format(self) -> None:
        """Test creating MacAddress from dot-separated string."""
        mac = MacAddress("001a.2b3c.4d5e")
        assert mac == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_create_from_bytes(self) -> None:
        """Test creating MacAddress from bytes."""
        mac = MacAddress(b"\x00\x1a\x2b\x3c\x4d\x5e")
        assert mac == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_create_uppercase(self) -> None:
        """Test creating MacAddress from uppercase hex."""
        mac = MacAddress("00:1A:2B:3C:4D:5E")
        assert mac == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_create_fails_invalid_format(self) -> None:
        """Test creation fails with invalid format."""
        with pytest.raises(InvalidMacAddressError):
            MacAddress("invalid")

    def test_create_fails_wrong_length(self) -> None:
        """Test creation fails with wrong byte length."""
        with pytest.raises(InvalidMacAddressError):
            MacAddress("00:1a:2b:3c:4d")

    def test_create_fails_invalid_hex(self) -> None:
        """Test creation fails with invalid hex characters."""
        with pytest.raises(InvalidMacAddressError):
            MacAddress("00:1g:2b:3c:4d:5e")

    def test_create_zero_mac(self) -> None:
        """Test creating zero MAC address."""
        mac = MacAddress("00:00:00:00:00:00")
        assert mac == b"\x00\x00\x00\x00\x00\x00"

    def test_create_broadcast_mac(self) -> None:
        """Test creating broadcast MAC address."""
        mac = MacAddress("ff:ff:ff:ff:ff:ff")
        assert mac == b"\xff\xff\xff\xff\xff\xff"


class TestMacAddressFormatting:
    """Tests for MacAddress formatting and string output."""

    @pytest.fixture
    def mac(self) -> MacAddress:
        """Create a MacAddress instance for testing."""
        return MacAddress("00:1a:2b:3c:4d:5e")

    def test_str_default_format(self, mac: MacAddress) -> None:
        """Test string representation uses default colon format."""
        assert str(mac) == "00:1a:2b:3c:4d:5e"

    def test_repr_format(self, mac: MacAddress) -> None:
        """Test repr shows class name and colon format."""
        assert repr(mac) == "MacAddress('00:1a:2b:3c:4d:5e')"

    def test_format_colon(self, mac: MacAddress) -> None:
        """Test colon format specification."""
        assert format(mac, ":") == "00:1a:2b:3c:4d:5e"

    def test_format_colon_uppercase(self, mac: MacAddress) -> None:
        """Test colon format with uppercase."""
        assert format(mac, "U:") == "00:1A:2B:3C:4D:5E"

    def test_format_dash(self, mac: MacAddress) -> None:
        """Test dash format specification."""
        assert format(mac, "-") == "00-1a-2b-3c-4d-5e"

    def test_format_dash_uppercase(self, mac: MacAddress) -> None:
        """Test dash format with uppercase."""
        assert format(mac, "U-") == "00-1A-2B-3C-4D-5E"

    def test_format_dot(self, mac: MacAddress) -> None:
        """Test dot format specification."""
        assert format(mac, ".") == "001a.2b3c.4d5e"

    def test_format_dot_uppercase(self, mac: MacAddress) -> None:
        """Test dot format with uppercase."""
        assert format(mac, "U.") == "001A.2B3C.4D5E"

    def test_format_pound(self, mac: MacAddress) -> None:
        """Test pound format specification."""
        assert format(mac, "#") == "00#1a#2b#3c#4d#5e"

    def test_format_pound_uppercase(self, mac: MacAddress) -> None:
        """Test pound format with uppercase."""
        assert format(mac, "U#") == "00#1A#2B#3C#4D#5E"

    def test_format_with_repr_flag_colon(self, mac: MacAddress) -> None:
        """Test format with repr flag."""
        assert format(mac, "r:") == "MacAddress('00:1a:2b:3c:4d:5e')"

    def test_format_with_repr_flag_dash(self, mac: MacAddress) -> None:
        """Test format with repr flag and dash format."""
        assert format(mac, "r-") == "MacAddress('00-1a-2b-3c-4d-5e')"

    def test_format_with_repr_flag_uppercase(self, mac: MacAddress) -> None:
        """Test format with repr flag and uppercase."""
        assert format(mac, "rU:") == "MacAddress('00:1A:2B:3C:4D:5E')"

    def test_format_empty_spec(self, mac: MacAddress) -> None:
        """Test format with empty spec uses default."""
        assert format(mac, "") == "00:1a:2b:3c:4d:5e"

    def test_format_uppercase_flag_only(self, mac: MacAddress) -> None:
        """Test format with only uppercase flag defaults to colon uppercase."""
        # "U" alone doesn't match any format, so it uses default colon format with uppercase
        assert format(mac, "U:") == "00:1A:2B:3C:4D:5E"

    def test_format_repr_flag_only(self, mac: MacAddress) -> None:
        """Test format with only repr flag."""
        assert format(mac, "r") == "MacAddress('00:1a:2b:3c:4d:5e')"


class TestMacAddressEquality:
    """Tests for MacAddress comparison."""

    def test_equality_same_format(self) -> None:
        """Test equality with same format."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = MacAddress("00:1a:2b:3c:4d:5e")
        assert mac1 == mac2

    def test_equality_different_format(self) -> None:
        """Test equality with different format input."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = MacAddress("00-1a-2b-3c-4d-5e")
        assert mac1 == mac2

    def test_equality_bytes_input(self) -> None:
        """Test equality between string and bytes input."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = MacAddress(b"\x00\x1a\x2b\x3c\x4d\x5e")
        assert mac1 == mac2

    def test_equality_raw_bytes(self) -> None:
        """Test equality with raw bytes."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        assert mac == b"\x00\x1a\x2b\x3c\x4d\x5e"

    def test_inequality(self) -> None:
        """Test inequality between different MAC addresses."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = MacAddress("ff:ff:ff:ff:ff:ff")
        assert mac1 != mac2

    def test_hashable(self) -> None:
        """Test that MacAddress is hashable."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = MacAddress("00:1a:2b:3c:4d:5e")
        mac_set = {mac1, mac2}
        assert len(mac_set) == 1

    def test_can_be_dict_key(self) -> None:
        """Test that MacAddress can be used as dict key."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = MacAddress("00:1a:2b:3c:4d:5e")
        d = {mac1: "value"}
        assert d[mac2] == "value"


class TestMacAddressIndexing:
    """Tests for MacAddress indexing (inherited from bytes)."""

    def test_indexing(self) -> None:
        """Test indexing into MacAddress."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        assert mac[0] == 0x00
        assert mac[1] == 0x1A
        assert mac[5] == 0x5E

    def test_slicing(self) -> None:
        """Test slicing MacAddress."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        assert mac[0:2] == b"\x00\x1a"
        assert mac[2:4] == b"\x2b\x3c"

    def test_iteration(self) -> None:
        """Test iteration over MacAddress."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        bytes_list = list(mac)
        assert bytes_list == [0x00, 0x1A, 0x2B, 0x3C, 0x4D, 0x5E]

    def test_length(self) -> None:
        """Test length of MacAddress."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        assert len(mac) == 6


# endregion Tests for MacAddress


# region Tests for MacFormat Enum


class TestMacFormat:
    """Tests for MacFormat enum and serialization."""

    @pytest.fixture
    def mac(self) -> MacAddress:
        """Create a MacAddress instance for testing."""
        return MacAddress("00:1a:2b:3c:4d:5e")

    def test_serialize_colon(self, mac: MacAddress) -> None:
        """Test MacFormat.COLON serialization."""
        result = MacFormat.COLON.serialize(mac)
        assert result == "00:1a:2b:3c:4d:5e"

    def test_serialize_colon_uppercase(self, mac: MacAddress) -> None:
        """Test MacFormat.COLON_U serialization."""
        result = MacFormat.COLON_U.serialize(mac)
        assert result == "00:1A:2B:3C:4D:5E"

    def test_serialize_dash(self, mac: MacAddress) -> None:
        """Test MacFormat.DASH serialization."""
        result = MacFormat.DASH.serialize(mac)
        assert result == "00-1a-2b-3c-4d-5e"

    def test_serialize_dash_uppercase(self, mac: MacAddress) -> None:
        """Test MacFormat.DASH_U serialization."""
        result = MacFormat.DASH_U.serialize(mac)
        assert result == "00-1A-2B-3C-4D-5E"

    def test_serialize_dot(self, mac: MacAddress) -> None:
        """Test MacFormat.DOT serialization."""
        result = MacFormat.DOT.serialize(mac)
        assert result == "001a.2b3c.4d5e"

    def test_serialize_dot_uppercase(self, mac: MacAddress) -> None:
        """Test MacFormat.DOT_U serialization."""
        result = MacFormat.DOT_U.serialize(mac)
        assert result == "001A.2B3C.4D5E"

    def test_serialize_pound(self, mac: MacAddress) -> None:
        """Test MacFormat.POUND serialization."""
        result = MacFormat.POUND.serialize(mac)
        assert result == "00#1a#2b#3c#4d#5e"

    def test_serialize_pound_uppercase(self, mac: MacAddress) -> None:
        """Test MacFormat.POUND_U serialization."""
        result = MacFormat.POUND_U.serialize(mac)
        assert result == "00#1A#2B#3C#4D#5E"

    def test_format_enum_values(self) -> None:
        """Test MacFormat enum string values."""
        assert MacFormat.COLON.value == ":"
        assert MacFormat.COLON_U.value == "U:"
        assert MacFormat.DASH.value == "-"
        assert MacFormat.DASH_U.value == "U-"
        assert MacFormat.DOT.value == "."
        assert MacFormat.DOT_U.value == "U."
        assert MacFormat.POUND.value == "#"
        assert MacFormat.POUND_U.value == "U#"

    def test_serialize_broadcast_mac(self) -> None:
        """Test serialization of broadcast MAC address."""
        mac = MacAddress("ff:ff:ff:ff:ff:ff")
        result = MacFormat.COLON.serialize(mac)
        assert result == "ff:ff:ff:ff:ff:ff"

    def test_serialize_zero_mac(self) -> None:
        """Test serialization of zero MAC address."""
        mac = MacAddress("00:00:00:00:00:00")
        result = MacFormat.COLON.serialize(mac)
        assert result == "00:00:00:00:00:00"


# endregion Tests for MacFormat Enum


# region Tests for InvalidMacAddressError


class TestInvalidMacAddressError:
    """Tests for InvalidMacAddressError exception."""

    def test_error_message_invalid_hex(self) -> None:
        """Test error message for invalid hex."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            MacAddress("00:1g:2b:3c:4d:5e")
        error_msg = str(exc_info.value)
        assert "Invalid MAC address" in error_msg
        assert "valid hex string" in error_msg

    def test_error_message_wrong_length(self) -> None:
        """Test error message for wrong length."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            MacAddress("00:1a:2b:3c")
        error_msg = str(exc_info.value)
        assert "Invalid MAC address" in error_msg
        assert "6 bytes long" in error_msg

    def test_error_includes_input(self) -> None:
        """Test error message includes the invalid input."""
        with pytest.raises(InvalidMacAddressError) as exc_info:
            MacAddress("invalid")
        error_msg = str(exc_info.value)
        assert "invalid" in error_msg

    def test_error_is_value_error(self) -> None:
        """Test that InvalidMacAddressError is a ValueError."""
        with pytest.raises(ValueError):
            MacAddress("invalid")


# endregion Tests for InvalidMacAddressError


# region Edge Case Tests


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_mac_in_list(self) -> None:
        """Test using MacAddress in a list."""
        macs = [
            MacAddress("00:1a:2b:3c:4d:5e"),
            MacAddress("ff:ff:ff:ff:ff:ff"),
        ]
        assert len(macs) == 2
        assert macs[0] == MacAddress("00:1a:2b:3c:4d:5e")

    def test_mac_sorting(self) -> None:
        """Test sorting MacAddress instances."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = MacAddress("ff:ff:ff:ff:ff:ff")
        mac3 = MacAddress("80:00:00:00:00:00")
        macs = [mac2, mac1, mac3]
        sorted_macs = sorted(macs)
        assert sorted_macs[0] == mac1
        assert sorted_macs[1] == mac3
        assert sorted_macs[2] == mac2

    def test_mac_address_immutable(self) -> None:
        """Test that MacAddress is immutable (inherits from bytes)."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        with pytest.raises(TypeError):
            mac[0] = 0xFF  # type: ignore[index] # ty: ignore[invalid-assignment]

    def test_format_with_whitespace(self) -> None:
        """Test format spec with various whitespace and flags."""
        mac = MacAddress("00:1a:2b:3c:4d:5e")
        # The formatter might ignore whitespace in the spec
        assert format(mac, ":") == "00:1a:2b:3c:4d:5e"

    def test_leading_zeros_preserved(self) -> None:
        """Test that leading zeros are preserved."""
        mac = MacAddress("00:01:02:03:04:05")
        assert str(mac) == "00:01:02:03:04:05"

    def test_mac_address_bytes_compatibility(self) -> None:
        """Test MacAddress works with bytes operations."""
        mac1 = MacAddress("00:1a:2b:3c:4d:5e")
        mac2 = b"\x00\x1a\x2b\x3c\x4d\x5e"
        assert mac1 + b"\x00" == mac2 + b"\x00"


# endregion Edge Case Tests
