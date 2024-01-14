import sys
import struct
with open(sys.argv[1], "rb") as infile:
    indata = bytearray(infile.read())


def e(val):
    return struct.pack("<I", val)


for i in range(0, len(indata), 4):
    d = struct.unpack("<I", indata[i:i + 4])[0]
    if (d & ~0x1f) == 0xd51bd040:
        # from: msr TPIDR_EL0, x(?)
        # to:   msr TPIDRRO_EL0, x(?)
        indata[i:i + 4] = e(0xd51bd060 | (d & 0x1f))
    elif (d & ~0x1f) == 0xd53bd040:
        # from: mrs x(?), TPIDR_EL0
        # to:   mrs x(?), TPIDRRO_EL0
        indata[i:i + 4] = e(0xd53bd060 | (d & 0x1f))
    elif d == 0xd4000001:
        # from: svc #0
        # to:   brk #0xbeef
        indata[i:i + 4] = e(0xd437dde0)

with open(sys.argv[2], "wb") as outfile:
    outfile.write(indata)
