"""
https://github.com/torvalds/linux/blob/610a9b8f49fbcf1100716370d3b5f6f884a2835a/mm/mmap.c#L1770
ffff80008037f0b0 T generic_get_unmapped_area_topdown

0x37f274: 0xcb000021   unknown     sub    x1, x1, x0
0x37f278: 0x910023e0   unknown     add    x0, sp, #0x8
0x37f27c: 0xa9027fe1   unknown     stp    x1, xzr, [sp, #0x20]
0x37f280: 0x97fffe2c   unknown     bl     0x37eb30
"""
with open("linuxasahi/kernel16k", "rb") as infile:
    indata = infile.read()
indata = bytearray(indata)
# generic_get_unmapped_area_topdown
offset = 0x37f274
# mov x1, #0xfc0000000
# (64G, MACH_VM_MAX_ADDRESS_RAW on iOS)
indata[offset:offset + 4] = b"\xe1\x17\x62\xb2"
"""
ffff800080349a58 T randomize_stack_top
"""
# randomize_stack_top
# mov x0, #0xfc0000000
# ret
offset = 0x349a58
indata[offset:offset + 8] = b"\xe0\x17\x62\xb2\xc0\x03\x5f\xd6"
"""
ffff8000804cc6a8 t load_elf_binary

ffff800080349b70 W arch_randomize_brk
ffff800080349bc8 T arch_mmap_rnd

https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.6/fs/binfmt_elf.c;l=1313;drc=9471f1f2f50282b9e8f59198ec6bb738b4ccc009

0x4cce2c: 0x54002080   unknown     b.eq   0x4cd23c
0x4cce30: 0xaa1303e0   unknown     mov    x0, x19
0x4cce34: 0x97f9f34f   unknown     bl     0x349b70 // arch_randomize_brk

0x4cd23c: 0xf000a3e0   unknown     adrp   x0, 5247
0x4cd240: 0x91288000   unknown     add    x0, x0, #0xa20
0x4cd244: 0xa9400400   unknown     ldp    x0, x1, [x0]
0x4cd248: 0xa9150660   unknown     stp    x0, x1, [x19, #0x150]
0x4cd24c: 0x17fffef9   unknown     b      0x4cce30

replace with
0: d2b55540     	mov	x0, #0xaaaa0000
4: f2c00140     	movk	x0, #0xa, lsl #32
8: aa0003e1     	mov     x1, x0
"""
offset = 0x4cd23c
indata[offset:offset + 12] = b"\x40\x55\xb5\xd2\x40\x01\xc0\xf2\xe1\x03\x00\xaa"
"""
0x4ccf64: 0x3201f3f5   unknown     mov    w21, #-0x55555556
0x4ccf68: 0xf2d55555   unknown     movk   x21, #0xaaaa, lsl #32
0x4ccf6c: 0x37b00de0   unknown     tbnz   w0, #0x16, 0x4cd128

0x4cd128: 0xf90007e2   unknown     str    x2, [sp, #0x8]
0x4cd12c: 0xb90013e3   unknown     str    w3, [sp, #0x10]
0x4cd130: 0x97f9f2a6   unknown     bl     0x349bc8

replace with
0: d2b55555     	mov     x21, #0xaaaa0000
4: f2c00155     	movk	x21, #0xa, lsl #32
"""
offset = 0x4ccf64
indata[offset:offset + 8] = b"\x55\x55\xb5\xd2\x55\x01\xc0\xf2"
# vdso
# ffff800081230000 D vdso_start
# ffff800081234000 D vdso_end
vdso_start = 0x1230000
vdso_end = 0x1234000
vdso_data = indata[vdso_start:vdso_end]
import patchlibc
patchlibc.patch(vdso_data)
indata[vdso_start:vdso_end] = vdso_data

with open("linuxasahi/image-patched", "wb") as outfile:
    outfile.write(indata)
