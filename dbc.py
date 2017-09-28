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
    def __init__(self, s=None, debug=False):
        if s is None:
            self.clear()
        else:
            self.parse(s, debug)

    #
    # Create and clear all object properties
    #
    def clear(self):
        self.version = "";
        self.namespace = [];
        self.messages = [];

    #
    # Import object from DBC file
    #
    def load(self, filename):
        self.parse(open(filename, "r").read())

    #
    # Parse object properties from string
    #
    def parse(self, s, debug=False):
        self.clear()
        lines = s.split("\n")

        if debug:
            print lines

        PARSE_TOP = 0
        PARSE_NS = "NS_ : "
        PARSE_BS = "BS_:"
        PARSE_BU = "BU_:"
        PARSE_BO = "BO_ "

        state = PARSE_TOP

        for line in lines:
            line = line.replace("\t", " ")
            if state == PARSE_TOP:
                # skip empty lines
                if line.strip() == "":
                    continue
                parts = line.split(" ")
                if len(parts) < 1:
                    continue
                # DBC file version
                if parts[0] == "VERSION":
                    if debug:
                        print "Parsing version..."
                    self.version = parts[1][1:-1]    # without the quotes
                    continue
                # begin sub-block
                buffer = ""
                if line in [PARSE_NS, PARSE_BS, PARSE_BU]:
                    state = parts[0]
                    if debug:
                        print "Parsing " + str(state) + "..."
                elif len(line) > 3 and line[:4] == PARSE_BO:
                    state = PARSE_BO
                    if debug:
                        print "Parsing " + str(state) + "..."

            if state == PARSE_NS:
                # empty line: return to top
                if line.strip() == "":
                    state = PARSE_TOP
                    if debug:
                        print "Return to top"
                    continue
                self.namespace.append(line.strip())

            if state == PARSE_BO:
                # empty line: parse buffer and return to top
                if line.strip() == "":
                    self.messages.append(Message(buffer))
                    state = PARSE_TOP
                    if debug:
                        print "Return to top"
                    continue
                buffer += line + "\n"

            # in any case: return to top on an empty line
            if line.strip() == "":
                state = PARSE_TOP
                if debug:
                    print "Return to top"
                continue

    #
    # Export DBC file as string
    #
    def __str__(self):
        version = "VERSION \"" + self.version + "\"\n"
        messages = ""
        for message in self.messages:
            messages += str(message) + "\n"
        buffer = version + "\n" + messages
        return buffer
