#include <stdio.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <unistd.h>

#define FIFO_PATH "/tmp/myfifo"

int main() {
    int fd;
    char buffer[100];

    // Open the FIFO for reading
    fd = open(FIFO_PATH, O_RDONLY);
    read(fd, buffer, sizeof(buffer));
    printf("Reader: Message received: %s\n", buffer);

    close(fd);
    return 0;
}