#!/usr/bin/env python3

from pymavlink import mavutil
import struct
import numpy as np
import socket
import time

# Definitions
input_control_index = {
    "Low": 0,
    "Medium": 1,
    "High": 2
}

control_settings = [0.1, 0.3, 0.5]  # percent
rate_settings = [np.deg2rad(15), np.deg2rad(30), np.deg2rad(45)]  # deg/s
attitude_settings = [np.deg2rad(5), np.deg2rad(10), np.deg2rad(20)]  # deg

FTI_INJXN_POINT = {
    "0": None,
    "1": control_settings,
    "2": control_settings,
    "3": control_settings,
    "4": rate_settings,
    "5": rate_settings,
    "6": rate_settings,
    "7": attitude_settings,
    "8": attitude_settings,
    "9": attitude_settings,
}

LOOP_GAIN = {
    "BASE": 1.0,
    "INCREASE": 1.2,
    "DECREASE": 0.8
}

def set_parameter(ip, port, param_name, param_value):
    master = mavutil.mavlink_connection(f"udp:{ip}:{port}")
    master.wait_heartbeat()
    print("Heartbeat Recieved")

    vstr = struct.pack(">i", int(param_value))
    vfloat, = struct.unpack(">f", vstr)
    # print("vfloat", vfloat)
    baby = bytes(param_name, 'utf-8')


    master.mav.param_set_send(
        master.target_system,  # Target system
        master.target_component,  # Target component
        baby,  # Parameter name (encoded as bytes)
        float(vfloat),  # Parameter value
        6  # Parameter type (float)
    )

    message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    # print(message['param_id'], message['param_value'])


def process_message(data):
    command = data.strip().split(' ')

    if len(command) != 6:
        print(f"Invalid command received: {command}")
        return

    param_name_point = command[0]
    param_value_point = command[3]
    setting = command[4]
    loop_gain = command[5]

    # print(f"{param_name_point}")
    # print(f"{param_value_point}")
    # print(f"{setting}")
    # print(f"{loop_gain}")

    setting_value = FTI_INJXN_POINT[param_value_point][input_control_index[setting]]
    loop_gain_value = LOOP_GAIN[loop_gain]

    # print(f"setting value {setting_value}")
    # print(f"loop gain value {loop_gain_value}")
    set_parameter(ip, port, "FTI_ENABLE", 0)

    print(f"Setting FTI_INJXN_POINT to {param_value_point}")
    set_parameter(ip, port, "FTI_INJXN_POINT", param_value_point)
    print("Successfully set FTI_INJXN_POINT")
    # print(f"Setting {setting} to {setting_value}")
    # set_parameter(ip, port, setting, setting_value)

    # print(f"Setting {loop_gain} to {loop_gain_value}")
    # set_parameter(ip, port, "FTI_LOOP_GAIN", loop_gain_value)
    # print("Successfully set FTI_LOOP_GAIN")

    print(f"Setting FTI_ENABLE to 1")
    set_parameter(ip, port, "FTI_ENABLE", 1)
    print("Successfully set FTI_ENABLE")

    time.sleep(int(command[1])*5)
    print("done sleeping")
    set_parameter(ip, port, "FTI_ENABLE", 0)
    print("Successfully set FTI_ENABLE to 0")



    client_socket.close()


if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 14561

    # Setting up TCP server to listen for incoming messages
    # server_ip = "192.168.1.123"
    server_ip = "10.3.20.79"
    server_port = 9876
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_ip, server_port))
    server_socket.listen()

    print(f"Server listening on {server_ip}:{server_port}")

    while True:
        client_socket, client_address = server_socket.accept()

        print(f"Connection established with {client_address}.")

        data = client_socket.recv(1024).decode("utf-8")
        print(f"Received command: {data}")

        process_message(data)

        # client_socket.close()
