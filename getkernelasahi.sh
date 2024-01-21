#!/bin/bash
set -e
rm -r kernel-16k-core-6.6.3-411.asahi.fc39.aarch64.rpm linuxasahi || true
wget https://download.copr.fedorainfracloud.org/results/@asahi/kernel/fedora-39-aarch64/06769478-kernel/kernel-16k-core-6.6.3-411.asahi.fc39.aarch64.rpm
mkdir linuxasahi
cd linuxasahi
tar xf ../kernel-16k-core-6.6.3-411.asahi.fc39.aarch64.rpm
dd if=lib/modules/6.6.3-411.asahi.fc39.aarch64+16k/vmlinuz of=kernel16k.gz bs=48264 skip=1
gunzip kernel16k.gz
