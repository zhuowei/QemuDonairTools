#include <stdint.h>
#include <sys/types.h>

// for donair, syscalls are patched to brk
#define SYSCALL "brk #0\n"
// normally syscalls are svc
//#define SYSCALL "svc #0\n"
__attribute((naked)) ssize_t write(int fd, void* data, size_t size) {
  asm volatile("mov x8, #64\n" SYSCALL "ret");
}

__attribute((naked)) void exit(int code) {
  asm volatile("mov x8, #93\n" SYSCALL "ret");
}

void _start() {
  static const char hello[] = "Hello from zhuowei's init!\n";
  for (int i = 0; i < 10; i++) {
    write(1, (void*)hello, sizeof(hello) - 1);
  }
  exit(42);
}
