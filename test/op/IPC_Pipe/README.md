
# Named Pipe (FIFO) in Linux - Documentation

## 📄 What is a Named Pipe (FIFO)?
A **Named Pipe** (also called **FIFO**) is a special type of file that allows **two unrelated processes** to communicate with each other using the filesystem.

- FIFO = **First In First Out**.
- Unlike anonymous pipes, named pipes are visible in the filesystem and can be opened by unrelated processes.

---

## 🛠️ How to Create a Named Pipe

### 1. Using Command Line
```bash
mkfifo [pipe_name]
```

This will create a named pipe .

---
## 🔄 Opening a Named Pipe in C

### Open for Writing
```c
int fd = open("/path/to/pipe", O_WRONLY);
```

### Open for Reading
```c
int fd = open("/path/to/pipe", O_RDONLY);
```

> ❗ **Important:**  
> - `open()` will **block** (wait forever) unless both a reader and a writer are present.  
> - To avoid blocking, use the `O_NONBLOCK` flag.

---

## ✍ Writing to and Reading from the Pipe

### Writer Program Example
```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <fcntl.h>

int main() {
    char buffer[80];
    char *msg = "Type a message for the other process: ";
    write(1, msg, strlen(msg));
    read(0, buffer, sizeof(buffer));

    int fd = open("/home/nazmul77/Desktop/Operating_System/NamedPipe/NamedPipe", O_WRONLY);
    if (fd < 0) {
        perror("File Open:");
        exit(EXIT_FAILURE);
    }

    write(fd, buffer, strlen(buffer));
    close(fd);
    return 0;
}
```

---

### Reader Program Example
```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdio.h>
#include <fcntl.h>

int main() {
    char buffer[80];
    int fd = open("/home/nazmul77/Desktop/Operating_System/NamedPipe/NamedPipe", O_RDONLY);
    if (fd < 0) {
        perror("File Open:");
        exit(EXIT_FAILURE);
    }

    int n = read(fd, buffer, sizeof(buffer));
    buffer[n] = '\0';
    printf("Received message: %s\n", buffer);
    close(fd);
    return 0;
}
```

---

## 🗑️ Deleting a Named Pipe

### Using Command Line
```bash
rm [pipe_name]
```

This will remove the named pipe from the filesystem.

---

## ⚡ Tips
- Always open the reader before opening the writer if you don't want `open()` to block.
- Use `ls -l` to check that the pipe was created (you will see `p` at the beginning of the permissions).

Example:
```bash
ls -l
```
Output:
```
prw-r--r-- 1 user group 0 Apr 27 10:00 NamedPipe
```

---

# 🚀 Conclusion
Named pipes are a simple and powerful IPC (Inter-Process Communication) method on Linux.  
Always make sure that both a reader and a writer are available to avoid blocking issues!
