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
  static const char hello[] = "Hello from zhuowei's init! 0\n";
  char hello2[sizeof(hello)];
  __builtin_memcpy(hello2, hello, sizeof(hello));
  for (int i = 0; i < 10; i++) {
    hello2[sizeof(hello2) - 3] = '0' + i;
    write(1, (void*)hello2, sizeof(hello2) - 1);
  }
  exit(42);
}
