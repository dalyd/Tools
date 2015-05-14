#include<time.h>
#include<iostream>


int main(int argc, char** argv) {
    volatile uint64_t x = 0;
    volatile uint64_t result;
    for (int i = 0; i < 1000000000; i++)
        {
            x++;
        }
    result = x;
}
