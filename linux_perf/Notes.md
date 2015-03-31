Useful commands

Build condvar
 g++ -v -g -fno-omit-frame-pointer condvar.cpp -o condvar -pthread  -lboost_system -lboost_thread
 
sudo perf record -g  -e syscalls:sys_enter_futex -e
syscalls:sys_exit_futex condvar

sudo perf record -g  -e syscalls:sys_enter_futex -e
syscalls:sys_exit_futex -e syscalls:sys_enter_sched_yield -e
syscalls:sys_exit_yield ./condvar

sudo perf report -g graph --stdio | less 
