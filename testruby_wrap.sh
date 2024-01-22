#!/bin/sh
cp ruby-3.1.2.tar.gz /tmp
cd /tmp
cat ruby-3.1.2.tar.gz >/dev/null
busybox time /testruby.sh
