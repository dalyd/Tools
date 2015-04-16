#include<time.h>
#include<iostream>


void inline sleepmicros(long long s) {
    if ( s <= 0 )
        return;
    struct timespec t;
    t.tv_sec = (int)(s / 1000000);
    t.tv_nsec = 1000 * ( s % 1000000 );
    struct timespec out;
    if ( nanosleep( &t , &out ) ) {
        std::cout << "nanosleep failed" << std::endl;
    }
}


int main(int argc, char** argv) {
    int x = 0;
    struct timespec t;
    t.tv_sec = 0;
    t.tv_nsec = 1000 * 1000;
    struct timespec out;
    for (int i = 0; i < 1000; i++)
        {
            //sleepmicros(10000);
            nanosleep(&t, &out);
        }
}
