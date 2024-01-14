#!/bin/bash
set -e
rm -rf rootdir5
mkdir rootdir5
cp -r libc/lib rootdir5/lib
python3 patchlibc.py libc/lib/aarch64-linux-gnu/ld-linux-aarch64.so.1 rootdir5/lib/ld-linux-aarch64.so.1
python3 patchlibc.py libc/lib/aarch64-linux-gnu/libc.so.6 rootdir5/lib/aarch64-linux-gnu/libc.so.6
mkdir rootdir5/sbin
cp -r linux_dynamic_hello/hello_dynamic rootdir5/sbin/init
