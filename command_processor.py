from abc import ABC, abstractmethod

# Common validation class for file labels
    DISPLAY_POSITIONS = {
        "20H": {"position": "Middle Line", "desc": "Text centered vertically."},
        "22H": {"position": "Top Line", "desc": "Text begins on the top line of the sign and the sign will use all its lines minus 1 in order to display the text. For example, a 6-line sign will allow a maximum of 5 lines (6 minus 1) for the Top Position. The Top/Bottom Line break will remain fixed until the next Middle or Fill position is specified."},
        "26H": {"position": "Bottom Line", "desc": "The starting position of the Bottom Line(s) immediately follows the last line of the Top Line. For example, a 6-line sign with 3 lines of text associated with the Top Line would start the Bottom Line text on the 4th line of the sign."},
        "30H": {"position": "Fill", "desc": "The sign will fill all available lines, centering the lines vertically."},
        "31H": {"position": "Left", "desc": "Text begins on the left side of the sign and the sign will use all its lines minus 1 in order to display the text (Alpha 3.0 protocol only)."},
        "32H": {"position": "Right", "desc": "Text begins on the left side of the sign and the sign will use all its lines minus 1 in order to display the text (Alpha 3.0 protocol only)."}
    }

    MODE_CODES = {
        "61H": {"mode": "ROTATE", "desc": "Message travels right to left."},
        "62H": {"mode": "HOLD", "desc": "Message remains stationary."},
        "63H": {"mode": "FLASH", "desc": "Message remains stationary and flashes."},
        "65H": {"mode": "ROLL UP", "desc": "Previous message is pushed up by a new message."},
        "66H": {"mode": "ROLL DOWN", "desc": "Previous message is pushed down by a new message."},
        "67H": {"mode": "ROLL LEFT", "desc": "Previous message is pushed left by a new message."},
        "68H": {"mode": "ROLL RIGHT", "desc": "Previous message is pushed right by a new message."},
        "69H": {"mode": "WIPE UP", "desc": "New message is wiped over the previous message from bottom to top."},
        "6AH": {"mode": "WIPE DOWN", "desc": "New message is wiped over the previous message from top to bottom."},
        "6BH": {"mode": "WIPE LEFT", "desc": "New message is wiped over the previous message from right to left."},
        "6CH": {"mode": "WIPE RIGHT", "desc": "New message is wiped over the previous message from left to right."},
        "6DH": {"mode": "SCROLL", "desc": "New message line pushes the bottom line to the top line if 2-line sign."},
        "6FH": {"mode": "AUTOMODE", "desc": "Various Modes are called upon to display the message automatically."},
        "70H": {"mode": "ROLL IN", "desc": "Previous message is pushed toward the center of the display by the new message."},
        "71H": {"mode": "ROLL OUT", "desc": "Previous message is pushed outward from the center by the new message."},
        "72H": {"mode": "WIPE IN", "desc": "New message is wiped over the previous message in an inward motion."},
        "73H": {"mode": "WIPE OUT", "desc": "New message is wiped over the previous message in an outward motion."},
        "74H": {"mode": "COMPRESSED ROTATE", "desc": "Message travels right to left. Characters are approximately one half their normal width. (Only available on certain sign models.)"},
        "75H": {"mode": "EXPLODE", "desc": "Message flies apart from the center (Alpha 3.0 protocol)."},
        "76H": {"mode": "CLOCK", "desc": "Wipe in a clockwise direction (Alpha 3.0 protocol)."},
        "6EH": {"mode": "SPECIAL", "desc": "This is followed by a Special Specifier ASCII character which defines one of the Special Modes. See “Special Modes” on page 89."},
        "30H": {"mode": "TWINKLE", "desc": "Message will twinkle on the sign."},
        "31H": {"mode": "SPARKLE", "desc": "New message will sparkle over the current message."},
        "32H": {"mode": "SNOW", "desc": "Message will “snow” onto the display."},
        "33H": {"mode": "INTERLOCK", "desc": "New message will interlock over the current message in alternating rows of dots from each end."},
        "34H": {"mode": "SWITCH", "desc": "Alternating characters “switch” off the sign up and down. New message “switches” on in a similar manner."},
        "35H": {"mode": "SLIDE or CYCLE COLORS", "desc": "New message slides onto the sign one character at a time from right to left."},
        "36H": {"mode": "SPRAY", "desc": "New message sprays across and onto the sign from right to left."},
        "37H": {"mode": "STARBURST", "desc": "“Starbursts” explode the new message onto the sign (animation)."},
        "38H": {"mode": "WELCOME", "desc": "The word “Welcome” is written in script across the sign (animation)."},
        "39H": {"mode": "SLOT MACHINE", "desc": "Slot machine symbols appear randomly across the sign (animation)."},
        "3AH": {"mode": "NEWS FLASH", "desc": "News flash animation"},
        "3BH": {"mode": "TRUMPET ANIMATION", "desc": "Trumpet animation"},
        "43H": {"mode": "CYCLE COLORS", "desc": "Color changes from one color to another."}
    }

    SPECIAL_IDENTIFIERS = {
        "53H": {"graphic": "THANK YOU", "desc": "The words “Thank You” are written in script across the sign (animation)."},
        "55H": {"graphic": "NO SMOKING", "desc": "A cigarette image appears, is then extinguished and replaced with a no smoking symbol (animation)."},
        "56H": {"graphic": "DON’T DRINK & DRIVE", "desc": "A car runs into a cocktail glass and is replaced with the text “Please don’t drink and drive” (animation)"},
        "57H": {"graphic": "RUNNING ANIMAL or FISH ANIMATION", "desc": "An animal runs across the sign (animation)."},
        "58H": {"graphic": "FIREWORKS", "desc": "Fireworks explode randomly across the sign (animation)."},
        "59H": {"graphic": "TURBO CAR or BALLOON ANIMATION", "desc": "A car drives across the sign (animation)."},
        "5AH": {"graphic": "CHERRY BOMB", "desc": "A bomb fuse burns down followed by an explosion (animation)."}
    }

    MODIFIERS = {
        b'\x05' + b'0': "Double Height Off",
        b'\x05' + b'1': "Double Height On",
        b'\x06' + b'0': "True Descenders Off",
        b'\x06' + b'1': "True Descenders On",
    }



    @staticmethod
    def parse_mode(mode_bytes):
        """Parses the mode field if present."""
        mode_data = {}
        if not mode_bytes:
            return None  # No mode field provided

        if len(mode_bytes) < 2:
            print("Error: Mode field incomplete")
            return None

        display_pos = chr(mode_bytes[0])
        mode_code = chr(mode_bytes[1])

        if display_pos not in Validator.DISPLAY_POSITIONS:
            print(f"Invalid display position: {display_pos}")
            return None
        if mode_code not in Validator.MODE_CODES:
            print(f"Invalid mode code: {mode_code}")
            return None

        mode_data['display_position'] = Validator.DISPLAY_POSITIONS[display_pos]
        mode_data['mode'] = Validator.MODE_CODES[mode_code]

        if mode_code == "S":  # Special mode requires an extra identifier
            if len(mode_bytes) < 3:
                print("Error: Special mode requires an identifier")
                return None
            special_identifier = chr(mode_bytes[2])
            if special_identifier not in Validator.SPECIAL_IDENTIFIERS:
                print(f"Invalid special identifier: {special_identifier}")
                return None
            mode_data['special_identifier'] = Validator.SPECIAL_IDENTIFIERS[special_identifier]

        return mode_data

    @staticmethod
    def process_message(message_bytes):
        """Processes message content, identifying ASCII modifiers."""
        parsed_message = []
        i = 0
        while i < len(message_bytes):
            if i < len(message_bytes) - 1 and bytes(message_bytes[i:i+2]) in Validator.MODIFIERS:
                parsed_message.append(f"[{Validator.MODIFIERS[bytes(message_bytes[i:i+2])]}]")
                i += 2  # Skip modifier bytes
            else:
                parsed_message.append(chr(message_bytes[i]))
                i += 1
        return ''.join(parsed_message)


