#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <wait.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        // fork failed
        perror("fork failed");
        exit(1);
    }

    if (pid == 0) {
        // Child process
        printf("Child process (PID: %d) is exiting immediately.\n", getpid());
        exit(0); // Child terminates quickly
    } else {
        // Parent process
        printf("Parent process (PID: %d) sleeping...\n", getpid());
        printf("Child PID is %d\n", pid);

        // Sleep without calling wait() to keep child in zombie state
        sleep(30);

        // After sleeping, the parent collects child's status
        printf("Parent process calling wait() to clean up child.\n");
        wait(NULL);

        printf("Parent process exiting.\n");
    }

    return 0;
}