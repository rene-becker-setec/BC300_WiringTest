import matplotlib.pyplot as plt
import datetime
import numpy as np
import re

LOG_FILE_NAME = '20231002_13.04.14.log'

batt_status_re = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2},\d{3})\s'
    r'\[\s+INFO\]\s(?:\w+:){6}\sBC300\s(?P<serial>A\d{10})\s-\sBattery\sStatus:'
    r'\sVoltage:\s(?P<voltage>\d+),\sCurrent:\s(?P<current>[-]?\d+),\sCharge:\s(?P<charge>[-]?\d+),'
    r'\sShunt\sTemperature:\s(?P<shunt_temp>[-]?\d+),\sBattery\sTemperature:\s(?P<battery_temp>[-]?\d+),'
    r'\sUptime:\s(?P<uptime>\d+)')

if __name__ == '__main__':

    dev1_timestamps = []
    dev1_currents = []
    dev2_timestamps = []
    dev2_currents = []

    with open(LOG_FILE_NAME, 'r') as logfile:
        for line in logfile:
            m = batt_status_re.match(line)
            if m:
                ts = datetime.datetime.fromisoformat(m['timestamp'])
                crnt = int(m['current'])
                if m['serial'] == 'A2232370046':
                    print(f'timestamp => {ts} - {crnt}')
                    dev1_timestamps.append(ts)
                    dev1_currents.append(crnt)
                else:
                    dev2_timestamps.append(ts)
                    dev2_currents.append(crnt)

    plt.plot(dev1_timestamps, dev1_currents, label='Device 1 (naked PCB)')
    plt.plot(dev2_timestamps, dev2_currents, label='Device 2 (in Enclosure)')

    plt.legend(loc="upper right")

    plt.show()

