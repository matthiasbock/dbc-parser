#
# Class to hold all properties of a CAN signal
# as it is represented in a DBC file
#

class SignalValueType:
    UNSIGNED = "+"
    SIGNED = "-"
    FLOAT = "SIG_VALTYPE_ 1"
    DOUBLE = "SIG_VALTYPE_ 2"

class SignalByteOrder:
    INTEL = "1"
    MOTOROLA = "0"

class Signal:
    #
    # Initialize object
    #
    def __init__(self, s=None, debug=False):
        if s is None:
            self.clear()
        else:
            self.parse(s, debug)

    #
    # Create and clear all signal properties
    #
    def clear(self):
        self.name = ""
        self.valuetype = SignalValueType.UNSIGNED
        self.startbit = 0
        self.bitlength = 0
        self.byteorder = SignalByteOrder.INTEL
        self.minimum = 0
        self.maximum = 0
        self.factor = 1
        self.offset = 0
        self.initial_value = 0
        self.unit = ""

    #
    # Parse signal from line string
    #
    def parse(self, s, debug=False):
        self.clear()
        parts = s.split(" ")
        if parts[0] != "" or parts[1] != "SG_":
            print "Aborting: Expected \"SG_\" at the beginning of signal. Got \"" + parts[1] + "\"."
            return
        self.name = parts[2]
        layout = parts[4]    # 36|12@1+
        p = layout.split("|")
        self.startbit = int(p[0])
        q = p[1].split("@")
        self.bitlength = int(q[0])
        self.byteorder = q[1][0]
        self.valuetype = q[1][1]
        factor_offset = parts[5]    # (1,0)
        p = factor_offset.split(",")
        self.factor = int(p[0][1:])
        self.offset = int(p[1][:-1])
        min_max = parts[6]    # [0|255]
        p = min_max.split("|")
        self.minimum = int(p[0][1:])
        self.maximum = int(p[1][:-1])
        self.unit = parts[7][1:-1]    # in quotes

    #
    # Export signal as string for DBC file
    #
    def __str__(self):
        layout = str(self.startbit) + "|" + str(self.bitlength) + "@" + self.byteorder + self.valuetype
        factor_offset = "(" + str(self.factor) + "," + str(self.offset) + ")"
        min_max = "[" + str(self.minimum) + "|" + str(self.maximum) + "]"
        line = " SG_ " + self.name + " : " + layout + " " + factor_offset + " " + min_max + " \"" + self.unit + "\" Vector__XXX\n"
        return line
