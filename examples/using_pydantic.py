from __future__ import annotations

from typing import Annotated

import pydantic

from net_misc import MacAddressBase, MacFormat


class Device(pydantic.BaseModel):
    mac_address: Annotated[MacAddressBase, MacFormat.DASH]
    mac_address_extra: MacAddressBase


def main():
    mac = MacAddressBase("00:1a:2b:3c:4d:5e")
    device = Device(mac_address=mac, mac_address_extra=mac)
    print(device.model_dump())
    print(device.model_dump(mode="json"))
    print(device.model_dump_json(indent=4))
    print(Device.model_validate_json(device.model_dump_json(indent=4)))


if __name__ == "__main__":
    main()
