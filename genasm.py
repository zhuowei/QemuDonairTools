import json
print(json.dumps("mov x16, x0\n"))
# skip sp (register 31 in qemu); we use host sp
for i in range(0, 31):
	if i == 16:
		continue
	regbase = 4*16 + 8*i
	print(json.dumps("ldr x{}, [x16, #{}]\n".format(i, regbase)))
print(json.dumps("ldr x16, [x16, #{}]\n".format(4*16+8*32)))
print(json.dumps("br x16\n"))
