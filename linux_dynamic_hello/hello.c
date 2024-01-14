#include <stdio.h>
#include <sys/wait.h>
#include <unistd.h>

static int pid;

extern char __executable_start;

int main() {
  printf("Starting up: base=%p &pid=%p\n", &__executable_start, &pid);
  int result = fork();
  pid = getpid();
  for (int i = 0; i < 10; i++) {
    printf("[pid=%d] Hello world :D %d\n", pid, i);
    usleep(1000);
  }
  if (result) {
    wait(NULL);
  }
  return 42;
}
