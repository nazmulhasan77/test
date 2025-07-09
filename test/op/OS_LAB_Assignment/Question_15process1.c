#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define SHM_NAME "/simple_shared_mem"
#define ITERATIONS 100000

int main() {
    // Open or create shared memory
    int shm_fd = shm_open(SHM_NAME, O_RDWR | O_CREAT, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(1);
    }

    // Set size
    if (ftruncate(shm_fd, sizeof(int)) == -1) {
        perror("ftruncate");
        exit(1);
    }

    // Map shared memory
    int *counter = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (counter == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    // Initialize counter
    *counter = 0;
    printf("Process 1: Initialized counter to 0\n");

    sleep(1);  // Give time for process 2 to start

    printf("Process 1: Starting increments\n");
    for (int i = 0; i < ITERATIONS; i++) {
        (*counter)++;  // Race condition here
    }

    printf("Process 1: Done. Counter = %d\n", *counter);

    munmap(counter, sizeof(int));
    close(shm_fd);

    return 0;
}

