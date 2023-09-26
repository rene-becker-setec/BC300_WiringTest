import asyncio
from bleak import BleakScanner

DEVICE1 = 'F8:F0:05:9D:1F:4D'
DEVICE2 = 'F8:F0:05:FE:47:EF'


async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        if device.address == DEVICE1:
            print(f'DEV#1: {device} - {advertising_data}')

        if device.address == DEVICE2:
            print(f'DEV#2: {device} - {advertising_data}')

    async with BleakScanner(callback) as scanner:
        await stop_event.wait()


asyncio.run(main())
