#!/usr/bin/env python3.8

import rospy
from sensor_msgs.msg import NavSatFix
import serial

# def parse_nmea(sentence):
#     data = sentence.split(',')
#     if data[0] == '$GNGGA' and len(data) >= 14:  # Check for complete data
#         try:
#             lat = float(data[2])
#             lon = float(data[4])
#             lat_dir = data[3]
#             lon_dir = data[5]
#             if lat_dir == 'S':
#                 lat = -lat
#             if lon_dir == 'W':
#                 lon = -lon
#             return lat, lon
#         except ValueError:
#             return None, None
#     else:
#         return None, None

def parse_nmea(sentence):
    data = sentence.split(',')
    if data[0] == '$GNGGA' and len(data) >= 14:  # Check for complete data
        try:
            # Latitude conversion from ddmm.mmmm to decimal degrees
            raw_lat = float(data[2])
            lat_deg = int(raw_lat / 100)
            lat_min = raw_lat % 100
            lat = lat_deg + (lat_min / 60)
            lat_dir = data[3]
            if lat_dir == 'S':
                lat = -lat

            # Longitude conversion from dddmm.mmmm to decimal degrees
            raw_lon = float(data[4])
            lon_deg = int(raw_lon / 100)
            lon_min = raw_lon % 100
            lon = lon_deg + (lon_min / 60)
            lon_dir = data[5]
            if lon_dir == 'W':
                lon = -lon

            return lat, lon
        except ValueError:
            rospy.logerr("ValueError in parse_nmea: Could not convert data to float.")
            return None, None
    else:
        return None, None


def gps_reader():
    rospy.init_node('gps_reader', anonymous=True)
    pub = rospy.Publisher('gps_data', NavSatFix, queue_size=10)

    # serial_port = serial.Serial('/dev/ttyACM0', 38400)  # Update with your GPS device serial port and baudrate

    while not rospy.is_shutdown():
        try:
            # data = serial_port.readline().decode('utf-8', errors='replace').strip()
            # for testing
            data = "$GNGGA,163115.00,1320.84865,N,07447.53325,E,1,10,2.94,60.2,M,-83.7,M,,*5D"

            lat, lon = parse_nmea(data)
            if lat is not None and lon is not None:
                fix = NavSatFix()
                fix.header.frame_id = 'gps'
                fix.latitude = lat
                fix.longitude = lon
                pub.publish(fix)
                rospy.loginfo("published GPS data - Latitude: {}, Longitude: {}".format(lat, lon))
        except Exception as e:
            rospy.logerr("Error reading serial data: {}".format(e))

if __name__ == '__main__':
    try:
        print("started")
        gps_reader()
        print("after gps_reader")
    except rospy.ROSInterruptException:
        pass

    # s = "$GNGGA,163115.00,1320.84865,N,07447.53325,E,1,10,2.94,60.2,M,-83.7,M,,*5D"
    # print(parse_nmea(s))
