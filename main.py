import asyncio
import logging
import logging.handlers
import queue
from bleak import BleakScanner
from bc_data import Bc300AdvertisingData

DEVICE1 = 'F8:F0:05:9D:1F:4D'  # this is the 'naked' unit
DEVICE2 = 'F8:F0:05:FE:47:EF'  # this is the unit in enclosure

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def main():
    stop_event = asyncio.Event()

    def callback(device, advertising_data):
        if device.address == DEVICE1 or device.address == DEVICE2:
            print(f'{device} - {advertising_data}')
            bc300_data = Bc300AdvertisingData.from_bytes(
                advertising_data.service_data['0000fe0e-0000-1000-8000-00805f9b34fb']
            )

    async with BleakScanner(callback) as scanner:
        await stop_event.wait()

if __name__ == '__main__':

    log_queue = queue.Queue()
    queue_handler = logging.handlers.QueueHandler(log_queue)

    root = logging.getLogger()
    root.addHandler(queue_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)')
    )

    queue_listener = logging.handlers.QueueListener(
        log_queue,
        console_handler,
        respect_handler_level=True
    )

    queue_listener.start()

    logger.info('Starting main routine ...')

    asyncio.run(main())
