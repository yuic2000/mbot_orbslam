'''
Author: Po-Hsun Chang
Email: pohsun@umich.edu
Latest update date: 04/06/2025
'''

import sys
import os
import shutil
import lcm
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from mbot_lcm_msgs import mbot_img_t
from mbot_lcm_msgs import mbot_imu_t
     
## -------------- Create folders and subfolders -------------- ##
# This function creates the necessary folders and subfolders for storing the dataset.
def createDataFolder(args):

    if not os.path.exists(args.path):
        os.makedirs(args.path)
        print(f"Folder '{args.path}' created.")

        mav0_folder = os.path.join(args.path, "mav0")
        os.makedirs(mav0_folder)
        print(f"Folder 'mav0' created.")

        ts_file = os.path.join(mav0_folder, "timestamp.txt")

        # Create the "cam0" folder and its subfolders
        cam0_folder = os.path.join(mav0_folder, "cam0")
        os.makedirs(cam0_folder)
        print(f"Folder 'cam0' created.")

        cam0_data_folder = os.path.join(cam0_folder, "data")
        os.makedirs(cam0_data_folder)
        print(f"Folder 'cam0/data' created.")

        cam0_data_file = os.path.join(cam0_folder, "data.csv")
        with open(cam0_data_file, 'w') as file:
                file.write("#timestamp [ns],filename\n")

        # Copy cam0 sensor.yaml to dataset
        src_file = "/home/mbot/mbot_ws/mbot_dataset/dataset/cam/sensor.yaml"
        cam_sensor_file = os.path.join(cam0_folder, os.path.basename(src_file))
        shutil.copy(src_file, cam_sensor_file)
        print(f"sensor.yaml copied to {cam0_folder}")

        # Create the "imu0" folder and its subfolders
        imu0_folder = os.path.join(mav0_folder, "imu0")
        os.makedirs(imu0_folder)
        print(f"Folder 'imu0' created.")

        imu0_data_file = os.path.join(imu0_folder, "data.csv")
        with open(imu0_data_file, 'w') as file:
            file.write("#timestamp [ns],w_RS_S_x [rad s^-1],w_RS_S_y [rad s^-1],w_RS_S_z [rad s^-1],a_RS_S_x [m s^-2],a_RS_S_y [m s^-2],a_RS_S_z [m s^-2]\n")
    
        # Copy imu0 sensor.yaml to dataset
        src_file = "/home/mbot/mbot_ws/mbot_dataset/dataset/imu/sensor.yaml"
        imu_sensor_file = os.path.join(imu0_folder, os.path.basename(src_file))
        shutil.copy(src_file, imu_sensor_file)
        print(f"sensor.yaml copied to {imu0_folder}")
    
    else:
        print("Folder exists!\n")

    return cam0_data_folder, cam0_data_file, imu0_data_file, ts_file

## -------------- Main function -------------- ##
def main():

    ## -------------  Read in arguments and file  ------------ ##
    parser = argparse.ArgumentParser()

    # Add parameters (arguments)
    parser.add_argument('-f', '--file', type=str, help="Log file", required=True)
    parser.add_argument('-p', '--path', type=str, help="Saved path to dataset", required=True)
    args = parser.parse_args()

    # Check if the user has provided a log file as an argument
    if len(sys.argv) < 2:
        sys.stderr.write("usage: read-log <logfile>\n")
        sys.exit(1)

    # Open the event log file in read mode
    log = lcm.EventLog(args.file, "r")

    ## -------------  Create folders and subfolders  ------------ ##
    cam0_data_folder, cam0_data_file, imu0_data_file, ts_file = createDataFolder(args)

    # Iterate through all events in the log
    for event in log:

        ## -------------  Save Image Data  ------------ ##
        if event.channel == "MBOT_IMG_CHANNEL":
            # Decode the data from the event
            msg = mbot_img_t.decode(event.data)
            ntime = msg.utime*1000
            img_name = f"{ntime}.png"

            # For PNG compressed data - no need to reshape, just decode the PNG
            img_data = np.frombuffer(msg.img_data[:msg.data_size], dtype=np.uint8)
            
            # Decode the PNG data
            img_array = cv2.imdecode(img_data, cv2.IMREAD_COLOR)
            
            # Convert from BGR to RGB (OpenCV uses BGR by default)
            img_array_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            
            # Use PIL to save the image
            # img = Image.fromarray(img_array_rgb).rotate(180) # for flipped
            img = Image.fromarray(img_array_rgb)
            output_img_name = f"{img_name}"
            output_path = os.path.join(cam0_data_folder, output_img_name)
            img.save(output_path)

            # Write each timestamp and filename pair in the specified format
            with open(cam0_data_file, 'a') as file:
                file.write(f"{ntime},{output_img_name}\n")
                print("Image saved\n")

            with open(ts_file, 'a') as file:
                file.write(f"{ntime}\n")
                print("Timestamp saved\n")

        ## -------------  Save IMU Data  ------------ ##
        if event.channel == "MBOT_IMU":   
            # Decode the data from the event
            msg = mbot_imu_t.decode(event.data)
            ntime = msg.utime*1000
            gyro = msg.gyro
            accel = msg.accel

            with open(imu0_data_file, 'a') as file:
                # file.write(f"{ntime},{gyro[2]},{gyro[0]},{gyro[1]},{accel[2]},{accel[0]},{accel[1]}\n")
                file.write(f"{ntime},{gyro[0]},{gyro[1]},{gyro[2]},{accel[0]},{accel[1]},{accel[2]}\n")
                print("Imu data saved\n") 

if __name__ == "__main__":
    main()
