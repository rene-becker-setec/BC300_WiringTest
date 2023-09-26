import logging


logger = logging.getLogger(__name__)


class Bc300AdvertisingData:

    @classmethod
    def from_bytes(cls, data: bytes):
        match data[0]:
            case 0x00:
                logger.debug('Introduction')
            case 0x01:
                logger.debug('Battery Status')
            case 0x04:
                logger.debug('Battery Info')


class Introduction(Bc300AdvertisingData):
    def __init__(self):
        pass


class BatteryStatus(Bc300AdvertisingData):
    def __init__(self):
        pass


class BatteryInfo(Bc300AdvertisingData):
    def __init__(self):
        pass