from ipaddress import IPv4Address, IPv4Interface, IPv4Network, IPv6Address, IPv6Interface, IPv6Network
from typing import overload


@overload
def get_network_offset(parent: IPv4Network, child: IPv4Network) -> int: ...


@overload
def get_network_offset(parent: IPv6Network, child: IPv6Network) -> int: ...


def get_network_offset(parent: IPv4Network | IPv6Network, child: IPv4Network | IPv6Network) -> int:
    if not child.subnet_of(parent):  # pyright: ignore[reportArgumentType]
        raise ValueError("Child network must be a subnet of the parent network")
    return (int(child.network_address) - int(parent.network_address)) >> (parent.max_prefixlen - child.prefixlen)


@overload
def get_offset_network(parent: IPv4Network, offset: int, prefixlen: int) -> IPv4Network: ...


@overload
def get_offset_network(parent: IPv6Network, offset: int, prefixlen: int) -> IPv6Network: ...


@overload
def get_offset_network(parent: IPv4Network | IPv6Network, offset: int, prefixlen: int) -> IPv4Network | IPv6Network: ...


def get_offset_network(parent: IPv4Network | IPv6Network, offset: int, prefixlen: int) -> IPv4Network | IPv6Network:
    if prefixlen < parent.prefixlen or prefixlen > parent.max_prefixlen:
        raise ValueError("Prefix length must be within the range of the parent network")

    if offset < 0 or (1 << (prefixlen - parent.prefixlen)) <= offset:
        raise ValueError("Offset must be within the range of the parent network")

    network_address = int(parent.network_address) + (offset << (parent.max_prefixlen - prefixlen))
    network_tuple = (network_address, prefixlen)

    return IPv4Network(network_tuple) if parent.version == 4 else IPv6Network(network_tuple)


@overload
def get_address_offset(parent: IPv4Network, child: IPv4Address) -> int: ...


@overload
def get_address_offset(parent: IPv6Network, child: IPv6Address) -> int: ...


def get_address_offset(parent: IPv4Network | IPv6Network, child: IPv4Address | IPv6Address) -> int:
    if child not in parent:  # pyright: ignore[reportArgumentType]
        raise ValueError("Child address must be in the parent network")

    return int(child) - int(parent.network_address)


@overload
def get_offset_address(parent: IPv4Network, offset: int) -> IPv4Address: ...


@overload
def get_offset_address(parent: IPv6Network, offset: int) -> IPv6Address: ...


def get_offset_address(parent: IPv4Network | IPv6Network, offset: int) -> IPv4Address | IPv6Address:
    if offset < 0 or parent.num_addresses <= offset:
        raise ValueError("Offset must be within the range of the parent network")

    addr_int = int(parent.network_address) + offset

    return IPv4Address(addr_int) if parent.version == 4 else IPv6Address(addr_int)


@overload
def get_interface(network: IPv6Network, offset: IPv6Address | int) -> IPv6Interface: ...


@overload
def get_interface(network: IPv4Network, offset: IPv4Address | int) -> IPv4Interface: ...


def get_interface(
    network: IPv4Network | IPv6Network, offset: IPv4Address | IPv6Address | int
) -> IPv4Interface | IPv6Interface:
    address = get_offset_address(network, offset) if isinstance(offset, int) else offset

    if address not in network:
        raise ValueError("Offset address must be in the parent network")

    prefixlen = network.prefixlen

    iface_tuple = (address, prefixlen)

    return IPv4Interface(iface_tuple) if network.version == 4 else IPv6Interface(iface_tuple)


@overload
def get_loopback(address: IPv4Address) -> IPv4Interface: ...


@overload
def get_loopback(address: IPv6Address) -> IPv6Interface: ...


@overload
def get_loopback(address: IPv4Address | IPv6Address) -> IPv4Interface | IPv6Interface: ...


def get_loopback(address: IPv4Address | IPv6Address) -> IPv4Interface | IPv6Interface:
    iface_tuple = (address, address.max_prefixlen)
    return IPv4Interface(iface_tuple) if address.version == 4 else IPv6Interface(iface_tuple)
