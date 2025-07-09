#include <stdlib.h>
#include <unistd.h> // read
#include <string.h>
#include <stdio.h>
#include <fcntl.h>

int main() {
    char buffer[80];
    int fd;
    char *named_pipe_path = "/home/nazmul77/Desktop/Operating_System/IPC_NamedPipe/NamedPipe"; 

    char *msg="Message from other Process: ";
    //Read message from Keyboard
    write(1,msg,strlen(msg)); //Write messege to Monitor

    // Open in Read mode
    fd = open(named_pipe_path, O_RDONLY);
    if (fd < 0) {
        perror("File Open: ");
        exit(EXIT_FAILURE);
    }

    // Read data from pipe
    read(fd, buffer, sizeof(buffer));
    //buffer[n] = '\0'; // Null terminate
    //printf("Received message: %s\n", buffer);
    //Write message to monitor
    write(1,buffer,strlen(buffer));
    

    close(fd);
    return 0;
}
