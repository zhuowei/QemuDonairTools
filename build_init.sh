NDKROOT="/Users/zhuowei/Library/Android/sdk/ndk/26.1.10909125"
CC="$NDKROOT/toolchains/llvm/prebuilt/darwin-x86_64/bin/clang"
$CC -target arm64-linux-android34 -nostdlib -static -Os -o rootdir/init -fuse-ld=lld -Wl,--image-base=0x400000000 -Wl,-z -Wl,max-page-size=0x10000 init.c
