from bitstring import BitArray


class Parameter:

    raw = None
    value = None

    def __str__(self):
        return "{}".format(self.value)

    def get_raw(self):
        return self.raw

    def get_value(self):
        return self.value


class ParamSimple(Parameter):

    def set_raw(self, raw):
        self.raw = raw
        self.value = raw

    def set_value(self, value):
        self.raw = value
        self.value = value


class ParamOnOff(Parameter):

    def set_raw(self, raw):
        self.raw = raw
        self.value = "On" if raw else "Off"

    def set_value(self, value):
        if isinstance(value, str):
            value = value.lower()
            raw = 1 if value == "on" else 0
        elif isinstance(value, bool):
            raw = int(value)
        else:
            raw = min(value, 1) if value > 0 else max(value, 0)
        self.set_raw(raw)


class ParamTable(Parameter):
 
    def __init__(self, table):
        self.table_decode = table
        self.table_encode = { v : i for i, v in enumerate(table) }
 
    def set_raw(self, raw):
        self.raw = raw
        self.value = self.table_decode[raw]
 
    def set_value(self, value):
        self.raw = self.table_encode[value]
        self.value = value
 
 
class ParamRange(Parameter):
 
    def __init__(self, offset, value_min, value_max):
        self.offset = offset
        self.value_min = value_min
        self.value_max = value_max
 
    def set_raw(self, raw):
        self.raw = raw
        value = raw + self.offset
        self.value = min(value, self.value_max) if value > 0 else max(value, self.value_min)
 
    def set_value(self, value):
        self.value = min(value, self.value_max) if value > 0 else max(value, self.value_min)
        self.raw = value - self.offset  
 
 
class ParamPan(ParamRange):
 
    def set_raw(self, raw):
        super().set_raw(raw)
        if self.value == 0:
            self.value = "CNT"
        elif self.value < 0:
            self.value = "L{}".format(-self.value)
        else:
            self.value = "R{}".format(self.value)
 
    def set_value(self, value):
        if value == "CNT":
            dummy_value = 0
        elif value[0] == "L":
            dummy_value = -int(value[1:])
        else:
            dummy_value = int(value[1:])
        super().set_value(dummy_value)
        self.value = value


class ParamEFSense(Parameter):

    def set_raw(self, raw):
        self.raw = raw
        self.value = "Hold" if raw == 127 else raw

    def set_value(self, value):
        self.raw = 127 if value == "Hold" else value
        self.value = value


class ParamBitArray(Parameter):

    def __init__(self, length, invert=False):
        self.length = length
        self.invert = invert

    def set_raw(self, raw):
        self.raw = raw
        value = BitArray(uint=raw, length=self.length) 
        if self.invert:
            value = ~value
        self.value = list(value)

    def set_value(self, value):
        raw = BitArray(value) 
        self.raw = (~raw).uint if self.invert else raw.uint
        self.value = value 

