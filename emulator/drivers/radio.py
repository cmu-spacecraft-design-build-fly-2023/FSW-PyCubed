import asyncio
import queue
import random


class RadioDebug:
    def __init__(self, radio):
        self.radio = radio
        self.last_tx_packet = None

    def push_rx_queue(self, packet):
        """Debug function to push a packet into the rx queue (fifo)"""
        self.radio._rx_queue.put(packet)

    def reset(self):
        self.clear_rx_queue()
        self.clear_tx_queue()

    def clear_tx_queue(self):
        """Debug function to clear the tx queue"""
        self.radio._tx_queue = queue.Queue()

    def clear_rx_queue(self):
        """Debug function to clear the rx queue"""
        self.radio._rx_queue = queue.Queue()


class Radio:
    def __init__(self):
        self.node = 0
        self.listening = False

        self._rx_queue = queue.Queue()
        self._rx_time_bias = 0.5
        self._rx_time_dev = 0.3

        self._tx_queue = queue.Queue()
        self._tx_time_bias = 0.5
        self._tx_time_dev = 0.3

        self._last_rssi = -147.0
        self._frequency_error = 123.45

        self.test = RadioDebug(self)

    def listen(self):
        self.listening = True

    async def receive(self, *, keep_listening=True, with_header=False, with_ack=False, timeout=None, debug=False):
        rx_time = self._rx_time_bias + (random.random() - 0.5) * self._rx_time_dev
        await asyncio.sleep(rx_time)
        if self._rx_queue.empty():
            return None
        return self._rx_queue.get().observe()

    def last_rssi(self):
        return self._last_rssi

    def frequency_error(self):
        return self._frequency_error

    def sleep(self):
        self.listening = False

    async def send(self, packet, destination=0x00, keep_listening=True):
        tx_time = self._tx_time_bias + (random.random() - 0.5) * self._tx_time_dev
        await asyncio.sleep(tx_time)
        self.test.last_tx_packet = packet
        return None

    async def send_with_ack(self, packet, keep_listening=True):
        await self.send(packet)
        return True

    def fifo_empty(self):
        return True
