Useful commands

Build condvar using makefile
 
sudo perf record -g  -e syscalls:sys_enter_futex -e
syscalls:sys_exit_futex condvar

sudo perf record -g  -e syscalls:sys_enter_futex -e
syscalls:sys_exit_futex -e syscalls:sys_enter_sched_yield -e
syscalls:sys_exit_yield ./condvar

sudo perf report -g graph --stdio -n | less 
