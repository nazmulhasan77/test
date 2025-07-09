#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    int a = 10, b = 5;
    pid_t pid1, pid2, pid3;

    printf("Parent process started - PID: %d)\n", getpid());

    pid1 = fork();
    if (pid1 == 0) {
        // child_1 - Addition
        printf("Child process - PID: %d, PPID: %d) - ADDITION\n", getpid(), getppid());
        printf("Result: %d + %d = %d\n", a, b, a + b);
        exit(0);
    }

    pid2 = fork();
    if (pid2 == 0) {
        // child_3 - Multiplication
        printf("Child process - PID: %d, PPID: %d) - MULTIPLICATION\n", getpid(), getppid());
        printf("Result: %d * %d = %d\n", a, b, a * b);
        exit(0);
    }

    pid3 = fork();
    if (pid3 == 0) {
        // child_2 - Subtraction
        printf("Child process - PID: %d, PPID: %d) - SUBTRACTION\n", getpid(), getppid());
        printf("Result: %d - %d = %d\n", a, b, a - b);
        exit(0);
    }

    

    // Parent waits for all children
    wait(NULL);
    wait(NULL);
    wait(NULL);

    printf("Parent process (PID: %d) finished.\n", getpid());

    return 0;
}
