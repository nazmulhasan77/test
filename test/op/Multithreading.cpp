#include <iostream>
#include <pthread.h>   // Required for pthreads
using namespace std;

void *subtraction(void *arg){
    int processor_no;
    processor_no = sched_getcpu();
    cout << "Subtraction Thread" << ", Processor NO: " << processor_no << endl;
    return NULL;
}

void *addition(void *arg){
    int processor_no;
    processor_no = sched_getcpu();
    cout << "Addition Thread" << ", Processor NO: " << processor_no << endl;
    return NULL;
}

int main() {
    pthread_t threadID1,threadID2;
    int processor_no;
    //create thread
    pthread_create(&threadID1,NULL, &subtraction , NULL);
    pthread_create(&threadID2,NULL, &addition , NULL);
    //wait for subthread to finish
    pthread_join(threadID1,NULL);
    pthread_join(threadID2,NULL);

    

    processor_no = sched_getcpu();

    cout << "Main Processor NO : " << processor_no << endl;

    return 0;
}
