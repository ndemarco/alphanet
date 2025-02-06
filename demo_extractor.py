import re
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Constants
SOH = ']!'   # ASCII printable Start of Header
STX = ']"'  # ASCII Printable Start of Text
ETX = ']#'   # ASCII Printable End of Text
EOT = ']$'   # ASCII Printable End of Transmission
ESC = '];'   # ASCII Escape character
CHECKSUM_LENGTH = 4  # Length of the checksum in ASCII characters

# Define the demo_message string

def read_message(filename):
    '''Reads the message file and returns the message.'''
    try:
        with open(filename, 'r') as file:
            message = file.read()
        logging.info(f"Read {len(message)} bytes from input file.")
        return message

    except Exception as e:
        logging.error(f"Could not read file: {e}")

def parse_frames(message):
    """
    Parse frame from message. Returns a list of raw frames, each bounded by SOH ... EOT
    """
    frame_pattern = re.escape(SOH) + r'(.*?)' + re.escape(EOT)
    # DOTALL so '.' matches newlines, if needed
    frames = re.findall(frame_pattern, message, flags=re.DOTALL)
    return frames

def parse_packets(frame):
    """
    Parse packets from frame. Returns a list of packet contents (including STX, ETX, and optional checksum).
    """
    # Pattern: STX (some stuff) ETX + optional 4-digit hex checksum
    pattern = re.escape(STX) + r'.*?' + re.escape(ETX) + r'(?:[0-9a-fA-F]{4})?'
    return re.findall(pattern, frame, flags=re.DOTALL)

def strip_checksum(packet):
    """
    If packet ends with ETX + 4 hex digits, it's a checksum.
    Remove it, and return (stripped_packet, True)
    Otherwise return (original_packet, False)
    """

    etx_index = packet.rfind(ETX)
    if etx_index == -1:
        return packet, False

    # Everything after ETX
    suffix = packet[etx_index + len(ETX):]
    # Verify the suffix is exactly 4 hex digits
    if len(suffix) == 4 and all(c in "0123456789ABCDEFabcdef" for c in suffix):
        return packet[:-4], True
    else:
        return packet, False

def compute_checksum(packet):
    '''Computes a 16-bit checksum for a properly formatted packet. Properly formatted
    packets start with STX and end with ETX.

    Returns a properly formatted 4-digit hex checksum encoded as ASCII characters.
    '''
    checksum = sum(ord(char) for char in packet) & 0xFFFF  # 16-bit summation
    formatted_checksum = f"{checksum:04X}"  # Format checksum as four ASCII uppercase hex digits
    logging.debug(f"Computed checksum: {formatted_checksum} for data: {packet}")
    return formatted_checksum

def fix_packet(packet, demo_message):
    """
    - If demo message in packet:
        1) Remove any old 4-digit checksum from the end
        2) Remove demo_message from packet
        3) Recompute and append new checksum
      Return the fixed packet

    - If demo message not in packet, return the packet.
    """

    if demo_message not in packet:
        return packet

    # 1) remove the checksum.
    stripped, had_checksum = strip_checksum(packet)


    # 2) remove the demo message
    stripped = stripped.replace(demo_message, '')

    # 3) recomput and append new checksum
    new_sum = compute_checksum(stripped)
    revised_packet = stripped + new_sum

    logging.info(f"Found demo message in packet; revised packet: {revised_packet}")
    return revised_packet


# Let's go!
def main():

    demo_message = r'''];"bThank You];&n2for using the]-AlphaNET]-demo]-program]; o]6There are many different Alpha LED display models]8];&mYou may choose from]-]7One line models]-Two line models]-]8Three line models]-Four line models]-];"b]7Alphavision FS Series];&n0has over 100 models]-]7in Full Matrix];&jor Character Matrix configurations];&ito meet any large scale display requirement]-]; nZ];"bAlphavision VS Series];&a]8Our top-of-the-line full color indoor and outdoor product series for full video applications ...];&a]; q];"bEthernet connection];&n0Connect your Alpha display network to a LAN by using Alpha Ethernet adapters]; b]:8]3];"b]:3]2Alpha Ticker];&n3Alpha Tracker]1]; a]:5Display real-time stock and financial data on selected Alpha models that are 5 feet, 50 feet, or 500 feet long ....]; a];"b]:3Outdoor Products];&cAsk your Alpha Distributor];&n2about the unique AlphaEclipse Outdoor Products];&aOutdoor LED message centers or Time & Temperature displays to fit any advertising requirement ...];&a]; n2]+0]; b]:8Call your]; rAlpha Distributor]; s]; jtoday for more]; iinformation about the entire]; jAlpha Indoor and]; iAlphaEclipse Outdoor LED product families]; nS]; nX'''


    message = read_message('test_message.txt')
    if not message:
        logging.error("No message read from file.")
        return

    # 1) Split the entire message into frames.
    frames = parse_frames(message)
    logging.info(f"Found {len(frames)} frame(s).")
    
    revised_frames = []
    for frame_index, frame in enumerate(frames, start=1):
        logging.info(f"Frame {frame_index} has length {len(frame)} bytes.")
        logging.info(f"   {frame}\n")

        # 2) Within each frame, find all packets    
        packets = parse_packets(frame)
        logging.info(f"   Found {len(packets)} packet(s) in this frame.")

        # 3) Fix each packet, if applicable
        revised_packets = []
        for i, packet in enumerate(packets, start=1):
            fixed = fix_packet(packet, demo_message)
            revised_packets.append(fixed)
            if fixed != packet:
                logging.info(f"   Revised packet {i} in frame {frame_index}:\n   {fixed}")

        # 4) Reassemble the frame content by substituting the revised packets
        #    back in place of the originals. Run a single pass to replace each
        #    original packet with its revised version in the same order found.

        revised_frame = frame
        for old, new in zip(packets, revised_packets):
            revised_frame = revised_frame.replace(old, new, 1)

        # Save the newly assembled frame with the same bounding EOT
        revised_frames.append(revised_frame)

    # 5) Reassemble the entire message: SOH + revised_frame + EOT for each frame.
    final_message = ""
    for frame_data in revised_frames:
        final_message += SOH + frame_data + EOT

    return final_message

print(main())
logging.info("Final message")
