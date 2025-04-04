CAMERA_CONFIG = {
    "camera_id": 0,
    "image_width": 1280,
    "image_height": 720,
    "fps": 20
}

TAG_CONFIG = {
    "tag_size": 54,              # in millimeter
    "small_tag_size": 10.8,      # in millimeter
    "tag_family": "tagCustom48h12",
    "skip_frames": 5             # Process every 5th frame for tag detection
}

CONE_CONFIG = {
    "cone_base_radius": 40,  # in millimeter
    "cone_height": 80,       # in millimeter
    "skip_frames": 5,        # Process every 5th frame for cone detection
    "conf_thres": 0.8         # Detection confidence threshold [0,1]
}