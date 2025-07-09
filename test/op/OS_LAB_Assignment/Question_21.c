#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdint.h>
#include <inttypes.h>  // For PRIu64

typedef struct {
    uint64_t* sequence;
    int n;
} FibData;

void* generateFibonacci(void* arg) {
    FibData* data = (FibData*)arg;
    uint64_t* fibSequence = data->sequence;
    int n = data->n;

    if (n >= 0) fibSequence[0] = 0;
    if (n >= 1) fibSequence[1] = 1;

    for (int i = 2; i <= n; i++) {
        fibSequence[i] = fibSequence[i - 1] + fibSequence[i - 2];
    }

    return NULL;
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <number of Fibonacci numbers>\n", argv[0]);
        return 1;
    }

    int n = atoi(argv[1]);
    if (n < 0) {
        fprintf(stderr, "Please enter a non-negative number.\n");
        return 1;
    }

    uint64_t* fibSequence = malloc((n + 1) * sizeof(uint64_t));
    if (!fibSequence) {
        fprintf(stderr, "Memory allocation failed.\n");
        return 1;
    }

    FibData data = {fibSequence, n};
    pthread_t fibThread;

    if (pthread_create(&fibThread, NULL, generateFibonacci, &data) != 0) {
        fprintf(stderr, "Thread creation failed.\n");
        free(fibSequence);
        return 1;
    }

    pthread_join(fibThread, NULL);

    printf("Fibonacci sequence up to term %d:\n", n);
    for (int i = 0; i <= n; i++) {
        printf("fib(%d) = %" PRIu64 "\n", i, fibSequence[i]);
    }

    free(fibSequence);
    return 0;
}
