#ifndef BOOST_SYSTEM_NO_DEPRECATED
#define BOOST_SYSTEM_NO_DEPRECATED 1
#endif

#include <iostream>
#include <unistd.h>
#include <sched.h>
#include <pthread.h>
#include <boost/thread/condition.hpp>
#include <boost/thread/condition_variable.hpp>
#include <boost/thread/mutex.hpp>

boost::condition_variable cond;
boost::mutex mut;
bool lock_free;

int k = 4;
int i = 0;

void work() {
    while (i<k*500000000) i++;
}

void cond_wait() {
    std::cout << "cond_wait start" << std::endl;
    boost::unique_lock<boost::mutex> lock(mut);
    std::cout << "cond_wait after lock" << std::endl;
    while(!lock_free)
      {
	
	std::cout << "In while loop" << std::endl;
        cond.wait(lock);
      }
    std::cout << "After cond.wait" << std::endl;
    //Only thread in this region
    lock_free = false;
}

void cond_notify() {
    std::cout << "cond_notify start" << std::endl;
    boost::unique_lock<boost::mutex> lock(mut);
    std::cout << "cond_notify after lock" << std::endl;
   lock_free = true;
   cond.notify_one();
 
}

void* thread(void* arg) {
  
    work();
    sleep(k);
    std::cout << "After sleep, try to get lock" << std::endl;    
    
    cond_wait();
    // Begin critical section
    work();
    // End critical section
    cond_notify();



    for (i=0; i<k*2000000; i++) sched_yield();

}

int main(int argc, char* argv[]) {

    const int n = 3;
    lock_free = true;
    pthread_t ps[n];
    for (int t=0; t<n; t++)
      pthread_create(&ps[t], NULL, thread, NULL);
    for (int t=0; t<n; t++)
      pthread_join(ps[t], NULL);
}
