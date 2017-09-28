#
# Class to hold all properties of a CAN message
# as it is represented in a DBC file
#

from signals import Signal

class Message:
    #
    # Initialize new message object
    #
    def __init__(self, s):
        self.clear()
        if not (s is None):
            self.parse(s)

    #
    # Create and clear all object properties
    #
    def clear(self):
        self.ID = 0
        self.Name = ""
        self.DLC = 0
        self.layout = {}

    #
    # Parse a CAN message from a DBC file
    #
    def parse(self, s):
        self.clear()

        lines = s.strip().split("\n")

        header = lines[0]
        parts = header.split(" ")
        if parts[0] != "BO_":
            print "Error: Expected \"BO_\" at beginning of message. Got \"" + parts[0] + "\"."
        self.ID = int(parts[1])
        self.Name = parts[2][:-1]
        self.DLC = int(parts[3])
        # TODO: Evaluate whatever is the meaning of "Vector__XXX"

        for line in lines[1:]:
            parts = line.split(" ")
            if parts[0] != "" or parts[1] != "SG_":
                print "Error: Expected \"SG_\" at the beginning of signal. Got \"" + parts[1] + "\"."
            self.layout.push(Signal(line))

    #
    # Output object as string
    #
    def __str__(self):
        header = "BO_ " + str(self.ID) + " " + str(self.Name) + ": " + str(self.DLC) + " Vector__XXX"
        return header

