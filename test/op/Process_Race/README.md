# Shared Memory Data Inconsistency Example

This example demonstrates **data inconsistency** issues that can arise between a **parent process** and a **child process** when they concurrently access and modify a shared memory segment **without proper synchronization**.

> 🛑 **Note**: This code contains references to `sem_wait()` and `sem_post()`, but it does not initialize or define the semaphore `binary_sem`. This may result in a **compilation error** or **undefined behavior**. See the "Fix Required" section below.

---

## 🧠 Concept Overview

* **Shared Memory** is a method of inter-process communication (IPC) that allows multiple processes to access a common memory region.
* This example uses:

  * `ftok()` to generate a unique key for the shared memory segment.
  * `shmget()` to create the shared memory segment.
  * `shmat()` and `shmdt()` to attach/detach the segment to/from the process’s address space.
  * `fork()` to create a child process.
* Both parent and child access the shared memory concurrently and modify the same integer variable 100 times.

---

## ⚠️ Fix Required: Semaphore Not Defined

Your code uses `sem_wait(&binary_sem);` and `sem_post(&binary_sem);` but doesn't:

* Include `<semaphore.h>`
* Declare or initialize `sem_t binary_sem`

Without semaphores, this code will result in **race conditions** leading to **inconsistent updates** to the shared variable.

> ✅ **To fix this**, you should declare and initialize a POSIX unnamed semaphore in shared memory or use a named semaphore via `sem_open()`.

---

## 🛠️ How to Compile

```bash
gcc -o shared_memory_inconsistency shared_memory_shm.c -lrt -pthread
```

> 🔧 Use `-pthread` and `-lrt` if you implement POSIX semaphores.



## 🔍 What the Code Does

### 1. Generate a Key

```c
key = ftok("/home/bibrity/CSE_Courses/OS_CSE3241/Code/shared_memory_shm.c", 65);
```

Uses `ftok()` to generate a key based on a file path and project ID.

### 2. Create Shared Memory

```c
shmid = shmget(key, sizeof(key), IPC_CREAT | 0666);
```

Creates a shared memory segment of size `sizeof(key)` (Note: this should be changed to `sizeof(int)` for correct allocation).

### 3. Fork a Child Process

```c
pid = fork();
```

### 4. Attach and Modify Shared Memory

Both parent and child:

* Attach the shared memory using `shmat()`
* Perform 100 iterations where they:

  * Read the shared integer value
  * Increment (child) or decrement (parent) the value
  * Print before and after values
  * Use `sem_wait()` and `sem_post()` for synchronization (incomplete in current code)

### 5. Cleanup

* Both processes detach using `shmdt()`
* Parent deletes the shared memory using `shmctl()` with `IPC_RMID`

---

## 🧪 Expected Output (With Synchronization)

```
0. Child Process, Before updating: shared_var: 0
0. Child Process, After updating: shared_var: 1
...
0. Parent Process, Before updating: shared_var: 100
0. Parent Process, After updating: shared_var: 99
...
```

Without synchronization, the output may show **inconsistent or unexpected values**, due to concurrent access.

---

## ❗ Potential Issues

* `sizeof(key)` used in `shmget()` is incorrect. It should be `sizeof(int)` to hold an integer variable.
* `binary_sem` is not declared or initialized.
* No initialization of shared memory content (`*shmaddr = 0;`) before starting the loop.

---

## ✅ Recommended Fixes

1. **Correct memory size allocation**:

   ```c
   shmid = shmget(key, sizeof(int), IPC_CREAT | 0666);
   ```

2. **Initialize shared memory value**:

   ```c
   *shmaddr = 0; // after shmat() in parent
   ```

3. **Add semaphore initialization**:

   ```c
   #include <semaphore.h>
   sem_t *binary_sem = mmap(NULL, sizeof(sem_t), PROT_READ | PROT_WRITE,
                            MAP_SHARED | MAP_ANONYMOUS, -1, 0);
   sem_init(binary_sem, 1, 1);
   ```


## 📌 Summary

This example is a helpful starting point to understand **data inconsistency in shared memory**. However, to ensure correct behavior and prevent race conditions, synchronization primitives like **semaphores or mutexes** must be properly implemented and initialized.

---