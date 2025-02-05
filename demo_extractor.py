import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

# Constants
stx = "\x02"
etx = "\x03"
hex_char_offset = 0x20
STX = chr(hex_char_offset + stx)


SOH = ']!'   # ASCII printable Start of Header
STX = ']"'  # ASCII Printable Start of Text
ETX = ']#'   # ASCII Printable End of Text
EOT = ']$'   # ASCII Printable End of Transmission
ESC = '];'   # ASCII Escape character

CHECKSUM_LENGTH = 4  # Length of the checksum in ASCII characters

# Define the demo_message string
demo_message = r'''];"bThank You];&n2for using the]-AlphaNET]-demo]-program]; o]6There are many different Alpha LED display models]8];&mYou may choose from]-]7One line models]-Two line models]-]8Three line models]-Four line models]-];"b]7Alphavision FS Series];&n0has over 100 models]-]7in Full Matrix];&jor Character Matrix configurations];&ito meet any large scale display requirement]-]; nZ];"bAlphavision VS Series];&a]8Our top-of-the-line full color indoor and outdoor product series for full video applications ...];&a]; q];"bEthernet connection];&n0Connect your Alpha display network to a LAN by using Alpha Ethernet adapters]; b]:8]3];"b]:3]2Alpha Ticker];&n3Alpha Tracker]1]; a]:5Display real-time stock and financial data on selected Alpha models that are 5 feet, 50 feet, or 500 feet long ....]; a];"b]:3Outdoor Products];&cAsk your Alpha Distributor];&n2about the unique AlphaEclipse Outdoor Products];&aOutdoor LED message centers or Time & Temperature displays to fit any advertising requirement ...];&a]; n2]+0]; b]:8Call your]; rAlpha Distributor]; s]; jtoday for more]; iinformation about the entire]; jAlpha Indoor and]; iAlphaEclipse Outdoor LED product families]; nS]; nX'''

def read_message(filename):
    '''Reads the message file and returns the message.'''
    try:
        with open(filename, 'r') as file:
            message = file.read()
        logging.info(f"Read {len(message)} bytes from input file.")
        return message

    except Exception as e:
        logging.error(f"Could not read file: {e}")

def compute_checksum(data):
    '''Computes a 16-bit checksum for a properly formatted packet. Properly formatted
    packets start with STX and end with ETX.

    Returns a properly formatted 4-digit hex checksum encoded as ASCII characters.
    '''
    
    # Packet must start with STX and end with ETX.
    # if data[:2] != STX or data[-2:] != ETX:
    #     return -1
    
    checksum = sum(ord(char) for char in data) & 0xFFFF  # 16-bit summation
    
    formatted_checksum = f"{checksum:04X}"  # Format checksum as four ASCII uppercase hex digits
    logging.debug(f"Computed checksum: {formatted_checksum} for data: {data}")
    return formatted_checksum

def parse_packets(message):
    ''' Mark the packets within a frame. Frames start with
        after NULs, with a SOH.
        The frame includes a type code and a sign address.
        Then come the packets, and there can be more than one.
        Packets end with ETX, then an optional checksum.
        The frame ends with EOT.
    '''
    
    packet_pattern = re.escape(SOH) + r'(.*?)' + re.escape(EOT)

    # List all packets in the message
    packets = re.findall(packet_pattern, message)
    logging.debug(f"Found {len(packets)} packets ")
    return packets

message = read_message('test_message.txt')
packets = parse_packets(message)

# Display the packets
for i, packet in enumerate(packets, start=1):
    print(f"Packet {i}: {packet}" + "\n")

# If found, remove demo_text from packet.

for i, packet in enumerate(packets, start=1):
    if demo_message in packet:
        stripped_packet = packet.replace(demo_message, '')
        # recompute checksum and add to end of packet
        logging.debug(f"Found demo message in packet {i}.")
        print(f"Packet {i}: {stripped_packet}")
        print(stripped_packet[:-4])
#        compute_checksum(stripped_packet)
    # logging.debug(f"Processed packet {i}.")

string = ']"E(1]#'
string = ']"A!12345TESTING12345];0b];"bThank You];&n2for using the]-AlphaNET]-demo]-program]; o]6There are many different Alpha LED display models]8];&mYou may choose from]-]7One line models]-Two line models]-]8Three line models]-Four line models]-];"b]7Alphavision FS Series];&n0has over 100 models]-]7in Full Matrix];&jor Character Matrix configurations];&ito meet any large scale display requirement]-]; nZ];"bAlphavision VS Series];&a]8Our top-of-the-line full color indoor and outdoor product series for full video applications ...];&a]; q];"bEthernet connection];&n0Connect your Alpha display network to a LAN by using Alpha Ethernet adapters]; b]:8]3];"b]:3]2Alpha Ticker];&n3Alpha Tracker]1]; a]:5Display real-time stock and financial data on selected Alpha models that are 5 feet, 50 feet, or 500 feet long ....]; a];"b]:3Outdoor Products];&cAsk your Alpha Distributor];&n2about the unique AlphaEclipse Outdoor Products];&aOutdoor LED message centers or Time & Temperature displays to fit any advertising requirement ...];&a]; n2]+0]; b]:8Call your]; rAlpha Distributor]; s]; jtoday for more]; iinformation about the entire]; jAlpha Indoor and]; iAlphaEclipse Outdoor LED product families]; nS]; nX]#'

print 
print(f"Checksum: {compute_checksum(string)}")