#define _GNU_SOURCE
#include <stdio.h>
#include <pthread.h>   // Required for pthread
#include <sched.h>   // Required for sched_getcpu
#include <unistd.h>  // For usleep
int x=0;
void *addition(void *arg){
    for(int i=0 ;i<100;i++){
    int processor_no;
    processor_no = sched_getcpu();
    x++;
    printf("Addition Thread, Processor NO: %d,x: %d\n", processor_no,x);
    //usleep(10000);
    }
}

void *subtraction(void *arg){
    for(int i=0 ;i<100;i++){
    int processor_no;
    processor_no = sched_getcpu();
    x--;
    printf("Subtraction Thread, Processor NO: %d,x:%d\n", processor_no,x);
    //usleep(10000);
    }
}

int main(){
    pthread_t tid1,tid2;
    //create a thread
    pthread_create(&tid1, NULL, &addition, NULL);
    pthread_create(&tid2, NULL, &subtraction, NULL);
    for(int i=0 ;i<100;i++){
    int processor_no;
    processor_no = sched_getcpu();
    printf("Main Thread, Processor NO: %d\n", processor_no);
    usleep(10000);
    }

    //to force main thread to wait untill sub thread is not completed
    pthread_join(tid1,NULL);
    pthread_join(tid2,NULL);

    return 0;
}