#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <sys/wait.h>

void* thread_func(void* arg) {
    printf("Thread %d: started with TID %ld in PID %d\n", *(int*)arg, pthread_self(), getpid());
    sleep(5);  // Simulate long task
    printf("Thread %d: exiting\n", *(int*)arg);
    return NULL;
}

int main() {
    pthread_t t1, t2;
    int id1 = 1, id2 = 2;

    printf("Main thread: PID = %d\n", getpid());

    pthread_create(&t1, NULL, thread_func, &id1);
    pthread_create(&t2, NULL, thread_func, &id2);

    sleep(1);  // Let threads start

    pid_t pid = fork();

    if (pid == 0) {
        // Child process
        printf("\nChild Process: PID = %d, after fork()\n", getpid());
        printf("Only calling thread is present in this process\n");

        // Uncomment this to test exec():
        // execlp("ls", "ls", "-l", NULL);

        exit(0);
    } else {
        wait(NULL);  // Wait for child
        printf("\nParent Process: PID = %d, child finished\n", getpid());
    }

    // Join threads in parent
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    return 0;
}