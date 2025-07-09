#define GNU _GNU_SOURCE
#include <iostream>
#include <unistd.h>  // For getpid() and getppid()
using namespace std;
int main() {
    
    int child_status;
    int child_pid;
    int parentPID;
    int processor_no;
    //Get parent PID
    parentPID = getpid();
    
    child_status = fork();
    if (child_status==0){
        
        child_pid=getpid();
        processor_no=sched_getcpu(); // get processor no
        cout << "Parent PID: " << parentPID << ", Child PID: " << child_pid << ", Processor: " << processor_no << endl;
    }
    
    else{
        processor_no=sched_getcpu(); // get processor no
        cout << "Parent PID : " << parentPID << ", Processor:" << processor_no << endl; // first print this because child not created at first 

    }
      
    return 0;
}
