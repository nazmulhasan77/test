#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>

#define FIFO_PATH "/tmp/myfifo"

int main() {
    pid_t pid;
    char *message = "Hello from parent process!";
    char buffer[100];

    // Create named pipe (FIFO)
    if (mkfifo(FIFO_PATH, 0666) == -1) {
        perror("mkfifo");
        // Not exiting here in case it already exists
    }

    pid = fork();

    if (pid < 0) {
        perror("fork");
        return 1;
    }

    if (pid == 0) {
        // Child Process: Reads from the FIFO
        int fd_read = open(FIFO_PATH, O_RDONLY);
        if (fd_read < 0) {
            perror("Child: open for read failed");
            exit(1);
        }

        read(fd_read, buffer, sizeof(buffer));
        printf("Child (PID %d) received: %s\n", getpid(), buffer);
        close(fd_read);
    } else {
        // Parent Process: Writes to the FIFO
        int fd_write = open(FIFO_PATH, O_WRONLY);
        if (fd_write < 0) {
            perror("Parent: open for write failed");
            exit(1);
        }

        write(fd_write, message, strlen(message) + 1); // +1 to include null terminator
        printf("Parent (PID %d) sent message to child.\n", getpid());
        close(fd_write);

        wait(NULL); // Wait for child to finish

        // Clean up
        unlink(FIFO_PATH);
    }

    return 0;
}

