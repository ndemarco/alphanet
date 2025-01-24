import re
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

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
    formatted_checksum = f"{checksum:04X}"  # Format checksum as four ASCII uppercase hex digits
    logging.debug(f"Computed checksum: {formatted_checksum} for data: {data}")
    return formatted_checksum

# Function to process the file and remove demo_message
def process_file(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            content = file.read()
            logging.info(f"Read {len(content)} bytes from input file.")

        # Search for the demo_message within the content
        match = re.search(re.escape(demo_message), content)
        if not match:
            logging.warning("Demo message not found in the file.")
            return

        start_index = match.start()
        end_index = match.end()
        logging.info(f"Demo message found at index {start_index}-{end_index}.")

        # Find the preceding STX symbol
        stx_index = content.rfind(STX, 0, start_index)
        if stx_index == -1:
            logging.error("No preceding STX found.")
            return

        logging.info(f"Found STX at index {stx_index}.")

        # Find the first ETX symbol after the demo_message
        etx_index = content.find(ETX, end_index)
        if etx_index == -1:
            logging.error("No corresponding ETX found.")
            return

        logging.info(f"Found ETX at index {etx_index}.")

        # Extract the command block from STX to ETX
        command_block = content[stx_index + len(STX):etx_index]
        logging.debug(f"Original command block: {command_block}")

        # Remove the demo message from the command block
        new_command_block = command_block.replace(demo_message, '')
        logging.debug(f"New command block after removing demo_message: {new_command_block}")

        # Compute new checksum
        new_checksum = compute_checksum(new_command_block)

        # Build updated content
        cleaned_content = (
            content[:stx_index + len(STX)] + 
            new_command_block + 
            ETX + 
            new_checksum + 
            EOT + 
            content[etx_index + len(ETX) + CHECKSUM_LENGTH + len(EOT):]
        )

        # Write the updated content to the output file
        with open(output_file, 'w') as file:
            file.write(cleaned_content)
            logging.info(f"Updated content written to {output_file}")

        logging.info("Demo message removed and checksum updated successfully.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

# Usage example
input_file = "test_message.txt"
output_file = "clean_test_message.txt"

# Remove output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)
    logging.info(f"Existing output file {output_file} removed.")

process_file(input_file, output_file)
