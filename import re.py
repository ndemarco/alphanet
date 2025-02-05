import re

# 1) Leading NULs
leading_nuls_regex = re.compile(
    r'^(?P<leading_nuls>[\x00]*)'
)

# 2) Start Of Header: ]! + type code (1 ASCII printable) + address (2 chars of digit or ?)
start_of_header_regex = re.compile(
    r'^\]!(?P<type_code>[ -~])(?P<address>[0-9?]{2})'
)

# 3) Optional repeats: zero or more occurrences of ",<type_code><address>"
repeats_regex = re.compile(
    r'^(?:,(?P<type_code>[ -~])(?P<address>[0-9?]{2}))+'
)

# 4) One or more "packets":
#    each packet is ]\  ...  ]# plus optional 4-digit hex
#    we will match the first packet and then see if we can continue matching more.
packet_regex = re.compile(
    r'^\]\\(?P<contents>[\s\S]*?)\]#(?P<checksum>[0-9A-Fa-f]{0,4})?'
    # We use [\s\S]*? (lazy) so we stop at the first ]#
)

# 5) End Of Transmission
end_of_transmission_regex = re.compile(
    r'^\]\$'
)

# 6) Trailing NULs
trailing_nuls_regex = re.compile(
    r'^(?P<trailing_nuls>[\x00]*)$'
)


def parse_ascii_data_frame(data):
    """
    Returns True if data passes the multi-step checks.
    Otherwise prints debug info and returns False.
    """

    original_data = data  # keep a copy for reference
    
    # Step 1: leading NULs
    m = leading_nuls_regex.match(data)
    if m:
        # Debug
        print(f"[DEBUG] Leading NULs matched: {repr(m.group('leading_nuls'))}")
        data = data[m.end():]  # move past leading NULs
    else:
        print("[ERROR] Leading NULs not matched.")
        return False
    
    # Step 2: start of header
    m = start_of_header_regex.match(data)
    if not m:
        print("[ERROR] SOH (']!') + type code + address not found right after leading NULs.")
        return False
    print(f"[DEBUG] Found SOH ]!: type_code={m.group('type_code')}, address={m.group('address')}")
    data = data[m.end():]

    # Step 3: optional repeats
    # Attempt to match repeats at the current start. 
    # Because it's optional, we do finditer or match in a loop.
    repeated_header_count = 0
    while True:
        m = repeats_regex.match(data)
        if m:
            # could be multiple repeats in a single match because of the group (?: ... )+
            # We only move the end of the entire match forward
            end_pos = m.end()
            # We can debug each comma-chunk by re-scanning the matched portion
            # But for simplicity, just say "we found more repeats"
            repeated_header_count += 1
            data = data[end_pos:]
        else:
            break

    if repeated_header_count > 0:
        print(f"[DEBUG] Found {repeated_header_count} block(s) of repeating ',<type_code><address>'")

    # Step 4: one or more packets
    packet_count = 0
    while True:
        m = packet_regex.match(data)
        if not m:
            break
        packet_count += 1
        # Debug
        contents_preview = m.group('contents')[:40].replace('\n', '\\n')
        cs = m.group('checksum') if m.group('checksum') else "None"
        print(f"[DEBUG] Packet #{packet_count} matched. "
              f"Checksum={cs}, contents preview={repr(contents_preview)}")
        data = data[m.end():]

    if packet_count == 0:
        print("[ERROR] Found no valid STX..ETX packets. (Missing `]\\ ... ]#` block?)")
        return False

    # Step 5: end of transmission
    m = end_of_transmission_regex.match(data)
    if not m:
        print("[ERROR] No EOT marker `]$` found after packets.")
        return False
    print("[DEBUG] Found EOT marker ]$")
    data = data[m.end():]

    # Step 6: trailing NULs
    m = trailing_nuls_regex.match(data)
    if not m:
        print("[ERROR] Trailing NULs check failed. Extra junk after `]$`?")
        return False
    print(f"[DEBUG] Trailing NULs matched: {repr(m.group('trailing_nuls'))}")

    print("[INFO] All checks passed successfully.")
    return True


if __name__ == "__main__":
    # Replace this string with the one you're testing
    test_string = (
        "<NUL><NUL>...]!Z00]\"E$AAU000AFF00!AL04BAFF00]#0583]\"E2!A1]#010F]$..."
        # etc...
    )

    is_valid = parse_ascii_data_frame(test_string)
    print("Valid?" if is_valid else "Invalid!")
