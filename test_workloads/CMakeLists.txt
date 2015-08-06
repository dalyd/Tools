cmake_minimum_required(VERSION 3.1)
project (TestWorkloads)

find_package(Boost)

include_directories(${Boost_INCLUDE_DIRS})
add_executable(condvar condvar.cpp)
target_link_libraries(condvar ${Boost_LIBRARIES})