# Abstract Command Class
class Command(ABC):
    @abstractmethod
    def execute(self, data):
        pass


# Write Text File Command (0x41, 'A')
class WriteTextFileCommand(Command):
    def execute(self, data):
        if len(data) < 2:
            print("Error: Insufficient data for Write Text File command.")
            return

        file_label = data[0]
        if not Validator.validate_file_label(file_label):
            return

        remaining_data = data[1:]
        mode_field = None
        message_data = remaining_data

        # If the second byte is an ASCII character (mode field is optional)
        if remaining_data and (0x20 <= remaining_data[0] <= 0x7E):
            mode_field = Validator.parse_mode(remaining_data[:3])  # Try parsing up to 3 bytes
            if mode_field:
                message_data = remaining_data[len(mode_field):]  # Adjust message start position

        # Process message with modifiers
        parsed_message = Validator.process_message(message_data)

        # Final output
        print(f"Writing to file label {hex(file_label)}")
        if mode_field:
            print(f"Mode: {mode_field}")
        print(f"Message: {parsed_message}")


# Command Factory
class CommandFactory:
    _commands = {
        0x41: WriteTextFileCommand  # 'A' command
    }

    @staticmethod
    def get_command(command_byte):
        command_class = CommandFactory._commands.get(command_byte)
        if command_class:
            return command_class()
        else:
            raise ValueError(f"Unknown command: {hex(command_byte)}")


# Command Processor
class CommandProcessor:
    def process_packet(self, packet):
        if len(packet) < 1:
            print("Error: Empty packet")
            return
        
        command_byte = packet[0]  # Extract command byte
        data = packet[1:]  # Extract data bytes

        try:
            command = CommandFactory.get_command(command_byte)
            command.execute(data)
        except ValueError as e:
            print(e)


# Example Usage
processor = CommandProcessor()

# Valid command: Write text file with message
processor.process_packet([0x41, 0x21, ord("C"), ord("N"), ord("H"), ord("e"), ord("l"), ord("l"), ord("o")])

# Command with special mode
processor.process_packet([0x41, 0x21, ord("L"), ord("S"), ord("X"), ord("W"), ord("o"), ord("r"), ord("l"), ord("d")])

# Command with modifiers
processor.process_packet([0x41, 0x21, ord("T"), ord("B"), ord("H"), 0x05, ord("1"), ord("E"), ord("x"), ord("a"), ord("m"), ord("p"), ord("l"), ord("e")])

# Invalid file label
processor.process_packet([0x41, 0x30, ord("T"), ord("N"), ord("T"), ord("e"), ord("s"), ord("t")])  # 0x30 is invalid

# Invalid mode
processor.process_packet([0x41, 0x21, ord("X"), ord("B"), ord("T"), ord("e"), ord("s"), ord("t")])  # 'X' is not a valid position

# Unknown command
processor.process_packet([0x99, 0x21, ord("H"), ord("i")])  # 0x99 is an unknown command
