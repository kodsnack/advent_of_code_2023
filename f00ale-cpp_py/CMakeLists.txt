cmake_minimum_required(VERSION 3.18)
project(aoc23)

set(CMAKE_CXX_STANDARD 17)

if(${SANITIZE})
add_compile_options(-fsanitize=address,leak)
add_link_options(-fsanitize=address,leak)
endif()

add_compile_options(-Wall -Wextra -march=native)

add_library(aoc23_problems OBJECT
        src/p01.cpp
        src/p02.cpp
        src/p03.cpp
        src/p04.cpp
        src/p05.cpp
#        src/p06.cpp
#        src/p07.cpp
#        src/p08.cpp
#        src/p09.cpp
#        src/p10.cpp
#        src/p11.cpp
#        src/p12.cpp
#        src/p13.cpp
#        src/p14.cpp
#        src/p15.cpp
#        src/p16.cpp
#        src/p17.cpp
#        src/p18.cpp
#        src/p19.cpp
#        src/p20.cpp
#        src/p21.cpp
#        src/p22.cpp
#        src/p23.cpp
#        src/p24.cpp
#        src/p25.cpp
        )

add_executable(aoc23 src/main.cpp)
target_link_libraries(aoc23 PRIVATE aoc23_problems)
