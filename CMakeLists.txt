cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# == Pico VS Code extension block (unchanged) ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.2.0)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.2.0-a4)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# =============================================

set(PICO_BOARD pico CACHE STRING "Board type")

include(pico_sdk_import.cmake)

project(obs_avoidance C CXX ASM)

pico_sdk_init()

add_executable(obs_avoidance
    main.cpp
    rx_unitree.cpp
    tx_ardupilot.cpp
    obstacle_shared.cpp
)

pico_enable_stdio_uart(obs_avoidance 1)
pico_enable_stdio_usb(obs_avoidance 0)

target_include_directories(obs_avoidance PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/include
    ${CMAKE_CURRENT_LIST_DIR}/include/c_library_v2
    ${CMAKE_CURRENT_LIST_DIR}/include/unitree
    ${CMAKE_CURRENT_LIST_DIR}/include/mavlink
)

target_link_libraries(obs_avoidance
    pico_stdlib
    hardware_uart
    hardware_gpio
)

pico_add_extra_outputs(obs_avoidance)
