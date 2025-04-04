from utils.utils import register_signal_handlers
from camera.camera import Camera
from utils.config import CAMERA_CONFIG
import cv2
import lcm
from mbot_lcm_msgs import mbot_img_t
from mbot_lcm_msgs import timestamp_t
import time


# setup camera
config = CAMERA_CONFIG
camera_id = config["camera_id"]
image_width = config["image_width"]
image_height = config["image_height"]
fps = config["fps"]

camera = Camera(camera_id, image_width, image_height, fps)

lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=0")

subscription = lc.subscribe("EXAMPLE", time)


def time_callback(channel, data):
    msg = timestamp_t.decode(data)
    if msg.array_size == 0:
        print("No Timestamp received")
    else:
        print(f"Timestamp received: {msg.utime}")
        

# Subscribe to the timestamp channel
timestamp_subscription = lc.subscribe("TIMESTAMP_CHANNEL", time_callback)


def send_png_image():
    while camera.running:
        # Capture the frame
        frame = camera.capture_frame()

        # Process the frame (to be defined in subclasses)
        frame = camera.process_frame(frame)

        cur_time = timestamp_t.utime
        img_name = f"{cur_time}.png"

        msg = mbot_img_t()
        msg.img_name = img_name 
        msg.utime = cur_time  # Timestamp in milliseconds
        msg.img_data = bytearray(frame)  # Set the image data as a bytearray
 
        lc.publish('MBOT_IMG_CHANNEL', msg.encode())
        print(f"Sent PNG image '{msg.img_name}' with timestamp {msg.utime}")

if __name__ == '__main__':
    send_png_image()
