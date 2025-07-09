#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/wait.h>

#define NUM_ITERATIONS 100000

int main() {
    // Create shared memory region for one integer (shared between processes)
    int *shared_counter = mmap(NULL, sizeof(int), PROT_READ | PROT_WRITE,
                               MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    if (shared_counter == MAP_FAILED) {
        perror("mmap failed");
        return 1;
    }

    *shared_counter = 0;  // Initialize counter

    pid_t pid = fork();

    if (pid < 0) {
        perror("fork failed");
        return 1;
    }

    if (pid == 0) {
        // Child process: increments counter
        for (int i = 0; i < NUM_ITERATIONS; i++) {
            (*shared_counter)++;  // Not synchronized!
        }
        exit(0);
    } else {
        // Parent process: also increments counter
        for (int i = 0; i < NUM_ITERATIONS; i++) {
            (*shared_counter)++;  // Not synchronized!
        }

        wait(NULL);  // Wait for child to finish

        printf("Expected counter value: %d\n", NUM_ITERATIONS * 2);
        printf("Actual counter value:   %d\n", *shared_counter);

        // Cleanup shared memory
        munmap(shared_counter, sizeof(int));
    }

    return 0;
}