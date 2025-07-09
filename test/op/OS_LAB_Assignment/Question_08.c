#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>

int main() {
    int fd[2]; // fd[0] for reading, fd[1] for writing
    pid_t pid;
    char write_msg[] = "Hello from parent!";
    char read_msg[100];

    // Create pipe
    if (pipe(fd) == -1) {
        perror("pipe failed");
        return 1;
    }

    pid = fork(); // Create child process

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }

    if (pid == 0) {
        // Child process: reads from pipe
        close(fd[1]); // Close unused write end

        read(fd[0], read_msg, sizeof(read_msg));
        printf("Child (PID: %d) received message: %s\n", getpid(), read_msg);

        close(fd[0]); // Close read end
    } else {
        // Parent process: writes to pipe
        close(fd[0]); // Close unused read end

        printf("Parent (PID: %d) sending message to child...\n", getpid());
        write(fd[1], write_msg, strlen(write_msg) + 1); // +1 to include null terminator

        close(fd[1]); // Close write end
        wait(NULL);   // Wait for child to finish
    }

    return 0;
}



