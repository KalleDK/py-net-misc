from net_misc import MacAddress, MacFormat


def main():
    mac = MacAddress("00:1a:2b:3c:4d:5e")
    print(f"Original MAC Address: {mac}")
    print(f"MAC Address in COLON format: {format(mac, MacFormat.COLON)}")
    print(f"MAC Address in DASH format: {format(mac, MacFormat.DASH)}")
    print(f"MAC Address in DOT format: {format(mac, MacFormat.DOT)}")
    print(f"MAC Address in POUND format: {format(mac, MacFormat.POUND)}")


if __name__ == "__main__":
    main()
