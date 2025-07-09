#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define NUM_THREADS 6

sem_t semaphore;  // Counting semaphore

void* worker(void* arg) {
    int id = *(int*)arg;

    printf("Thread %d waiting to enter critical section...\n", id);
    sem_wait(&semaphore);  // Decrement semaphore or wait if 0

    printf("Thread %d entered critical section.\n", id);
    sleep(2);  // Simulate work
    printf("Thread %d leaving critical section.\n", id);

    sem_post(&semaphore);  // Increment semaphore to release resource

    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int thread_ids[NUM_THREADS];

    // Initialize semaphore with count = 3 (3 resources available)
    sem_init(&semaphore, 0, 3);

    // Create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        thread_ids[i] = i + 1;
        pthread_create(&threads[i], NULL, worker, &thread_ids[i]);
    }

    // Join threads
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    // Destroy semaphore
    sem_destroy(&semaphore);

    return 0;
}