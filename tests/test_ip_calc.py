from ipaddress import IPv4Address, IPv4Interface, IPv4Network, IPv6Address, IPv6Interface, IPv6Network

import pytest

from net_misc.ip_calc import (
    get_address_offset,
    get_interface,
    get_loopback,
    get_network_offset,
    get_offset_address,
    get_offset_network,
)


@pytest.mark.parametrize(
    ("parent", "child", "expected"),
    [
        (IPv4Network("192.0.2.0/24"), IPv4Network("192.0.2.128/25"), 1),
        (IPv6Network("2001:db8::/48"), IPv6Network("2001:db8:0:2::/64"), 2),
    ],
)
def test_get_network_offset(parent: IPv4Network | IPv6Network, child: IPv4Network | IPv6Network, expected: int) -> None:
    if isinstance(parent, IPv4Network):
        assert isinstance(child, IPv4Network)
        assert get_network_offset(parent, child) == expected
    else:
        assert isinstance(child, IPv6Network)
        assert get_network_offset(parent, child) == expected


@pytest.mark.parametrize(
    ("parent", "offset", "prefixlen", "expected"),
    [
        (IPv4Network("192.0.2.0/24"), 0, 26, IPv4Network("192.0.2.0/26")),
        (IPv4Network("192.0.2.0/24"), 3, 26, IPv4Network("192.0.2.192/26")),
        (IPv6Network("2001:db8::/48"), 2, 64, IPv6Network("2001:db8:0:2::/64")),
    ],
)
def test_get_offset_network(
    parent: IPv4Network | IPv6Network,
    offset: int,
    prefixlen: int,
    expected: IPv4Network | IPv6Network,
) -> None:
    assert get_offset_network(parent, offset, prefixlen) == expected


@pytest.mark.parametrize(
    ("parent", "child", "expected"),
    [
        (IPv4Network("192.0.2.0/24"), IPv4Address("192.0.2.37"), 37),
        (IPv6Network("2001:db8::/64"), IPv6Address("2001:db8::37"), 0x37),
    ],
)
def test_get_address_offset(parent: IPv4Network | IPv6Network, child: IPv4Address | IPv6Address, expected: int) -> None:
    if isinstance(parent, IPv4Network):
        assert isinstance(child, IPv4Address)
        assert get_address_offset(parent, child) == expected
    else:
        assert isinstance(child, IPv6Address)
        assert get_address_offset(parent, child) == expected


@pytest.mark.parametrize(
    ("parent", "offset", "expected"),
    [
        (IPv4Network("192.0.2.0/30"), 0, IPv4Address("192.0.2.0")),
        (IPv4Network("192.0.2.0/30"), 3, IPv4Address("192.0.2.3")),
        (IPv6Network("2001:db8::/126"), 3, IPv6Address("2001:db8::3")),
    ],
)
def test_get_offset_address(
    parent: IPv4Network | IPv6Network, offset: int, expected: IPv4Address | IPv6Address
) -> None:
    if isinstance(parent, IPv4Network):
        assert isinstance(expected, IPv4Address)
        assert get_offset_address(parent, offset) == expected
    else:
        assert isinstance(expected, IPv6Address)
        assert get_offset_address(parent, offset) == expected


@pytest.mark.parametrize(
    ("network", "offset", "expected"),
    [
        (IPv4Network("192.0.2.0/30"), 2, IPv4Interface("192.0.2.2/30")),
        (IPv4Network("192.0.2.0/30"), IPv4Address("192.0.2.1"), IPv4Interface("192.0.2.1/30")),
        (IPv6Network("2001:db8::/126"), 3, IPv6Interface("2001:db8::3/126")),
        (IPv6Network("2001:db8::/126"), IPv6Address("2001:db8::1"), IPv6Interface("2001:db8::1/126")),
    ],
)
def test_get_interface(
    network: IPv4Network | IPv6Network,
    offset: int | IPv4Address | IPv6Address,
    expected: IPv4Interface | IPv6Interface,
) -> None:
    if isinstance(network, IPv4Network):
        assert isinstance(offset, (int, IPv4Address))
        assert isinstance(expected, IPv4Interface)
        assert get_interface(network, offset) == expected
    else:
        assert isinstance(offset, (int, IPv6Address))
        assert isinstance(expected, IPv6Interface)
        assert get_interface(network, offset) == expected


