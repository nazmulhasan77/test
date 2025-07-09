#include <stdlib.h>
#include <unistd.h> //Read
#include <string.h>
#include<stdio.h>
#include <fcntl.h>
int main(){
    char buffer[80];
    char *msg="Type a message for other Process: ";
    //Read messege from Keyboard
    write(1,msg,strlen(msg)); //Write messege to Monitor
    read(0,buffer, sizeof(buffer));

    //Open a Named Pipe in Write Mode
    int fd;
    char *named_pipe_path="/home/nazmul77//Desktop/Operating_System/IPC_NamedPipe/NamedPipe"; 
    fd=open(named_pipe_path,O_WRONLY); //Write WRONLY
        if (fd < 0){
            perror("File Open: ");
            exit(EXIT_FAILURE);
        }
    //Write user messege to Named Pipe
    write(fd,buffer,strlen(buffer));


    close(fd); // Close the Pipe
    
    exit(EXIT_SUCCESS);
}