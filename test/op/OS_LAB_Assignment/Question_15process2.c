#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define SHM_NAME "/simple_shared_mem"
#define ITERATIONS 100000

int main() {
    // Open existing shared memory
    int shm_fd = shm_open(SHM_NAME, O_RDWR, 0666);
    if (shm_fd == -1) {
        perror("shm_open");
        exit(1);
    }

    // Map shared memory
    int *counter = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd, 0);
    if (counter == MAP_FAILED) {
        perror("mmap");
        exit(1);
    }

    printf("Process 2: Starting increments\n");
    for (int i = 0; i < ITERATIONS; i++) {
        (*counter)++;  // Race condition here
    }

    printf("Process 2: Done. Counter = %d\n", *counter);

    munmap(counter, sizeof(int));
    close(shm_fd);

    // Cleanup shared memory (only one process should do this, here process 2)
    if (shm_unlink(SHM_NAME) == 0) {
        printf("Process 2: Cleaned up shared memory.\n");
    } else {
        perror("shm_unlink");
    }

    return 0;
}

