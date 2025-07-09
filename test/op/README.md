
# 💻 Inter-Process Communication and Multithreading in C/C++

This repository demonstrates various methods of Inter-Process Communication (IPC) and multithreading in C/C++. It includes real-world examples of shared memory, pipes (named and unnamed), thread creation, and synchronization using mutexes.

---

## 📚 Theory Overview



### 1. 🔍 Process Identification
Understanding parent-child relationship and process IDs using:
- `getpid()`, `getppid()`

- **Example File:** `ProcessID_Showing.cpp`
---

### 2. 🏷️ Named Pipes (FIFOs)
Named pipes enable communication between unrelated processes via the filesystem.

- **System Calls:**
  - `mkfifo()`, `open()`, `read()`, `write()`, `unlink()`

- **Documentation:** `IPC_NamedPipe/NamedPipe_Documentation.md`

---

### 2. 🚰 Unnamed Pipes
Unnamed pipes are a unidirectional communication method used between related processes (typically parent and child). They operate in memory and disappear once the process terminates.

- **System Calls:**
  - `pipe()`, `fork()`, `read()`, `write()`

- **Example File:** `IPC_Unnamed_Pipe.cpp`
---

### 3. 🛡️ Thread Synchronization with Mutex
To prevent race conditions, mutexes (mutual exclusion locks) are used to protect critical sections.

- **Functions:**
  - `pthread_mutex_init()`, `pthread_mutex_lock()`, `pthread_mutex_unlock()`, `pthread_mutex_destroy()`
- **Example File:** `ThreadRaceMutex.cpp`

---

### 4. 🧵 Threads and Race Conditions
Threads share the same memory space. When multiple threads modify shared data simultaneously without coordination, it can lead to **race conditions**.

- **Thread Functions:**
  - `pthread_create()`, `pthread_join()`, `pthread_exit()`
- **Race Conditions Example:** `Thread.c`
---
### 5. 🧠 Shared Memory
Shared memory allows multiple processes to access the same region of memory. It is the fastest IPC mechanism because processes communicate directly without kernel involvement after memory is mapped.

- **System Calls:**
  - `shmget()`: Create or get shared memory segment.
  - `shmat()`: Attach to shared memory.
  - `shmdt()`: Detach from shared memory.
  - `shmctl()`: Control operations (e.g., removal).

- **Example File:** `Shared_Memory/SharedMemoryCleanCode.c`
- **Documentation:** `Shared_Memory/SharedMemoryDocumentation.md`

---








## 🗂️ Repository Structure

```
IPC_And_Threads/
├── Shared_Memory/
│   ├── SharedMemoryCleanCode.c
│   └── SharedMemoryDocumentation.md
├── IPC_NamedPipe/
│   └── NamedPipe_Documentation.md
├── IPC_Unnamed_Pipe.cpp
├── Multithreading.cpp
├── Thread.c
├── ThreadRaceMutex.cpp
├── ProcessID_Showing.cpp
├── .gitignore
└── README.md
```

---

## 🛠️ How to Compile and Run

### Compile
```bash
gcc Shared_Memory/SharedMemoryCleanCode.c -o shared_mem
./shared_mem
```

```bash
g++ IPC_Unnamed_Pipe.cpp -o unnamed_pipe
./unnamed_pipe
```

### Clean up shared memory (if needed)
```bash
ipcrm -M 1234  # remove by key
ipcs -m        # view shared memory segments
```

---

## 🧑‍💻 Author

**Nazmul Hasan**

---

## 📜 License

This project is licensed under the MIT License.