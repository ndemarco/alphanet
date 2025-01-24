import re

# Constants
STX = "]\""  # ASCII Printable Start of Text
ETX = "]#"   # ASCII Printable End of Text
EOT = "]$"   # ASCII Printable End of Transmission
CHECKSUM_LENGTH = 4  # Length of the checksum in ASCII characters

# Define the demo_message string
demo_message = r'''];"bThank You];&n2for using the]-AlphaNET]-demo]-program]; o]6There are many different Alpha LED display models]8];&mYou may choose from]-]7One line models]-Two line models]-]8Three line models]-Four line models]-];"b]7Alphavision FS Series];&n0has over 100 models]-]7in Full Matrix];&jor Character Matrix configurations];&ito meet any large scale display requirement]-]; nZ];"bAlphavision VS Series];&a]8Our top-of-the-line full color indoor and outdoor product series for full video applications ...];&a]; q];"bEthernet connection];&n0Connect your Alpha display network to a LAN by using Alpha Ethernet adapters]; b]:8]3];"b]:3]2Alpha Ticker];&n3Alpha Tracker]1]; a]:5Display real-time stock and financial data on selected Alpha models that are 5 feet, 50 feet, or 500 feet long ....]; a];"b]:3Outdoor Products];&cAsk your Alpha Distributor];&n2about the unique AlphaEclipse Outdoor Products];&aOutdoor LED message centers or Time & Temperature displays to fit any advertising requirement ...];&a]; n2]+0]; b]:8Call your]; rAlpha Distributor]; s]; jtoday for more]; iinformation about the entire]; jAlpha Indoor and]; iAlphaEclipse Outdoor LED product families]; nS]; nX]#'''

# Function to compute checksum
def compute_checksum(data):
    """Computes a 16-bit checksum for given data string."""
    checksum = sum(ord(char) for char in data) & 0xFFFF  # 16-bit summation
    return f"{checksum:04X}"  # Format checksum as four ASCII uppercase hex digits

# Function to process the file and remove demo_message
def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Search for the demo_message within the content
    match = re.search(re.escape(demo_message), content)
    if match:
        start_index = match.start()
        end_index = match.end()

        # Find the preceding STX symbol
        stx_index = content.rfind(STX, 0, start_index)
        if stx_index == -1:
            print("No preceding STX found.")
            return

        # Find the first ETX symbol after the demo_message
        etx_index = content.find(ETX, end_index)
        if etx_index == -1:
            print("No corresponding ETX found.")
            return

        # Extract the command block from STX to ETX
        command_block = content[stx_index + len(STX):etx_index]
        
        # Remove the demo message from the command block
        new_command_block = command_block.replace(demo_message, '')

        # Compute new checksum
        new_checksum = compute_checksum(new_command_block)

        # Replace the old checksum with the new one
        checksum_start_index = etx_index + len(ETX)
        checksum_end_index = checksum_start_index + CHECKSUM_LENGTH
        content = (content[:checksum_start_index] +
                   new_checksum +
                   content[checksum_end_index:])

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.write(content)

        print("Demo message removed and checksum updated successfully.")

    else:
        print("Demo message not found in the file.")

# Usage example
file_path = "test_message.txt"
process_file(file_path)
