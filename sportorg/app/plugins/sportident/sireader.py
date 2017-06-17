import threading
import time
import serial
from sportorg.lib.sportident import sireader


class SIReaderThread(threading.Thread):
    def __init__(self, port, func=lambda card_data: card_data):
        super().__init__()
        self.port = port
        self.func = func
        self.reading = True

    def run(self):
        si = sireader.SIReaderReadout(port=self.port)
        while True:
            try:
                while not si.poll_sicard():
                    time.sleep(0.5)
                    if not self.reading:
                        si.disconnect()
                        return
                # card_number = si.sicard
                # card_type = si.cardtype

                card_data = si.read_sicard()

                self.func(card_data)

                # beep
                si.ack_sicard()
            except sireader.SIReaderException as e:
                print(str(e))
            except sireader.SIReaderCardChanged as e:
                print(str(e))


def get_ports():
    ports = []
    for i in range(32):
        try:
            p = 'COM' + str(i)
            com = serial.Serial(p, 38400, timeout=5)
            com.close()
            ports.append(p)
        except serial.SerialException:
            continue

    return ports


def choose_port():
    ports = get_ports()
    if len(ports):
        print("Доступные порты:")
        for i, p in enumerate(ports):
            print("{} - {}".format(i, p))
        port = ports[0]
        return port
    else:
        print("Нет доступных портов")
        return None


port_runner = []


if __name__ == '__main__':
    port = choose_port()
    if port is not None:
        reader = SIReaderThread(port)
        reader.start()
        port_runner.append(reader)