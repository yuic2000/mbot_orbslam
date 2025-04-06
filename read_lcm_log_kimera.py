'''
Author: Po-Hsun Chang
Email: pohsun@umich.edu
Latest update date: 04/03/2025
'''

import sys
import os
import lcm
import argparse
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from mbot_lcm_msgs import mbot_img_t

parser = argparse.ArgumentParser()

# Add parameters (arguments)
parser.add_argument('-f', '--file', type=str, help="Log file", required=True)
parser.add_argument('-img_folder', '--img_folder', type=str, help="Name of the image folder", required=True)
args = parser.parse_args()

# Check if the user has provided a log file as an argument
if len(sys.argv) < 2:
    sys.stderr.write("usage: read-log <logfile>\n")
    sys.exit(1)

# Open the event log file in read mode
log = lcm.EventLog(args.file, "r")

if not os.path.exists(args.img_folder):
    os.makedirs(args.img_folder)
    data_folder = os.path.join(args.img_folder, "data")
    os.makedirs(data_folder)
    print(f"Folder '{args.img_folder}' created.")

data_file = os.path.join(args.img_folder, "data.csv")
with open(data_file, 'w') as file:
        # Write the header
        file.write("#timestamp [ns],filename\n")

# Iterate through all events in the log
for event in log:
    # Check if the event is on the "MBOT_ODOMETRY" channel
    if event.channel == "MBOT_IMG_CHANNEL":
        # Decode the data from the event
        msg = mbot_img_t.decode(event.data)
        utime = msg.utime
        img_name = msg.img_name
        img_data = np.frombuffer(msg.img_data, dtype=np.uint8)
        
        height = 720
        width = 1280
        channels = 3  # RGB image
        img_array = img_data.reshape((height, width, channels))

        # Save png images to data folder
        img = Image.fromarray(img_array, 'RGB')
        output_img_name = f"{img_name}"
        output_path = os.path.join(data_folder, output_img_name)
        img.save(output_path)

        # Write each timestamp and filename pair in the specified format

        with open(data_file, 'a') as file:
            file.write(f"{utime},{output_img_name}\n")
        # Print the decoded message
        print("Image saved")
