#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Global variables to store results
int average = 0;
int minimum = 0;
int maximum = 0;

int *numbers = NULL; // Array of input numbers
int count = 0;       // Number of input numbers

// Thread function to compute average
void* compute_average(void* arg) {
    int sum = 0;
    for (int i = 0; i < count; i++) {
        sum += numbers[i];
    }
    average = sum / count;
    pthread_exit(0);
}

// Thread function to compute minimum
void* compute_minimum(void* arg) {
    int min = numbers[0];
    for (int i = 1; i < count; i++) {
        if (numbers[i] < min)
            min = numbers[i];
    }
    minimum = min;
    pthread_exit(0);
}

// Thread function to compute maximum
void* compute_maximum(void* arg) {
    int max = numbers[0];
    for (int i = 1; i < count; i++) {
        if (numbers[i] > max)
            max = numbers[i];
    }
    maximum = max;
    pthread_exit(0);
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <list of integers>\n", argv[0]);
        return 1;
    }

    count = argc - 1;
    numbers = (int*)malloc(count * sizeof(int));

    for (int i = 0; i < count; i++) {
        numbers[i] = atoi(argv[i + 1]);
    }

    // Thread identifiers
    pthread_t tid_avg, tid_min, tid_max;

    // Create threads
    pthread_create(&tid_avg, NULL, compute_average, NULL);
    pthread_create(&tid_min, NULL, compute_minimum, NULL);
    pthread_create(&tid_max, NULL, compute_maximum, NULL);

    // Wait for threads to complete
    pthread_join(tid_avg, NULL);
    pthread_join(tid_min, NULL);
    pthread_join(tid_max, NULL);

    // Display results
    printf("A. The average value is %d\n", average);
    printf("B. The minimum value is %d\n", minimum);
    printf("C. The maximum value is %d\n", maximum);

    // Cleanup
    free(numbers);

    return 0;
}

