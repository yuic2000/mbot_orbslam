from utils.utils import register_signal_handlers
from camera.camera import Camera
from utils.config import CAMERA_CONFIG
import cv2
import lcm
from mbot_lcm_msgs import mbot_img_t
from mbot_lcm_msgs import timestamp_t
import time
import threading


# Configuration
config = CAMERA_CONFIG
camera_id = config["camera_id"]
image_width = config["image_width"]
image_height = config["image_height"]
fps = config["fps"]
PUBLISH_RATE_HZ = 10  # Configurable publish rate (Hz)

# Initialize camera
camera = Camera(camera_id, image_width, image_height, fps)

# Initialize LCM
lc = lcm.LCM("udpm://239.255.76.67:7667?ttl=0")

# Global variable to store the latest timestamp
last_timestamp = None


def time_callback(channel, data):
    """Callback function for timestamp messages"""
    msg = timestamp_t.decode(data)
    global last_timestamp
    last_timestamp = msg.utime


def publish_images():
    """Function to capture, process and publish camera images"""
    global last_timestamp
    period = 1.0 / PUBLISH_RATE_HZ  # Calculate period based on rate
    
    while camera.running:
        start_time = time.time()
        
        # Capture and process the frame
        frame = camera.capture_frame()
        frame = camera.process_frame(frame)
        
        # PNG compression
        _, buffer = cv2.imencode('.png', frame)
        frame_bytes = buffer.tobytes()

        # Skip publishing if no timestamp is available
        if last_timestamp is None:
            time.sleep(0.01)  # Small delay to prevent CPU spinning
            continue
            
        # Create and publish the message
        cur_time = last_timestamp
        img_name = f"{cur_time}.png"

        msg = mbot_img_t()
        msg.img_name = img_name 
        msg.utime = cur_time
        msg.data_size = len(frame_bytes)  # Set the size of compressed data
        msg.img_data = bytearray(frame_bytes)  # Use the compressed PNG data

        lc.publish('MBOT_IMG_CHANNEL', msg.encode())
        # print(f"Sent PNG image '{img_name}' ({msg.data_size} bytes)")
        
        # Sleep to maintain the desired publish rate
        elapsed = time.time() - start_time
        sleep_time = max(0, period - elapsed)
        time.sleep(sleep_time)


def main():
    """Main function to set up and run the image publisher"""
    # Subscribe to timestamp messages
    lc.subscribe("MBOT_TIMESYNC", time_callback)

    # Start image publishing in a separate thread
    publish_thread = threading.Thread(target=publish_images, daemon=True)
    publish_thread.start()

    # Register signal handlers for clean shutdown
    register_signal_handlers(lambda: camera.cleanup())

    try:
        print(f"MBot Image Publisher running at {PUBLISH_RATE_HZ} Hz")
        while True:
            lc.handle()
    except KeyboardInterrupt:
        print("Shutting down...")
        camera.cleanup()


if __name__ == "__main__":
    main()