#include <stdio.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include "message.h"

int main() {
    key_t key = ftok(FILE_PATH, PROJ_ID);
    if (key == -1) {
        perror("ftok failed");
        exit(1);
    }

    int msgid = msgget(key, 0666);
    if (msgid == -1) {
        perror("msgget failed");
        exit(1);
    }

    struct msg_buffer message;

    if (msgrcv(msgid, &message, sizeof(message.msg_text), 1, 0) == -1) {
        perror("msgrcv failed");
        exit(1);
    }

    printf("Receiver: Message received: %s\n", message.msg_text);

    // Clean up
    if (msgctl(msgid, IPC_RMID, NULL) == -1) {
        perror("msgctl (IPC_RMID) failed");
        exit(1);
    }

    return 0;
}
