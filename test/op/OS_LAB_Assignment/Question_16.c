#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

#define NUM_THREADS 10
#define NUM_ITERATIONS 100000

int counter = 0;           // Shared global variable
pthread_mutex_t mutex;     // Mutex to protect counter

void* increment_counter(void* arg) {
    for (int i = 0; i < NUM_ITERATIONS; i++) {
        // Lock mutex before modifying shared data
        pthread_mutex_lock(&mutex);

        counter++;  // Critical section

        // Unlock mutex after modification
        pthread_mutex_unlock(&mutex);
    }
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];

    // Initialize mutex
    if (pthread_mutex_init(&mutex, NULL) != 0) {
        perror("Mutex init failed");
        return 1;
    }

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        if (pthread_create(&threads[i], NULL, increment_counter, NULL) != 0) {
            perror("Failed to create thread");
            return 1;
        }
    }

    // Join threads
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Expected counter value: %d\n", NUM_THREADS * NUM_ITERATIONS);
    printf("Actual counter value:   %d\n", counter);

    // Destroy mutex
    pthread_mutex_destroy(&mutex);

    return 0;
}

