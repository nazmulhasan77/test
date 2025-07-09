#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    int n;
    printf("Enter the number of child processes: ");
    if (scanf("%d", &n) != 1 || n <= 0) {
        printf("Invalid number.\n");
        return 1;
    }

    printf("\nParent process started. PID = %d\n\n", getpid());

    pid_t pid;
    for (int i = 0; i < n; i++) {
        pid = fork();
        if (pid < 0) {
            perror("fork failed");
            return 1;
        }

        if (pid == 0) {
            // Child process
            printf("Child %d: PID = %d, Parent PID = %d\n", i + 1, getpid(), getppid());
            exit(0);  // Use exit instead of return in child
        }
        // Parent continues the loop
    }

    // Parent waits for all children
    for (int i = 0; i < n; i++) {
        wait(NULL);
    }

    printf("\nParent process (PID = %d) finished waiting for all children.\n", getpid());

    return 0;
}
