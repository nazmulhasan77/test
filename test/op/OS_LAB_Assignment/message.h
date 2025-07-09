// message.h
#ifndef MESSAGE_H
#define MESSAGE_H

#define MAX_TEXT 100
#define FILE_PATH "keyfile"   // Used with ftok to generate key
#define PROJ_ID 65            // Arbitrary project ID for ftok()

struct msg_buffer {
    long msg_type;
    char msg_text[MAX_TEXT];
};

#endif
