//***********************************************
//PARSING IN XYZ!!!!!
//***********************************************

#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"
#include <stdio.h>

#include <vector>
#include <array>

#include "mavlink/SysMavlink/mavlink.h"
#include "mavlink/SysMavlink/mavlink_msg_ret_lidar_distance_data_packet.h"
#include "mavlink/SysMavlink/mavlink_msg_ret_lidar_auxiliary_data_packet.h"

#include "unitree/parse_range_auxiliary_data_to_cloud.h"

#define LIDAR_UART    uart0
#define LIDAR_BAUD    2000000
#define LIDAR_TX_PIN  16
#define LIDAR_RX_PIN  17

int main() {
    stdio_init_all();
    sleep_ms(2500);
    printf("BOOT ok. Matched-pair -> cloud test\n");

    uart_init(LIDAR_UART, LIDAR_BAUD);
    gpio_set_function(LIDAR_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(LIDAR_RX_PIN, GPIO_FUNC_UART);
    uart_set_fifo_enabled(LIDAR_UART, true);

    static mavlink_message_t rx_msg;
    static mavlink_status_t  rx_status;

    static mavlink_ret_lidar_auxiliary_data_packet_t last_aux;
    static mavlink_ret_lidar_distance_data_packet_t  last_dist;
    static bool have_aux = false;
    static bool have_dist = false;

    absolute_time_t t0 = get_absolute_time();
    uint32_t clouds_ok = 0;
    uint32_t clouds_fail = 0;

    while (true) {
        while (uart_is_readable(LIDAR_UART)) {
            uint8_t b = uart_getc(LIDAR_UART);

            if (mavlink_parse_char(MAVLINK_COMM_0, b, &rx_msg, &rx_status)) {

                if (rx_msg.msgid == MAVLINK_MSG_ID_RET_LIDAR_AUXILIARY_DATA_PACKET) {
                    mavlink_msg_ret_lidar_auxiliary_data_packet_decode(&rx_msg, &last_aux);
                    have_aux = true;
                } else if (rx_msg.msgid == MAVLINK_MSG_ID_RET_LIDAR_DISTANCE_DATA_PACKET) {
                    mavlink_msg_ret_lidar_distance_data_packet_decode(&rx_msg, &last_dist);
                    have_dist = true;
                }

                if (have_aux && have_dist && last_aux.packet_id == last_dist.packet_id) {

                    std::vector<std::array<float, 4>> cloud;
                    cloud.reserve(256);

                    bool ok = parseRangeAuxiliaryDataToCloud(last_aux, last_dist, cloud);

                    if (ok) {
                        clouds_ok++;
                        printf("cloud ok: packet_id=%u points=%u\n",
                               (unsigned)last_dist.packet_id,
                               (unsigned)cloud.size());

                        if (!cloud.empty()) {
                            printf("  p0: x=%.3f y=%.3f z=%.3f i=%.3f\n",
                                   (double)cloud[0][0],
                                   (double)cloud[0][1],
                                   (double)cloud[0][2],
                                   (double)cloud[0][3]);
                        }
                    } else {
                        clouds_fail++;
                        printf("cloud FAIL: packet_id=%u\n", (unsigned)last_dist.packet_id);
                    }

                    have_aux = false;
                    have_dist = false;
                }
            }
        }

        if (absolute_time_diff_us(t0, get_absolute_time()) >= 1000000) {
            printf("clouds/s ok=%lu fail=%lu\n",
                   (unsigned long)clouds_ok,
                   (unsigned long)clouds_fail);
            clouds_ok = clouds_fail = 0;
            t0 = get_absolute_time();
        }

        tight_loop_contents();
    }
}