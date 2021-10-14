import math
import struct
from dataclasses import dataclass

import serial

PACKET_LENGTH = 10


@dataclass
class RC3563Reading:
    voltage_v: float
    resistance_ohm: float


def parse_packet(pkt: bytes) -> RC3563Reading:
    status_display, r_range_code, r_display_bytes, sign_code, v_range_code, v_display_bytes = struct.unpack('BB3sBB3s', pkt)

    r_display_code = (status_display & 0xF0) >> 4
    v_display_code = (status_display & 0x0F) >> 0

    assert sign_code in (0, 1)
    assert r_range_code in (1, 2, 3, 4, 5, 6)
    assert r_display_code in (0x05, 0x06, 0x09, 0x0a)
    assert v_display_code in (0x04, 0x08)

    r_display_value = struct.unpack('I', r_display_bytes + b"\x00")[0] / 10000
    resistance_base = r_display_value

    sign = 1 if sign_code == 1 else -1
    v_display_value = struct.unpack('I', v_display_bytes + b"\x00")[0] / 10000
    voltage = sign * v_display_value

    if r_display_code == 0x05:
        resistance = resistance_base * 0.001
    elif r_display_code == 0x06:
        resistance = math.inf
    elif r_display_code == 0x09:
        resistance = resistance_base
    elif r_display_code == 0x0a:
        resistance = math.inf

    # noinspection PyUnboundLocalVariable
    return RC3563Reading(voltage, resistance)


class RC3563:
    def __init__(self, path: str):
        self.serial = serial.Serial(path, 115200, timeout=1)

    def close(self):
        self.serial.close()

    def read(self) -> RC3563Reading:
        while True:
            pkt = self.serial.read(PACKET_LENGTH)
            if len(pkt) == 0:
                continue
            if len(pkt) != PACKET_LENGTH:
                self.serial.flushInput()
                continue

            pkt = parse_packet(pkt)
            return pkt


__all__ = [
    "RC3563Reading",
    "RC3563",
]
