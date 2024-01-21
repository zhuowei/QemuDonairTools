./qemu-system-aarch64 -M virt -m 1G -cpu cortex-a76 -nographic -serial mon:stdio \
	-kernel "/Users/zhuowei/Documents/winprogress/donair/linux64k/image-patched" \
	-append "root=/dev/vda1 rootflags=\"iocharset=cp437\" kpti=0 nokaslr=1 init=/myinit" \
	-drive file=fat:/Users/zhuowei/Documents/winprogress/donair/rootdir6,format=raw,readonly=on,media=disk
