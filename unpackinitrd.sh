set -e
rm -rf rootdir6 || true
mkdir rootdir6
tar -x -C rootdir6 --exclude usr/lib/modules --exclude usr/lib/firmware -f casper/initrd
python3 patchlibc.py rootdir6/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1 rootdir6/lib/ld-linux-aarch64.so.1
python3 patchlibc.py rootdir6/lib/aarch64-linux-gnu/libc.so.6 rootdir6/lib/aarch64-linux-gnu/libc.so.6
python3 patchlibc.py rootdir6/lib/klibc-SVGXxscWf9nOevB_HZqdYeSV05I.so rootdir6/lib/klibc-SVGXxscWf9nOevB_HZqdYeSV05I.so
cp busybox/bin/busybox rootdir6/usr/bin/busybox
rm -r rootdir6/bin
cp myinit rootdir6/
cp resolv.conf rootdir6/etc/
cp libc/lib/aarch64-linux-gnu/libdl.so.2 rootdir6/usr/lib/aarch64-linux-gnu
# cp runtest_initrd rootdir6/
mkdir rootdir6/dev
mkdir rootdir6/root
mkdir rootdir6/sys
mkdir rootdir6/proc
mkdir rootdir6/tmp
mkdir rootdir6/bin
