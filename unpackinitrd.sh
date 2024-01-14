set -e
rm -rf rootdir6 || true
mkdir rootdir6
tar -x -C rootdir6 --exclude usr/lib/modules --exclude usr/lib/firmware -f casper/initrd
python3 patchlibc.py rootdir6/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1 rootdir6/lib/ld-linux-aarch64.so.1
python3 patchlibc.py rootdir6/lib/aarch64-linux-gnu/libc.so.6 rootdir6/lib/aarch64-linux-gnu/libc.so.6
python3 patchlibc.py rootdir6/lib/klibc-SVGXxscWf9nOevB_HZqdYeSV05I.so rootdir6/lib/klibc-SVGXxscWf9nOevB_HZqdYeSV05I.so
