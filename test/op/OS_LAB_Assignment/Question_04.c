#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid1, pid2, pid3;

    printf("Parent_process started. PID = %d\n\n", getpid());

    pid1 = fork();
    if (pid1 == 0) {
        // Child 1
        printf("I am child_1. PID = %d, Parent PID = %d\n", getpid(), getppid());
        return 0;
    }

    pid2 = fork();
    if (pid2 == 0) {
        // Child 2
        printf("I am child_2. PID = %d, Parent PID = %d\n", getpid(), getppid());
        return 0;
    }

    pid3 = fork();
    if (pid3 == 0) {
        // Child 3
        printf("I am child_3. PID = %d, Parent PID = %d\n", getpid(), getppid());
        return 0;
    }

    // Parent waits for all children
    wait(NULL);
    wait(NULL);
    wait(NULL);

    printf("\nParent_process (PID = %d) finished waiting for all children.\n", getpid());

    return 0;
}

