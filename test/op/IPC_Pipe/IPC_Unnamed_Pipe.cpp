//Inter Process Communication using Unnamed Pipe
//nazmulhasan77
#include <unistd.h>     // Provides access to the POSIX operating system API, including fork(), pipe(), and sleep().
#include <stdlib.h>     // Defines functions for memory allocation, process control, conversions, and others like exit().
#include <stdio.h>      // Provides input and output functions such as printf(), scanf(), etc.
#include <sys/wait.h>   // Allows the parent process to wait for its child process to terminate using wait() and waitpid().
#include <sched.h>      // Provides functions for process scheduling, like clone(), sched_setaffinity(), etc.
#include <string.h>     // Defines string handling functions such as strcpy(), strlen(), strcmp(), etc.


int main(){
    pid_t pid;
    int processor_no;
    int pipe_fd[2]; //Pipe Descriptor
    char buffer[80];

    //Create an unnamed pipe
    printf("Pipe Descriptor: %d ,%d\n",pipe_fd[0],pipe_fd[1]);
    pipe(pipe_fd);
    printf("Pipe Descriptor: %d ,%d\n",pipe_fd[0],pipe_fd[1]); // 3 read, 4 write
   
   /* File Descriptor:
    0: standard input(stdin/keyboard)
    1: standard output(stdin/monitor)
    2: standard error(stderr)
   */

    //create child
    pid=fork();
    if(pid<0){
        perror("Fork");
        exit(EXIT_FAILURE);
        
    }
    else if(pid == 0) {
        //child process
        pid=getpid();
        processor_no=sched_getcpu();
        printf("Child PID: %d, Processor No: %d \n",pid,processor_no);
        const char *msg="Type a messege to parent: ";
        //write child messege to the pipe
        write(1,msg,strlen(msg));
        read(0,buffer,sizeof(buffer));
        close(pipe_fd[0]);
        write(pipe_fd[1],buffer,strlen(buffer));
        close(pipe_fd[1]);

    }

    else{
        //Parent Process
        pid=getpid();
        processor_no=sched_getcpu();
        printf("Parent PID: %d, Processor No: %d \n",pid,processor_no);

        close(pipe_fd[1]);
        //Read child messege from the pipe
        read(pipe_fd[0],buffer,sizeof(buffer));
        close(pipe_fd[0]);
        //Write child messege to the monitor
        write(1,buffer,strlen(buffer));

        //wait for the terminitation of Child Process in order to avoid making them orphan process
        int status;
        wait(&status); 
    }


    exit(EXIT_SUCCESS);
}