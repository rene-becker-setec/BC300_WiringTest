import logging
import struct

logger = logging.getLogger(__name__)


class Bc300AdvertisingData:

    @classmethod
    def from_bytes(cls, data: bytes):
        match data[0]:
            case 0x00:
                logger.debug('Introduction')
                (prod_id, hw_ver, hw_rev, hw_mod, sw_ver,
                 serial, uptime, discovery) = struct.unpack_from(
                    '>BBBBB7sIB',
                    buffer=data, offset=1
                )
                return Introduction(
                    prod_id=prod_id, hw_ver=hw_ver, hw_rev=hw_rev, hw_mod=hw_mod, sw_ver=sw_ver,
                    ser_num=serial,
                    uptime=uptime, discovery=discovery
                )
            case 0x01:
                logger.debug('Battery Status')
            case 0x04:
                logger.debug('Battery Info')


class Introduction(Bc300AdvertisingData):
    def __init__(self, prod_id, hw_ver, hw_rev, hw_mod, sw_ver, ser_num, uptime, discovery):
        self.product_id = prod_id
        self.hw_version = hw_ver
        self.hw_revision = hw_rev
        self.hw_modification = hw_mod
        self.sw_version = sw_ver
        self.serial_num = ser_num
        self.uptime = uptime
        self.discovery = discovery

    def __str__(self) -> str:
        return (f'Introduction: Product ID: {self.product_id}, HW Version: {self.hw_version}, '
                f'HW Revision: {self.hw_revision}, HW Mod: {self.hw_modification}, SW Version: {self.sw_version}, '
                f'Serial: {self.serial_num}, Uptime: {self.uptime}, Discovery: {self.discovery}')


class BatteryStatus(Bc300AdvertisingData):
    def __init__(self):
        pass


class BatteryInfo(Bc300AdvertisingData):
    def __init__(self):
        pass


if __name__ == '__main__':
    x = b'\x00\x01\x03\x01\x01\x99A123456\x00\x00\x00\x01\x00'
    print(f'Size: {len(x)}')
    y = Bc300AdvertisingData.from_bytes(x)

    print(y)