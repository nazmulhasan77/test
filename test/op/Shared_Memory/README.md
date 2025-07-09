
# Shared Memory IPC 

## Overview

In Unix/Linux systems, **Inter-Process Communication (IPC)** allows processes to communicate and share data. One of the fastest and most efficient IPC methods is **Shared Memory**, where multiple processes map the same memory segment into their address space.

This program demonstrates:
- Creating and using shared memory (`shmget`, `shmat`, `shmdt`, `shmctl`)
- Process creation using `fork`
- Communication between parent and child via shared memory

---

## Concepts Explained

### Shared Memory
- A segment of memory accessible by multiple processes.
- Allows direct memory access (unlike pipes or message queues).
- Requires explicit synchronization (not shown in this example).

### System Calls Used

| Function   | Purpose |
|------------|---------|
| `shmget()` | Create/get shared memory segment |
| `shmat()`  | Attach shared memory to process |
| `shmdt()`  | Detach shared memory |
| `shmctl()` | Control/remove shared memory segment |
| `fork()`   | Create a new child process |

---

## Step-by-Step Program Walkthrough

### Global Variable

```c
int global_var = 10;
```
Used to demonstrate that the parent and child **do not share global variables**.

---

### Initialize Variables

```c
int local_var;
int *local_addr, *global_addr;
pid_t pid;
int status;
key_t key;
int shmid;

local_var = 20;
local_addr = &local_var;
global_addr = &global_var;
```

---

### Step 1: Create Shared Memory Segment

```c
key = 1234;
shmid = shmget(key, sizeof(int), IPC_CREAT | 0666);

if (shmid == -1) {
    perror("shmget: ");
    exit(EXIT_FAILURE);
}
```

---

### Step 2: Create Child Process

```c
pid = fork();
```

---

### Child Process

#### Step 3: Attach to Shared Memory

```c
void *shm_addr = shmat(shmid, NULL, 0);
if (shm_addr == (void *) -1) {
    perror("shmat: ");
    exit(EXIT_FAILURE);
}
```

#### Step 4: Write to Shared Memory

```c
int *shared_var = (int *) shm_addr;
*shared_var = 20;
printf("Child -> Shared_Variable Put: %d\n", shared_var[0]);
```

#### Step 5: Detach Shared Memory

```c
if (shmdt(shm_addr) == -1) {
    perror("shmdt: ");
    exit(EXIT_FAILURE);
}
```

---

### Parent Process

#### Step 3: Attach to Shared Memory

```c
void *shm_addr = shmat(shmid, NULL, 0);
if (shm_addr == (void *) -1) {
    perror("shmat: ");
    exit(EXIT_FAILURE);
}
```

#### Step 4: Read from Shared Memory

```c
int *shared_var = (int *) shm_addr;
printf("Parent -> Shared_Variable Get: %d\n", shared_var[0]);
```

#### Step 5: Detach Shared Memory

```c
if (shmdt(shm_addr) == -1) {
    perror("shmdt: ");
    exit(EXIT_FAILURE);
}
```

#### Step 6: Wait for Child

```c
wait(&status);
```

#### Step 7: Remove Shared Memory Segment

```c
if (shmctl(shmid, IPC_RMID, NULL) == -1) {
    perror("shmctl: ");
    exit(EXIT_FAILURE);
}
```

---

### Final Output Example

```
Shared Memory Id: 12345
Child -> Shared_Variable Put: 20
Parent -> Shared_Variable Get: 20
Successfully terminating..
```

---

## Notes on Permissions

- If you get `Permission Denied` for `shmget`, try:
  - Removing old segment: `ipcrm -M 1234`
  - Running with `sudo`
  - Using `IPC_PRIVATE` for unique key

---

## Summary of Key Functions

| Function | Description |
|----------|-------------|
| `shmget` | Allocates a shared memory segment |
| `shmat`  | Attaches shared memory to address space |
| `shmdt`  | Detaches shared memory |
| `shmctl` | Control operations (e.g., remove segment) |
| `fork`   | Creates a new process |
| `wait`   | Synchronizes with child termination |

---
## Full Code

```c
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/shm.h>

// Global variable for demonstration
int global_var = 10;

int main() {
    int local_var;
    int *local_addr, *global_addr;
    pid_t pid;
    int status;
    key_t key;
    int shmid;

    // Initialize local variable and get address of variables
    local_var = 20;
    local_addr = &local_var;
    global_addr = &global_var;

    // --------------------------------------------
    // Step 1: Create a shared memory segment
    // --------------------------------------------
    key = 1234;  // Unique key for shared memory
    shmid = shmget(key, sizeof(int), IPC_CREAT | 0666);  // Request shared memory

    if (shmid == -1) {  // Check for error in shmget
        perror("shmget: ");
        exit(EXIT_FAILURE);
    }

    printf("Shared Memory Id: %d\n", shmid);

    // --------------------------------------------
    // Step 2: Fork a child process
    // --------------------------------------------
    pid = fork();

    if (pid == -1) {
        perror("fork: ");
        exit(EXIT_FAILURE);
    }

    // --------------------------------------------
    // Child Process
    // --------------------------------------------
    else if (pid == 0) {

        // Step 3: Attach to the shared memory
        void *shm_addr = shmat(shmid, NULL, 0);
        if (shm_addr == (void *) -1) {
            perror("shmat: ");
            exit(EXIT_FAILURE);
        }

        // Step 4: Write to shared memory
        int *shared_var = (int *) shm_addr;
        *shared_var = 20;  // Write value into shared memory
        printf("Child -> Shared_Variable Put: %d\n", shared_var[0]);

        // Step 5: Detach from shared memory
        if (shmdt(shm_addr) == -1) {
            perror("shmdt: ");
            exit(EXIT_FAILURE);
        }

        exit(EXIT_SUCCESS);  // Child exits
    }

    // --------------------------------------------
    // Parent Process
    // --------------------------------------------
    else {
        // Optional delay to ensure child writes first
        sleep(1);

        // Step 3: Attach to the shared memory
        void *shm_addr = shmat(shmid, NULL, 0);
        if (shm_addr == (void *) -1) {
            perror("shmat: ");
            exit(EXIT_FAILURE);
        }

        // Step 4: Read from shared memory
        int *shared_var = (int *) shm_addr;
        printf("Parent -> Shared_Variable Get: %d\n", shared_var[0]);

        // Step 5: Detach from shared memory
        if (shmdt(shm_addr) == -1) {
            perror("shmdt: ");
            exit(EXIT_FAILURE);
        }

        // Step 6: Wait for child to finish
        wait(&status);

        // Step 7 (Recommended): Remove shared memory
        if (shmctl(shmid, IPC_RMID, NULL) == -1) {
            perror("shmctl: ");
            exit(EXIT_FAILURE);
        }

        printf("Successfully terminating..\n");
    }

    return EXIT_SUCCESS;
}
```c