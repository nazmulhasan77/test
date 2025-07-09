#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid = fork();

    if (pid < 0) {
        // Fork failed
        perror("fork failed");
        return 1;
    }

    if (pid > 0) {
        // Parent process
        printf("Parent process (PID: %d) exiting...\n", getpid());
        // Parent exits immediately, child becomes orphan
        return 0;
    } else {
        // Child process
        printf("Child process started with PID: %d, parent PID: %d\n", getpid(), getppid());

        // Sleep to allow parent to exit and become orphan
        sleep(5);

        // After parent has exited, PPID should change to 1 (init)
        printf("Child process after orphaning - PID: %d, new parent PID: %d\n", getpid(), getppid());

        // Keep running or do some work
        sleep(5);

        printf("Child process exiting...\n");
    }

    return 0;
}

