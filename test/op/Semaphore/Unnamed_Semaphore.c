/*
	To understand how synchronization can be done between a parent process 
	and a child process by a binary unnamed semaphore.
*/
#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <wait.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <semaphore.h>

int main(){
	//Initialize a binary semaphore
	//int sem_init(sem_t *sem, int pshared, unsigned int value);
	sem_t binary_sem;
	if(sem_init(&binary_sem, 1, 1) == -1){
		perror("sem_init: ");
		exit(EXIT_FAILURE);
	}	
	
	//Generate a key by converting a pathname and a project identifier
	//key_t ftok(const char *pathname, int proj_id);
	key_t key;
	key = ftok("/home/bibrity/CSE_Courses/OS_CSE3241/Code/shared_memory_shm.c", 65);
	
	//Create a shared memory segment
	//int shmget(key_t key, size_t size, int shmflg);
	int shmid;
	shmid = shmget(key, sizeof(key), IPC_CREAT|0666);
	if(shmid == -1){
		perror("shmget: ");
		exit(EXIT_FAILURE);
	}
		
	//Create child process
	pid_t pid;
	pid = fork();
	if(pid == -1){
		perror("fork: ");
		exit(EXIT_FAILURE);
	}
	
	//Activities of Child process and parent process
	if(pid == 0){//Child process
		//Attaches the shared memory segment identified by shmid to the address space of the Child process.
		//void *shmat(int shmid, const void *shmaddr, int shmflg);
		int *shmaddr;
		shmaddr = shmat(shmid, NULL, 0);
		if(shmaddr == (int *)-1){
			perror("shmat: ");
			exit(EXIT_FAILURE);
		}
		
		//Use shared memory
		for(int i = 0; i<100; i++){
			sem_wait(&binary_sem);
			printf("%d. Child Process, Before updating: shared_var: %d\n", i, *shmaddr);
			*shmaddr += 1;
			printf("%d. Child Process, After updating: shared_var: %d\n", i, *shmaddr);
			sem_post(&binary_sem);
		}
		
		//Detach the shared memory segment from the address space of the Child process.
		//int shmdt(const void *shmaddr);
		if(shmdt(shmaddr) == -1){
			perror("shmdt: ");
			exit(EXIT_FAILURE);
		}
	}
	else{//Parent process
		//Attaches the shared memory segment identified by shmid to the address space of the Parent process.
		//void *shmat(int shmid, const void *shmaddr, int shmflg);
		int *shmaddr;
		shmaddr = shmat(shmid, NULL, 0);
		if(shmaddr == (int *)-1){
			perror("shmat: ");
			exit(EXIT_FAILURE);
		}
		
		//Use shared memory
		for(int i = 0; i<100; i++){
			sem_wait(&binary_sem);
			printf("%d. Parent Process, Before updating: shared_var: %d\n", i, *shmaddr);
			*shmaddr -= 1;
			printf("%d. Parent Process, After updating: shared_var: %d\n", i, *shmaddr);
			sem_post(&binary_sem);
		}	
	
		//Wait until termination of all processes
		wait(NULL);
		
		//Destroy unknamed semaphore
		//int sem_destroy(sem_t *sem);
		if(sem_destroy(&binary_sem)== -1){
			perror("sem_destroy: ");
			exit(EXIT_FAILURE);
		}
		
		//Detach the shared memory segment from the address space of the Parent process.
		//int shmdt(const void *shmaddr);
		if(shmdt(shmaddr) == -1){
			perror("shmdt: ");
			exit(EXIT_FAILURE);
		}
		
		//Remove shared memory segment
		//int shmctl(int shmid, int cmd, struct shmid_ds *buf);
		if(shmctl(shmid, IPC_RMID, NULL)){
			perror("shmctl: ");
			exit(EXIT_FAILURE);		
		}		
	}

	//Termination of parent process and child process
	exit(EXIT_SUCCESS);
}