#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/msg.h>
#include <stdio.h>
#include <string.h>

struct msg_queue {
    long type;         // Must be long and > 0
    char text[80];
};

int main() {
    struct msg_queue msg;
    key_t key = 1234;

    // Create the message queue
    int msqid = msgget(key, 0666 | IPC_CREAT);
    if (msqid == -1) {
        perror("msgget");
        exit(EXIT_FAILURE);
    }

    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        printf("Child\n");
        msg.type = 1;  // Must be > 0
        strcpy(msg.text, "Hello, Parent\n");

        if (msgsnd(msqid, &msg, sizeof(msg.text), 0) == -1) {
            perror("msgsnd");
            exit(EXIT_FAILURE);
        }
    } else {
        // Parent process
        printf("Parent\n");
        int status;
        wait(&status);  // Wait for child to send

        if (msgrcv(msqid, &msg, sizeof(msg.text), 1, 0) == -1) {
            perror("msgrcv");
            exit(EXIT_FAILURE);
        }

        printf("Received message: %s", msg.text);

        // Cleanup message queue
        msgctl(msqid, IPC_RMID, NULL);
    }

    return 0;
}
