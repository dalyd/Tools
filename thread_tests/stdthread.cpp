#include<chrono>
#include<iostream>
#include<thread>


void runThread() {
    std::this_thread::sleep_for(std::chrono::seconds(10));
}

int main(int argc, char* argv[])
{
    for (int i=0; i < 10000; i++)
        {
            try {
                auto t = new std::thread(runThread);
                t->detach();
                free(t);
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
