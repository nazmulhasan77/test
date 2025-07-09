#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

#define MAX_TEXT 100

// Define the message buffer structure
struct msg_buffer {
    long msg_type;
    char msg_text[MAX_TEXT];
};

int main() {
    key_t key;
    int msgid;
    struct msg_buffer message;

    // Generate a unique key (can be any fixed value for related processes)
    key = ftok(".", 65);

    // Create a message queue
    msgid = msgget(key, 0666 | IPC_CREAT);
    if (msgid == -1) {
        perror("msgget failed");
        exit(1);
    }

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }

    if (pid == 0) {
        // Child process: receives message
        printf("Child (PID %d) waiting for message...\n", getpid());
        msgrcv(msgid, &message, sizeof(message.msg_text), 1, 0);
        printf("Child (PID %d) received message: %s\n", getpid(), message.msg_text);
    } else {
        // Parent process: sends message
        strcpy(message.msg_text, "Hello from parent process!");
        message.msg_type = 1;

        sleep(1); // Delay to ensure child is ready
        msgsnd(msgid, &message, sizeof(message.msg_text), 0);
        printf("Parent (PID %d) sent message to child.\n", getpid());

        wait(NULL); // Wait for child to finish

        // Remove the message queue
        msgctl(msgid, IPC_RMID, NULL);
    }

    return 0;
}

