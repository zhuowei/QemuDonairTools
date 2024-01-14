"""
https://github.com/torvalds/linux/blob/610a9b8f49fbcf1100716370d3b5f6f884a2835a/mm/mmap.c#L1770
ffff80008041cbf0 T get_unmapped_area
ffff80008041f388 T generic_get_unmapped_area
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
# generic_get_unmapped_area_topdown
offset = 0x41f608
# mov x1, #0xfc0000000
# (64G, MACH_VM_MAX_ADDRESS_RAW on iOS)
indata[offset:offset + 4] = b"\xe1\x17\x62\xb2"
# randomize_stack_top
# mov x0, #0xfc0000000
# ret
offset = 0x3e0c68
indata[offset:offset + 8] = b"\xe0\x17\x62\xb2\xc0\x03\x5f\xd6"
# TODO(zhuowei): doesn't work; still goes out of the 64G bounds?
# load_elf_binary
# https://source.chromium.org/chromiumos/chromiumos/codesearch/+/main:src/third_party/kernel/v6.6/fs/binfmt_elf.c;l=1313;drc=9471f1f2f50282b9e8f59198ec6bb738b4ccc009
# 0x592a70: 0x54001fe0   unknown     b.eq   0x592e6c
# 0x592a74: 0xaa1303e0   unknown     mov    x0, x19
# 0x592a78: 0x97f938c8   unknown     bl     0x3e0d98 // arch_randomize_brk
#
# 0x592e6c: 0x3201f3e0   unknown     mov    w0, #-0x55555556
# 0x592e70: 0xf2d55540   unknown     movk   x0, #0xaaaa, lsl #32
# 0x592e74: 0xa9158260   unknown     stp    x0, x0, [x19, #0x158]
# 0x592e78: 0x17fffeff   unknown     b      0x592a74
# replace with
# 0: d2b55540     	mov	x0, #0xaaaa0000
# 4: f2c00140     	movk	x0, #0xa, lsl #32
offset = 0x592e6c
indata[offset:offset + 8] = b"\x40\x55\xb5\xd2\x40\x01\xc0\xf2"
# 0x592b94: 0x3201f3f5   unknown     mov    w21, #-0x55555556
# 0x592b98: 0xf2d55555   unknown     movk   x21, #0xaaaa, lsl #32
# 0x592b9c: 0x37b00de0   unknown     tbnz   w0, #0x16, 0x592d58
#
# 0x592d58: 0xf90007e2   unknown     str    x2, [sp, #0x8]
# 0x592d5c: 0xb90013e3   unknown     str    w3, [sp, #0x10]
# 0x592d60: 0x97f9382c   unknown     bl     0x3e0e10 // arch_mmap_rnd
# replace with
# 0: d2b55555     	mov     x21, #0xaaaa0000
# 4: f2c00155     	movk	x21, #0xa, lsl #32
offset = 0x592b94
indata[offset:offset + 8] = b"\x55\x55\xb5\xd2\x55\x01\xc0\xf2"
# vdso
# ffff800081590000 D vdso_start
# ffff8000815a0000 D vdso_end
vdso_start = 0x1590000
vdso_end = 0x15a0000
vdso_data = indata[vdso_start:vdso_end]
import patchlibc
patchlibc.patch(vdso_data)
indata[vdso_start:vdso_end] = vdso_data

with open("linux64k/image-patched", "wb") as outfile:
    outfile.write(indata)
