from __future__ import unicode_literals

import calendar
import datetime
import os
import sys
import time

__all__ = [
    'encode_base32',
    'ulid',
]

py3 = (sys.version_info[0] == 3)
text_type = (str if py3 else unicode)

symbols = "0123456789abcdefghjkmnpqrstvwxyz"


def _to_binary(byte_list):
    if py3:
        return bytes(byte_list)
    else:
        return bytes(b''.join(chr(b) for b in byte_list))


def encode_base32(binary):
    """
    Encode 16 binary bytes into a 26-character long base32 string.
    :param binary: Bytestring or list of bytes
    :return: ASCII string of 26 characters
    :rtype: str
    """
    assert len(binary) == 16

    if not py3 and isinstance(binary, str):
        binary = [ord(b) for b in binary]

    return ''.join([
        symbols[(binary[0] & 224) >> 5],
        symbols[binary[0] & 31],
        symbols[(binary[1] & 248) >> 3],
        symbols[((binary[1] & 7) << 2) | ((binary[2] & 192) >> 6)],
        symbols[(binary[2] & 62) >> 1],
        symbols[((binary[2] & 1) << 4) | ((binary[3] & 240) >> 4)],
        symbols[((binary[3] & 15) << 1) | ((binary[4] & 128) >> 7)],
        symbols[(binary[4] & 124) >> 2],
        symbols[((binary[4] & 3) << 3) | ((binary[5] & 224) >> 5)],
        symbols[binary[5] & 31],
        symbols[(binary[6] & 248) >> 3],
        symbols[((binary[6] & 7) << 2) | ((binary[7] & 192) >> 6)],
        symbols[(binary[7] & 62) >> 1],
        symbols[((binary[7] & 1) << 4) | ((binary[8] & 240) >> 4)],
        symbols[((binary[8] & 15) << 1) | ((binary[9] & 128) >> 7)],
        symbols[(binary[9] & 124) >> 2],
        symbols[((binary[9] & 3) << 3) | ((binary[10] & 224) >> 5)],
        symbols[binary[10] & 31],
        symbols[(binary[11] & 248) >> 3],
        symbols[((binary[11] & 7) << 2) | ((binary[12] & 192) >> 6)],
        symbols[(binary[12] & 62) >> 1],
        symbols[((binary[12] & 1) << 4) | ((binary[13] & 240) >> 4)],
        symbols[((binary[13] & 15) << 1) | ((binary[14] & 128) >> 7)],
        symbols[(binary[14] & 124) >> 2],
        symbols[((binary[14] & 3) << 3) | ((binary[15] & 224) >> 5)],
        symbols[binary[15] & 31],
    ])


def ulid(timestamp=None):
    """
    Generate an ULID, formatted as a base32 string of length 26.

    :param timestamp: An optional timestamp override.
                      If `None`, the current time is used.
    :type timestamp: int|float|datetime.datetime|None
    :return: ASCII string
    :rtype: str
    """

    if timestamp is None:
        timestamp = time.time()
    elif isinstance(timestamp, datetime.datetime):
        timestamp = calendar.timegm(timestamp.utctimetuple())

    ts = int(timestamp )
    ts_bytes = _to_binary(
        (ts >> shift) & 0xFF for shift in (40, 32, 24, 16, 8, 0)
    )
    t2 = ts_bytes + os.urandom(10)
    return encode_base32(t2)


if __name__ == "__main__":

  print ulid()
  print ulid(1469918220538)[:10], "=", '01aryz847tbtvzvmzshk4dnj11'[:10]
