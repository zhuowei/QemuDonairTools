#!/bin/sh
rm initrd_stock.cpio || true
exec tar -c -C stock_rootdir6 --format newc -f initrd_stock.cpio .
