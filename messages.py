#
# Class to hold all properties of a CAN message
# as it is represented in a DBC file
#

from signals import Signal

class Message:
    #
    # Initialize new message object
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
        self.ID = 0
        self.name = ""
        self.DLC = 0
        self.signals = []

    #
    # Parse a CAN message from a DBC file
    #
    def parse(self, s, debug=False):
        self.clear()
        lines = s.strip().split("\n")
        if debug:
            print "Parsing message"
            print lines
        header = lines[0]
        parts = header.split(" ")
        if parts[0] != "BO_":
            print "Aborting: Expected \"BO_\" at beginning of message. Got \"" + parts[0] + "\"."
            return
        self.ID = int(parts[1])
        self.name = parts[2][:-1]
        self.DLC = int(parts[3])
        # TODO: Evaluate whatever is the meaning of "Vector__XXX"

        for line in lines[1:]:
            self.signals.append(Signal(line, debug))

    #
    # Output object as string
    #
    def __str__(self):
        header = "BO_ " + str(self.ID) + " " + str(self.name) + ": " + str(self.DLC) + " Vector__XXX\n"
        signals = ""
        for signal in self.signals:
            signals += str(signal)
        return header + signals