@pytest.mark.parametrize(
    ("address", "expected"),
    [
        (IPv4Address("192.0.2.37"), IPv4Interface("192.0.2.37/32")),
        (IPv6Address("2001:db8::37"), IPv6Interface("2001:db8::37/128")),
    ],
)
def test_get_loopback(address: IPv4Address | IPv6Address, expected: IPv4Interface | IPv6Interface) -> None:
    if isinstance(address, IPv4Address):
        assert isinstance(expected, IPv4Interface)
        assert get_loopback(address) == expected
    else:
        assert isinstance(expected, IPv6Interface)
        assert get_loopback(address) == expected


@pytest.mark.parametrize(
    ("parent", "child"),
    [
        (IPv4Network("192.0.2.0/24"), IPv4Network("192.0.3.0/24")),
        (IPv6Network("2001:db8::/48"), IPv6Network("2001:db9::/48")),
    ],
)
def test_get_network_offset_rejects_non_subnet(
    parent: IPv4Network | IPv6Network, child: IPv4Network | IPv6Network
) -> None:
    if isinstance(parent, IPv4Network):
        assert isinstance(child, IPv4Network)
        with pytest.raises(ValueError, match="Child network must be a subnet"):
            get_network_offset(parent, child)
    else:
        assert isinstance(child, IPv6Network)
        with pytest.raises(ValueError, match="Child network must be a subnet"):
            get_network_offset(parent, child)


@pytest.mark.parametrize(
    ("parent", "prefixlen", "offset"),
    [
        (IPv4Network("192.0.2.0/24"), 23, 0),
        (IPv6Network("2001:db8::/64"), 63, 0),
        (IPv4Network("192.0.2.0/24"), 33, 0),
        (IPv6Network("2001:db8::/64"), 129, 0),
        (IPv4Network("192.0.2.0/24"), 26, -1),
        (IPv4Network("192.0.2.0/24"), 26, 4),
        (IPv6Network("2001:db8::/64"), 68, 16),
    ],
)
def test_get_offset_network_rejects_invalid_values(
    parent: IPv4Network | IPv6Network, prefixlen: int, offset: int
) -> None:
    with pytest.raises(ValueError):
        get_offset_network(parent, offset, prefixlen)


@pytest.mark.parametrize(
    ("parent", "child"),
    [
        (IPv4Network("192.0.2.0/24"), IPv4Address("192.0.3.1")),
        (IPv6Network("2001:db8::/64"), IPv6Address("2001:db9::1")),
    ],
)
def test_get_address_offset_rejects_address_outside_parent(
    parent: IPv4Network | IPv6Network, child: IPv4Address | IPv6Address
) -> None:
    if isinstance(parent, IPv4Network):
        assert isinstance(child, IPv4Address)
        with pytest.raises(ValueError, match="Child address must be in the parent"):
            get_address_offset(parent, child)
    else:
        assert isinstance(child, IPv6Address)
        with pytest.raises(ValueError, match="Child address must be in the parent"):
            get_address_offset(parent, child)


@pytest.mark.parametrize(
    ("parent", "offset"),
    [
        (IPv4Network("192.0.2.0/30"), -1),
        (IPv4Network("192.0.2.0/30"), 4),
        (IPv6Network("2001:db8::/126"), -1),
        (IPv6Network("2001:db8::/126"), 4),
    ],
)
def test_get_offset_address_rejects_invalid_offset(parent: IPv4Network | IPv6Network, offset: int) -> None:
    with pytest.raises(ValueError, match="Offset must be within the range"):
        get_offset_address(parent, offset)


@pytest.mark.parametrize(
    ("network", "offset"),
    [
        (IPv4Network("192.0.2.0/30"), -1),
        (IPv4Network("192.0.2.0/30"), 4),
        (IPv4Network("192.0.2.0/30"), IPv4Address("192.0.3.1")),
        (IPv6Network("2001:db8::/126"), 4),
        (IPv6Network("2001:db8::/126"), IPv6Address("2001:db9::1")),
    ],
)
def test_get_interface_rejects_invalid_offset(
    network: IPv4Network | IPv6Network, offset: int | IPv4Address | IPv6Address
) -> None:
    if isinstance(network, IPv4Network):
        assert isinstance(offset, (int, IPv4Address))
        with pytest.raises(ValueError):
            get_interface(network, offset)
    else:
        assert isinstance(offset, (int, IPv6Address))
        with pytest.raises(ValueError):
            get_interface(network, offset)
