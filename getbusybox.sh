#!/bin/sh
set -e
rm busybox_1.30.1-7ubuntu3_arm64.deb || true
wget https://mirrors.mit.edu/ubuntu-ports/pool/universe/b/busybox/busybox_1.30.1-7ubuntu3_arm64.deb
rm -r busybox || true
mkdir busybox
cd busybox
tar xf ../busybox_1.30.1-7ubuntu3_arm64.deb
tar xf data.tar.zst
