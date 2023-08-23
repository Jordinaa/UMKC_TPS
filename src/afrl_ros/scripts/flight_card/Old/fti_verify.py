#!/usr/bin/env python3
from pymavlink import mavutil
import ctypes

# def set_parameter(ip, port, param_name, param_value):
#     master = mavutil.mavlink_connection(f"udp:{ip}:{port}")
#     master.wait_heartbeat()
#     print("Heartbeat received")

#     # Send the parameter update command
#     master.mav.param_set_send(
#         master.target_system,  # Target system
#         master.target_component,  # Target component
#         # param_name.encode('utf-8'),  # Parameter name (encoded as bytes)
#         b"FTI_ENABLE",
#         # 1065353216,
#         1,  # Parameter value
#         mavutil.mavlink.MAV_PARAM_TYPE_INT32  # Parameter type (float)
#     )

def set_parameter(ip, port, param_name, param_value):
    master = mavutil.mavlink_connection(f"udp:{ip}:{port}")
    master.wait_heartbeat()
    print("Heartbeat received")



    param_value_32bit = ctypes.c_int32(param_value).value
    # Send the parameter update command
    master.mav.param_set_send(
        master.target_system,  # Target system
        master.target_component,  # Target component
        # param_name.encode('utf-8'),  # Parameter name (encoded as bytes)
        b"FTI_ENABLE",
        # 1065353216,
        1,  # Parameter value
        mavutil.mavlink.MAV_PARAM_TYPE_INT32  # Parameter type (float)
    )
    print(f"Parameter {param_name} set to {param_value}.")

    # Request the parameter value from the vehicle
    master.param_fetch_one(param_name)
    for i in range(5):
        msg = master.recv_match(type='PARAM_VALUE', blocking=True, timeout=1)
        if msg and msg.param_id == param_name:
            print(f"Received parameter: {msg.param_id} = {msg.param_value}") 
            print(f"msg type:{msg.param_type}")
            break

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 14569

    set_parameter(ip, port, "FTI_ENABLE", 1) # 
    # in QGC it sets FTI_ENABLE to this number 1065353216
    
    #set_parameter(ip, port, "FTI_INJXN_POINT", 2.0) #ailerons is 1 
    #https://mavlink.io/en/messages/common.html#MAV_PARAM_TYPE

#  mavproxy.py --master=/dev/ttyUSB0,57600 
# --out udp:127.0.0.1:14551 --out udp:127.0.0.1:14520 --out udp:127.0.0.1:14530 --out udp:127.0.0.1:14569
