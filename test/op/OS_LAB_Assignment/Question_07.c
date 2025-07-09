#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int global_var = 100; // Global variable

int main() {
    int local_var = 200; // Local variable

    printf("Before fork:\n");
    printf("Parent (PID: %d) - global_var = %d, local_var = %d\n\n", getpid(), global_var, local_var);

    pid_t pid = fork(); // Create child process

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }

    if (pid == 0) {
        // Child process
        printf("Child Process (PID: %d) started...\n", getpid());

        global_var += 50;  // Change global variable
        local_var += 50;   // Change local variable

        printf("Child (PID: %d) - global_var = %d, local_var = %d\n", getpid(), global_var, local_var);
        return 0;
    } else {
        // Parent process
        wait(NULL); // Wait for child to finish
        printf("\nParent Process (PID: %d) resumed after child.\n", getpid());
        printf("Parent (PID: %d) - global_var = %d, local_var = %d\n", getpid(), global_var, local_var);
    }

    return 0;
}

