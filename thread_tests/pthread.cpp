#include<chrono>
#include<iostream>
#include<pthread.h>
#include<thread>

void *runThread(void *threadid) {
    std::this_thread::sleep_for(std::chrono::seconds(10));
    pthread_exit(NULL);
}

int main(int argc, char* argv[])
{
    pthread_attr_t attr;
    pthread_t threads[10000];
    pthread_attr_init(&attr);
    auto s = pthread_attr_setstacksize(&attr, 8*1024*1024); // this is default
    if (s !=0)
        {
            std::cout << "pthread_attr_setstacksize returned nonzero: " << s << std::endl;
            return(EXIT_FAILURE);

        }
    for (int i=0; i < 10000; i++)
        {
            try {
                auto t = pthread_create(&threads[i], &attr, runThread, (void *) &i);
                if (t !=0)
                    {
                        // ERROR
                        std::cout << "pthread_create returned nonzero: " << t << " on iteration " << i << std::endl;
                        return(EXIT_FAILURE);
                    }
                pthread_detach(threads[i]);
            }
            catch(std::system_error e) {
                std::cout << "Crashed on " << i << " thread" << std::endl;
                std::cout << "e.code: " << e.code() << " e.what: " << e.what() << std::endl;
                return(EXIT_FAILURE);
            }
        }
    std::cout << "Started all threads" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(10));
    std::cout << "Slept for 10 seconds" << std::endl;

}
