"""
https://github.com/torvalds/linux/blob/610a9b8f49fbcf1100716370d3b5f6f884a2835a/mm/mmap.c#L1770
ffff80008041f568 T generic_get_unmapped_area_topdown
ffff80008041ef58 T vm_unmapped_area
ffff8000803e0c68 T randomize_stack_top
0x41f754: 0xcb000021   unknown     sub    x1, x1, x0
0x41f758: 0x910023e0   unknown     add    x0, sp, #0x8
0x41f75c: 0xa9027fe1   unknown     stp    x1, xzr, [sp, #0x20]
0x41f760: 0x97fffdfe   unknown     bl     0x41ef58
"""
with open("linux64k/boot/linux-image", "rb") as infile:
	indata = infile.read()
indata = bytearray(indata)
offset = 0x41f754
# mov x1, #0xfc0000000
# (64G, MACH_VM_MAX_ADDRESS_RAW on iOS)
indata[offset:offset + 4] = b"\xe1\x17\x62\xb2"
# mov x0, #0xfc0000000
# ret
offset = 0x3e0c68
indata[offset:offset + 8] = b"\xe0\x17\x62\xb2\xc0\x03\x5f\xd6"
with open("linux64k/image-patched", "wb") as outfile:
	outfile.write(indata)
