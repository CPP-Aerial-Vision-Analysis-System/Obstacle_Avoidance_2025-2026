#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"

#include <stdio.h>
#include <vector>
#include <array>
#include <cmath>
#include <cfloat>

#include "obstacle_shared.h"

//sysmavlink include
#include "mavlink/SysMavlink/mavlink.h"
#include "mavlink/SysMavlink/mavlink_msg_ret_lidar_distance_data_packet.h"
#include "mavlink/SysMavlink/mavlink_msg_ret_lidar_auxiliary_data_packet.h"

//unitree include
#include "unitree/parse_range_auxiliary_data_to_cloud.h"

#define LIDAR_UART    uart0
#define LIDAR_BAUD    2000000
#define LIDAR_TX_PIN  16
#define LIDAR_RX_PIN  17

static constexpr float MIN_R = 0.20f;
static constexpr float MAX_R = 20.0f;
static constexpr float PI = 3.14159265358979323846f;

static mavlink_message_t rx_msg;
static mavlink_status_t  rx_status;

static mavlink_ret_lidar_auxiliary_data_packet_t last_aux;
static mavlink_ret_lidar_distance_data_packet_t  last_dist;
static bool have_aux = false;
static bool have_dist = false;

static std::vector<std::array<float, 4>> cloud;

static inline int yaw_to_sector(float yaw) {
    float a = yaw + PI;  // [0,2pi)
    if (a < 0) a += 2.0f * PI;
    if (a >= 2.0f * PI) a -= 2.0f * PI;

    int idx = (int)floorf(a * (float)K_OBS / (2.0f * PI));
    if (idx < 0) idx = 0;
    if (idx >= K_OBS) idx = K_OBS - 1;
    return idx;
}

void rx_unitree_init() {
    uart_init(LIDAR_UART, LIDAR_BAUD);
    gpio_set_function(LIDAR_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(LIDAR_RX_PIN, GPIO_FUNC_UART);
    uart_set_fifo_enabled(LIDAR_UART, true);

    cloud.reserve(512);
}

void rx_unitree_poll() {
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
                cloud.clear();

                bool ok = parseRangeAuxiliaryDataToCloud(last_aux, last_dist, cloud);
                if (ok) {
                    float best_r[K_OBS];
                    float best_x[K_OBS], best_y[K_OBS], best_z[K_OBS];
                    uint8_t has[K_OBS];

                    for (int s = 0; s < K_OBS; s++) {
                        best_r[s] = FLT_MAX;
                        best_x[s] = best_y[s] = best_z[s] = 0.0f;
                        has[s] = 0;
                    }

                    for (size_t i = 0; i < cloud.size(); i++) {
                        float x = cloud[i][0];
                        float y = cloud[i][1];
                        float z = cloud[i][2];

                        float r = sqrtf(x*x + y*y + z*z);
                        if (r < MIN_R || r > MAX_R) continue;

                        float yaw = atan2f(y, x);
                        int s = yaw_to_sector(yaw);

                        if (r < best_r[s]) {
                            best_r[s] = r;
                            best_x[s] = x;
                            best_y[s] = y;
                            best_z[s] = z;
                            has[s] = 1;
                        }
                    }

                    // Publish result
                    ObstacleSet local{};
                    local.time_ms = to_ms_since_boot(get_absolute_time());
                    for (int s = 0; s < K_OBS; s++) {
                        if (has[s]) {
                            local.valid[s] = 1;
                            local.x[s] = best_x[s];
                            local.y[s] = best_y[s];
                            local.z[s] = best_z[s];
                        }
                    }
                    g_obs = local;
                }

                have_aux = false;
                have_dist = false;
            }
        }
    }
}
