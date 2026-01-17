#include "pico/stdlib.h"
#include "hardware/uart.h"
#include "hardware/gpio.h"
#include <stdio.h>

#include "obstacle_shared.h"

// Standard MAVLink (ONLY in this file)
#include "ardupilotmega/mavlink.h"

#define FC_UART     uart1
#define FC_BAUD     921600
#define FC_TX_PIN   4
#define FC_RX_PIN   5

static constexpr uint8_t MY_SYSID  = 42;
static constexpr uint8_t MY_COMPID = MAV_COMP_ID_PERIPHERAL;

static absolute_time_t next_send_time;

static inline void send_msg(const mavlink_message_t* msg) {
    uint8_t buf[MAVLINK_MAX_PACKET_LEN];
    uint16_t len = mavlink_msg_to_send_buffer(buf, msg);
    uart_write_blocking(FC_UART, buf, len);
}

void tx_ardupilot_init() {
    uart_init(FC_UART, FC_BAUD);
    gpio_set_function(FC_TX_PIN, GPIO_FUNC_UART);
    gpio_set_function(FC_RX_PIN, GPIO_FUNC_UART);
    uart_set_fifo_enabled(FC_UART, true);

    next_send_time = make_timeout_time_ms(100);
}

void tx_ardupilot_send_if_due() {
    // 10 Hz send rate
    if (!time_reached(next_send_time)) return;
    next_send_time = make_timeout_time_ms(100);

    ObstacleSet snap = g_obs;

    mavlink_message_t msg;
    for (int s = 0; s < K_OBS; s++) {
        if (!snap.valid[s]) continue;

        mavlink_msg_obstacle_distance_3d_pack(
            MY_SYSID,
            MY_COMPID,
            &msg,
            snap.time_ms,
            MAV_DISTANCE_SENSOR_LASER,
            MAV_FRAME_BODY_FRD,
            (uint16_t)s,          // stable ID = sector index
            snap.x[s], snap.y[s], snap.z[s],
            0.20f,
            20.0f
        );

        send_msg(&msg);
    }
}
