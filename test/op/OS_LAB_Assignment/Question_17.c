#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <semaphore.h>
#include <string.h>
#include <sys/stat.h>

#define SHM_NAME "/shm_counter"
#define SEM_NAME "/sem_counter"
#define ITERATIONS 100000

int main() {
    // Open or create shared memory
    int shm_fd = shm_open(SHM_NAME, O_CREAT | O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(EXIT_FAILURE);
    }

    // Resize shared memory
    if (ftruncate(shm_fd, sizeof(int)) == -1) {
        perror("ftruncate");
        exit(EXIT_FAILURE);
    }

    // Map shared memory
    int *counter = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (counter == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }

    // Open or create named semaphore
    sem_t *sem = sem_open(SEM_NAME, O_CREAT, 0666, 1);
    if (sem == SEM_FAILED) {
        perror("sem_open");
        exit(EXIT_FAILURE);
    }

    // Initialize counter to 0 only if this process created shared memory (optional)
    // Use fstat or another mechanism if needed; here we skip initialization for simplicity

    printf("Process %d started incrementing...\n", getpid());

    for (int i = 0; i < ITERATIONS; i++) {
        sem_wait(sem);       // Lock (wait)
        (*counter)++;        // Critical section
        sem_post(sem);       // Unlock (signal)
    }

    printf("Process %d done. Counter = %d\n", getpid(), *counter);

    // Cleanup (don't unlink here if you want to run multiple processes repeatedly)
    munmap(counter, sizeof(int));
    close(shm_fd);
    sem_close(sem);

    return 0;
}