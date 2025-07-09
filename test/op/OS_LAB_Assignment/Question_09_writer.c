#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>
#include <string.h>

#define FIFO_PATH "/tmp/myfifo"

int main() {
    int fd;
    char *message = "Hello from writer process!";

    // Create the named pipe (FIFO)
    mkfifo(FIFO_PATH, 0666);  // Ignore error if already exists

    // Open the FIFO for writing
    fd = open(FIFO_PATH, O_WRONLY);
    write(fd, message, strlen(message) + 1);
    printf("Writer: Message sent to FIFO.\n");

    close(fd);
    return 0;
}