#!/usr/bin/env python3

import serial
import time

def main():
    # Open COM2 with 9600 baud, 7 data bits, even parity, 2 stop bits
    ser = serial.Serial(
        port="COM2",
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        timeout=1
    )

    # 1) First wake-up sequence: 20 NUL (0x00) bytes
    wake_up_1 = b"\x00" * 20

    # 2) Attribute/checksum blocks (taken from your working capture)
    attributes_block = (
        b']!Z00]'
        b'"E$AAU000AFF00!AL04BAFF00]#0583]'
        b'"E2!A1]#010F]'
    )

    # 3) Another 20 NUL bytes (some firmware expects a gap before text)
    wake_up_2 = b"\x00" * 20

    # 4) Simple text block:
    #    - "A!HELLO];" loads "HELLO" into the sign.
    #    - "0b];" helps finalize the page on certain firmware versions.
    text_block = (
        b']!Z00]'
        b'"A!HELLO];0b];'
    )

    # Combine all parts into one message
    full_message = wake_up_1 + attributes_block + wake_up_2 + text_block

    # Send the message
    ser.write(full_message)
    ser.flush()

    # Optional short delay to ensure everything is sent
    time.sleep(1)

    # Close the port
    ser.close()
    print("Message sent to COM2.")

if __name__ == "__main__":
    main()