# Inter-Process Communication using System V Message Queue in C

This project demonstrates how to implement **inter-process communication (IPC)** using **System V message queues** in C. It involves communication between a **parent** and a **child** process created using `fork()`.

## 🛠️ How It Works

This program uses a **System V message queue** to allow a child process to send a message to its parent process.

---

## 📜 Step-by-Step Explanation

### 1. Define the Message Structure

```c
struct msg_queue {
    long type;         // Must be > 0
    char text[80];     // Message content
};
```

* `type`: a long value that defines the type of message.
* `text`: an 80-character buffer to hold the message text.

### 2. Create a Message Queue

```c
key_t key = 1234;
int msqid = msgget(key, 0666 | IPC_CREAT);
```

* `key`: Unique identifier for the queue.
* `0666`: Permissions (read/write for all).
* `IPC_CREAT`: Create queue if it doesn’t already exist.

### 3. Create a Child Process

```c
pid_t pid = fork();
```

* `fork()` creates a child process.
* Both parent and child continue executing after this point.

### 4. Child Process Sends a Message

```c
if (pid == 0) {
    msg.type = 1;
    strcpy(msg.text, "Hello, Parent\n");
    msgsnd(msqid, &msg, sizeof(msg.text), 0);
}
```

* Only the **child** executes this block.
* Sets message type to 1.
* Uses `msgsnd()` to send the message.

### 5. Parent Process Receives the Message

```c
else {
    wait(&status); // Wait for child
    msgrcv(msqid, &msg, sizeof(msg.text), 1, 0);
    printf("Received message: %s", msg.text);
    msgctl(msqid, IPC_RMID, NULL); // Remove queue
}
```

* Only the **parent** executes this block.
* Waits for the child to finish sending.
* Receives message of type 1 using `msgrcv()`.
* Deletes the message queue using `msgctl()`.

---

## 🔃 Flow Summary

```
PARENT       CHILD
  |           |
  |----fork-->|
  |           |---- msgsnd() --> Message Queue
  |<-- wait --|
  |---- msgrcv() reads from Queue
  |           |
```

---

## ▶️ Compilation and Execution

### Compile

```bash
gcc Message_Queue.c -o message_queue
```

### Run

```bash
./message_queue
```

### Expected Output

```
Parent
Child
Received message: Hello, Parent
```

---

## 🧹 Cleanup

The program removes the message queue using:

```c
msgctl(msqid, IPC_RMID, NULL);
```

This ensures no dangling message queues remain.

---

## 🧠 Notes

* `msg.type` **must be greater than 0**.
* `msgsnd()` and `msgrcv()` operate only on the `text` portion, not `type`.
* Synchronization is handled via `wait()` to avoid race conditions.