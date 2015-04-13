SHELL = /bin/sh
.SUFFIXES:
.SUFFIXES: .c .cpp .o


CC=g++
CFLAGS=-g  -pthread  -lboost_system -lboost_thread -fno-omit-frame-pointer

condvar : condvar.cpp
	 $(CC) $< -I. -I$(srcdir) $(CFLAGS) -o $@
