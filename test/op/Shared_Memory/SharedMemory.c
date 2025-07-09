#include<stdlib.h>
#include<stdio.h>
#include <unistd.h>
#include<sys/wait.h>
#include<sys/shm.h>
int global_var=10;

int main(){
    int local_var;
    int *local_addr,*global_addr;
    pid_t pid;
    int status;
    key_t key;
    int shmid;

    local_var=20;
    local_addr=&local_var;
    global_addr=&global_var;

    //Create a shared memory space
    //int shmget(key_t key,size_t size,int shmflg)
    key=1234;
    shmid = shmget(key,sizeof(int),IPC_CREAT|0666);
    

    if(shmid == 0){
        perror("shmget: ");
        exit(EXIT_FAILURE);
    }

    printf("Shared Memory Id: %d\n",shmid);

    //Create a child
    pid=fork();
    if(pid==-1){
        perror("fork: ");
        exit(EXIT_FAILURE);
    }
    else if(pid==0){
        //Child Process
        printf("Child -> Local Veriable: %d , Global variable: %d\n", local_var,global_var);
        printf("Child -> Local Veriable Address: %p , Global variable Addrsss: %p\n", local_addr,global_addr);
        local_var=100;
        global_var=200;
        printf("Child -> Local Veriable: %d , Global variable: %d\n", local_var,global_var);
        printf("Child -> Local Veriable Address: %p , Global variable Addrsss: %p\n", local_addr,global_addr);

        //Attach child to the shared memory 
        //void *shmat(int shmid, const void *_Nullable shmaddr, int shmflg);
        //int shmdt(const void *shmaddr);
        void *shm_addr;
        shm_addr=shmat(shmid,NULL,0);

        if(shm_addr==(int *) -1){
            perror("shmat: ");
            exit(EXIT_FAILURE);
        }
        //Put valur into the Shared Memory
        int *shared_var = shm_addr;
        *shared_var=20;
        printf("Child -> Shared_Variable: %d\n",shared_var[0]);

        //Detach child  from shared memory
        status=shmdt(shm_addr);
        if(shm_addr==(int *) -1){
            perror("shmat: ");
            exit(EXIT_FAILURE);
        }


    }
    else{
        //parent process
        printf("Parent -> Local Veriable: %d , Global variable: %d\n", local_var,global_var);
        printf("Parent -> Local Veriable Address: %p , Global variable Addrsss: %p\n", local_addr,global_addr);

        //Attach Parent to the shared memory 
        void *shm_addr;
        shm_addr=shmat(shmid,NULL,0);

        if(shm_addr==(int *) -1){
            perror("shmat: ");
            exit(EXIT_FAILURE);
        }
        //Put value into the Shared Memory
        int *shared_var = shm_addr;
        printf("Parent -> Shared_Variable: %d\n",shared_var[0]);

        //Detach Parent  from shared memory
        status=shmdt(shm_addr);
        if(shm_addr==(int *) -1){
            perror("shmat: ");
            exit(EXIT_FAILURE);
        }



        wait(&status);
        //Parent's task after child terminatiion
        for(int i=0 ; i<10 ; i++){
            printf("Parent -> Local Veriable: %d , Global variable: %d\n", local_var,global_var);
            printf("Parent -> Local Veriable Address: %p , Global variable Addrsss: %p\n", local_addr,global_addr);
        }
    }

    printf("Successfully terminating.. \n");


    exit(EXIT_SUCCESS);
}