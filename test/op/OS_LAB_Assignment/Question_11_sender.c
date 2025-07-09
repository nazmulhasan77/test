#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include "message.h"

int main() {
    key_t key = ftok(FILE_PATH, PROJ_ID);
    if (key == -1) {
        perror("ftok failed");
        exit(1);
    }

    int msgid = msgget(key, IPC_CREAT | 0666);
    if (msgid == -1) {
        perror("msgget failed");
        exit(1);
    }

    struct msg_buffer message;
    message.msg_type = 1;

    printf("Sender: Enter a message: ");
    fgets(message.msg_text, MAX_TEXT, stdin);
    message.msg_text[strcspn(message.msg_text, "\n")] = '\0';  // Remove newline

    if (msgsnd(msgid, &message, sizeof(message.msg_text), 0) == -1) {
        perror("msgsnd failed");
        exit(1);
    }

    printf("Sender: Message sent successfully.\n");

    return 0;
}
