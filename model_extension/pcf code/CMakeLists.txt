cmake_minimum_required(VERSION 3.23)
project(pair_correlation_function)

set(CMAKE_CXX_STANDARD 14)

include_directories(.)

add_executable(pair_correlation_function
        bincontainer.h
        functions.cpp
        functions.h
        main.cpp
        particle.h
        vector3d.h)
