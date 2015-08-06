cmake_minimum_required(VERSION 2.8)
project (TestWorkloads)

add_definitions(-fno-omit-frame-pointer)

find_package(Boost COMPONENTS thread system REQUIRED)
find_package (Threads)
include_directories(${Boost_INCLUDE_DIRS})
add_executable(condvar condvar.cpp)
target_link_libraries(condvar ${Boost_LIBRARIES})
target_link_libraries (condvar ${CMAKE_THREAD_LIBS_INIT})

add_executable(sleep sleep.cpp)
add_executable(cpuload cpuload.cpp)