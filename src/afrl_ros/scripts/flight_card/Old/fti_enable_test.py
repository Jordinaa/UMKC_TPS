#!/usr/bin/env python3

from pymavlink import mavutil
import struct



def set_parameter(ip, port, param_name, param_value):
    master = mavutil.mavlink_connection(f"udp:{ip}:{port}")
    master.wait_heartbeat()
    print("Heartbeat Recieved")

    vstr = struct.pack(">i", int(param_value))
    vfloat, = struct.unpack(">f", vstr)
    print("vfloat", vfloat)
    baby = bytes("FTI_ENABLE", 'utf-8')
    master.mav.param_set_send(
        master.target_system,  # Target system
        master.target_component,  # Target component
        baby,  # Parameter name (encoded as bytes)
        float(vfloat), #struct.pack(">i", int(param_value)),  # Parameter value
        6  # Parameter type (float)
    )

    # master.param_fetch_one(param_name)
    # master.mav.param_request_read_send(
    #     master.target_system, master.target_component,
    #     b'FTI_ENABLE',
    #     -1
    # )

    message = master.recv_match(type='PARAM_VALUE', blocking=True).to_dict()
    # print(message)
    # print(message['param_id'], message['param_value'])



if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 14561

    param_name_point = "FTI_INJXN_POINT"
    param_value_point = int(2)
    set_parameter(ip, port, param_name_point, param_value_point)

    param_name = "FTI_ENABLE"
    param_value = int(1)
    set_parameter(ip, port, param_name, param_value)

    #param set FTI_ENABLE 0
    #param show FTI_ENABLE 
