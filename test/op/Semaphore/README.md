
# 🧵 Parent-Child Synchronization using Semaphores and Shared Memory in C

This project demonstrates inter-process communication and synchronization using **System V Shared Memory** and **POSIX Binary Semaphores** in C.

Two versions of the same logic are implemented:

- 🗂️ **Named Semaphore**: Synchronization via a POSIX named binary semaphore.
- 📎 **Unnamed Semaphore**: Synchronization via a POSIX unnamed binary semaphore.

Each example shows how a parent and a child process safely update a **shared integer variable** 100 times without creating data races.

---


## 🧠 Key Concepts

- **Semaphores**: Synchronization primitives to enforce mutual exclusion.
- **Binary Semaphore**: A semaphore that holds either `0` or `1` — essentially a lock.
- **Shared Memory**: Fastest IPC mechanism that allows two or more processes to access a common memory region.
- **Parent and Child Process**: Created using `fork()`, share the memory but must synchronize access.

---

## 🧰 Requirements

- GCC or Clang compiler
- Linux operating system (for POSIX and System V IPC support)
- Sufficient permissions to create shared memory segments and semaphores

---

## ⚙️ How to Compile

```bash
# Compile the named semaphore example
gcc Named_Semaphore.c -o named -pthread

# Compile the unnamed semaphore example
gcc Unnnamed_semaphore.c -o unnamed -pthread
````

---

## 🔄 Execution Flow (Both Versions)

1. Generate a shared memory key using `ftok()`.
2. Allocate shared memory using `shmget()`.
3. Initialize a semaphore (named or unnamed).
4. Create a child process using `fork()`.
5. Both processes:

   * Attach shared memory using `shmat()`
   * Use `sem_wait()` before accessing the shared variable
   * Modify the shared variable (Child increments, Parent decrements)
   * Print before and after values
   * Use `sem_post()` to release the lock
6. Parent waits for child to finish using `wait(NULL)`
7. Detach shared memory using `shmdt()`
8. Destroy shared memory using `shmctl()`
9. Clean up the semaphore (`sem_unlink()` or `sem_destroy()`)

---

## 🔐 Named Semaphore Version

### ✅ File: `named_semaphore.c`

### 📌 Highlights

* Uses `sem_open()` to create a named semaphore `/binary_semaphore`
* This semaphore is **visible system-wide** (via `/dev/shm/sem.*`)
* Safe for synchronization across unrelated processes

### 🧾 Semaphore Details

```c
sem_t *binary_sem;
binary_sem = sem_open("/binary_semaphore", O_CREAT);
```

* The semaphore persists across runs unless explicitly removed using `sem_unlink()`
* Useful when you want multiple programs to synchronize using a common name

### 🧠 Shared Memory Logic

```c
key_t key = ftok("shared_memory_shm.c", 65);
int shmid = shmget(key, sizeof(int), IPC_CREAT | 0666);
```

* `ftok()` turns a file path + integer into a consistent key
* `shmget()` creates a shared segment to store one `int`

### 🧵 Process Behavior

* **Child Process:**

  * Increments the shared variable 100 times
* **Parent Process:**

  * Decrements the shared variable 100 times
* **Result:**

  * If perfectly synchronized, final value should be 0

### 🧹 Cleanup

```c
sem_unlink("/binary_semaphore"); // Destroy named semaphore
shmdt(shmaddr);                  // Detach memory
shmctl(shmid, IPC_RMID, NULL);  // Remove memory
```

---

## 📎 Unnamed Semaphore Version

### ✅ File: `unnamed_semaphore.c`

### 📌 Highlights

* Uses `sem_init()` to initialize an unnamed semaphore in the process's memory space
* Only accessible by related processes (e.g., after `fork()`)
* No system-wide name or persistence

### ❗ Important Note

> Although the semaphore is initialized with `pshared = 1`, it resides in the process's local stack, not in shared memory. Technically, this does **not guarantee correct inter-process synchronization**.

For correctness, the semaphore must reside in **shared memory**. This version works *empirically* on Linux because `fork()` copies memory and some platforms allow synchronization to work temporarily—but it's **non-portable** and **not POSIX-compliant**.

### 🧾 Semaphore Initialization

```c
sem_t binary_sem;
sem_init(&binary_sem, 1, 1); // pshared=1 allows sharing between processes
```

### 🧹 Cleanup

```c
sem_destroy(&binary_sem); // Only the parent calls this
```

---

## 🔑 Shared Memory Key Generation

```c
key_t key = ftok("shared_memory_shm.c", 65);
```

* **Path:** Should be an existing file
* **ID:** Any small integer (usually ≤ 255)
* **Result:** Same file + ID = same key (if reused)

---

## 🧼 Memory Cleanup

Always ensure memory and semaphores are destroyed properly:

### For Named Semaphores:

```bash
# View all named semaphores
ls /dev/shm/sem.*

# Remove manually (if not unlinked)
sem_unlink("/binary_semaphore");
```

### For Shared Memory:

```bash
# List shared memory
ipcs -m

# Remove manually
ipcrm -m <shmid>
```

---

## ⚖️ Comparison

| Feature                 | Named Semaphore           | Unnamed Semaphore            |
| ----------------------- | ------------------------- | ---------------------------- |
| Lifetime                | Persistent until unlinked | Tied to process lifetime     |
| Visibility              | System-wide               | Only among related processes |
| Initialization Function | `sem_open()`              | `sem_init()`                 |
| Cleanup                 | `sem_unlink()`            | `sem_destroy()`              |
| Usability in shared mem | ❌ No need                 | ✅ Must be in shared memory   |

---

## ⚠️ Limitations

### Named Version

* Slower due to file system interactions (in `/dev/shm`)
* Must handle `sem_unlink` carefully to avoid semaphore leaks

### Unnamed Version

* Incorrect placement of semaphore (not in shared memory)
* Undefined behavior on systems that don't allow memory sharing like this

---

## 🚀 Improvements

* ✅ Place the unnamed `sem_t` in shared memory using `mmap` or `shmget`
* ✅ Add `sleep()` calls for artificial delays to visualize race conditions
* ✅ Extend the project to use multiple semaphores or threads
* ✅ Use `ftok("/tmp", 'A')` for a more portable key

---
