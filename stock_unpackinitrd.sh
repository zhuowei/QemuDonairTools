set -e
rm -rf stock_rootdir6 || true
mkdir stock_rootdir6
tar -x -C stock_rootdir6 --exclude usr/lib/modules --exclude usr/lib/firmware -f casper/initrd
cp busybox/bin/busybox stock_rootdir6/usr/bin/busybox
rm -r stock_rootdir6/bin
cp myinit stock_rootdir6/
cp resolv.conf stock_rootdir6/etc/
cp libc/lib/aarch64-linux-gnu/libdl.so.2 stock_rootdir6/usr/lib/aarch64-linux-gnu
# cp runtest_initrd rootdir6/
mkdir stock_rootdir6/dev
mkdir stock_rootdir6/root
mkdir stock_rootdir6/sys
mkdir stock_rootdir6/proc
mkdir stock_rootdir6/tmp
mkdir stock_rootdir6/bin
