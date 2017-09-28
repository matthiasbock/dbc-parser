#
# Data base CAN (DBC) file format library
#
# A DBC file contains information about the
# constitution of CAN messages (frames) and
# the signals they are consituted from.
# This library supports reading DBC files
# and writing matching C structs
# e.g. for implementation on a microcontroller.
#

from messages import Message

class DBC:
    #
    # Initialize object
    #
    def __init__(self, s):
        self.clear()
        if not (s is None):
            self.parse(s)

    #
    # Create and clear all object properties
    #
    def clear(self):
        version = "";
        namespace = [];
        messages = [];

    #
    # Import object from DBC file
    #
    def load(self, filename):
        self.parse(open(filename, "r").read())

    #
    # Parse object properties from string
    #
    def parse(self, s):
        self.clear()
        lines = s.split("\n")

        PARSE_TOP = 0
        PARSE_NS = "NS_"
        PARSE_BS = "BS_"
        PARSE_BU = "BU_"
        PARSE_BO = "BO_"

        state = PARSE_TOP

        for line in lines:
            if state == PARSE_TOP:
                # skip empty lines
                if line.strip() == "":
                    continue
                parts = line.split(" ")
                if len(parts) < 1:
                    continue
                # DBC file version
                if parts[0] == "VERSION":
                    self.version = parts[1][1:-1]    # without the quotes
                    continue
                # begin sub-block
                buffer = ""
                if len(parts) > 1 and parts[1] == ":":
                    state = parts[0]
                    continue
            
            if state = PARSE_NS:
                # empty line: return to top
                if line.strip() == "":
                    state = PARSE_TOP
                    continue
                self.namespace.push(line.strip())
            
            if state == PARSE_BO:
                # empty line: parse buffer and return to top
                if line.strip() == "":
                    self.messages.push(Message(buffer))
                    state = PARSE_TOP
                    continue
                buffer += line + "\n"

            # in any case: return to top on an empty line            
            if line.strip() == "":
                state = PARSE_TOP
                continue
