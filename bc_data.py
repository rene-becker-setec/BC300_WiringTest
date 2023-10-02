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
                    '<BBBBB7sIB',
                    buffer=data, offset=1
                )
                return Introduction(
                    prod_id=prod_id, hw_ver=hw_ver, hw_rev=hw_rev, hw_mod=hw_mod, sw_ver=sw_ver,
                    ser_num=serial,
                    uptime=uptime, discovery=discovery
                )
            case 0x01:
                logger.debug('Battery Status')
                (voltage, current, charge, temp_shunt, temp_batt, uptime, _) = struct.unpack_from(
                    '<hiibbIb',
                    buffer=data, offset=1
                )
                return BatteryStatus(
                    voltage=voltage, current=current, charge=charge, temp_shunt=temp_shunt, temp_batt=temp_batt,
                    uptime=uptime
                )
            case 0x04:
                logger.debug('Battery Info')
                (time2go, est_capacity, soc, soh, _, v2soc, charge_rate, ch2soc_factor, delta_t_500ms,
                 i_avg_ma, i_pt1_16ma) = struct.unpack_from(
                    '<HHBBBBHHBHB',
                    buffer=data, offset=1
                )
                return BatteryInfo(
                    time2go=time2go, est_capacity=est_capacity, soc=soc, soh=soh,v2soc=v2soc, charge_rate=charge_rate,
                    ch2soc_factor=ch2soc_factor, delta_t_500ms=delta_t_500ms, i_avg_ma=i_avg_ma, i_pt1_16ma=i_pt1_16ma
                )


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
    def __init__(self, voltage, current, charge, temp_shunt, temp_batt, uptime):
        self.voltage = voltage
        self.current = current
        self.charge = charge
        self.temp_shunt = temp_shunt
        self.temp_batt = temp_batt
        self.uptime = uptime

    def __str__(self):
        return (f'Battery Status: Voltage: {self.voltage}, Current: {self.current}, Charge: {self.charge}, '
                f'Shunt Temperature: {self.temp_shunt}, Battery Temperature: {self.temp_batt}, Uptime: {self.uptime}')


class BatteryInfo(Bc300AdvertisingData):
    def __init__(self, time2go, est_capacity, soc, soh, v2soc, charge_rate, ch2soc_factor, delta_t_500ms,
                 i_avg_ma, i_pt1_16ma):
        self.time2go = time2go
        self.est_capacity = est_capacity
        self.soc = soc
        self.soh = soh
        self.v2soc = v2soc
        self.charge_rate = charge_rate
        self.ch2soc_factor = ch2soc_factor
        self.delta_t_500ms = delta_t_500ms
        self.i_avg_ma = i_avg_ma
        self.i_pt1_16ma = i_pt1_16ma

    def __str__(self):
        return (f'Battery Info: Time2Go: {self.time2go}, Estimated Capacity: {self.est_capacity},'
                f'State of Charge: {self.soc}, State of Health: {self.soh} , Voltage based SoC: {self.v2soc}, '
                f'Charge Rate: {self.charge_rate}, Ch2SoC Contribution Factor: {self.ch2soc_factor} '
                f'Time between samples: {self.delta_t_500ms}, '
                f'Average Peukert corrected discharge current: {self.i_avg_ma}, '
                f'PT1 filtered Peukert corrected discharcge current 16mA resolution: {self.i_pt1_16ma}')


if __name__ == '__main__':
    x = b'\x00\x01\x03\x01\x01\x99A123456\x00\x00\x00\x01\x00'
    print(f'Size: {len(x)}')
    y = Bc300AdvertisingData.from_bytes(x)
    print(y)

    x = b'\x01\x1f\x00\x00\x00\x00\x0a\x00\x00\x00\x0b\x12\x20\x00\x01\x02\x03\x00'
    y = Bc300AdvertisingData.from_bytes(x)
    print(y)

    x = b'\x04\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10'
    y = Bc300AdvertisingData.from_bytes(x)
    print(y)
    #     voltage  current  charge   t_shunt  t_batt uptime   flags (not used)
    # '01 2834     de150000 95250000 16       05     531a0000 00'
    x = b'\x01(4\xde\x15\x00\x00\x95%\x00\x00\x16\x05S\x1a\x00\x00\x00'
    y = Bc300AdvertisingData.from_bytes(x)
    print(y)
