#include "pico/stdlib.h"
#include <stdio.h>

#include "rx_unitree.h"
#include "tx_ardupilot.h"

int main() {
    stdio_init_all();
    sleep_ms(2500);
    printf("MAIN: Unitree L1 -> 17 pts -> OBSTACLE_DISTANCE_3D\n");

    rx_unitree_init();
    tx_ardupilot_init();

    while (true) {
        rx_unitree_poll();
        tx_ardupilot_send_if_due();

        tight_loop_contents();
    }
}
