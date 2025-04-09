import pandas as pd

def calculate_frequency(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Calculate the frequency
    timestamps = df['#timestamp [ns]']
    time_differences = timestamps.diff().dropna()  # Calculate time differences
    frequency = 1 / (time_differences.mean() * 1e-9)  # Convert nanoseconds to seconds and calculate frequency

    return frequency

cam_freq = calculate_frequency('dataset4/mav0/cam0/data.csv')
imu_freq = calculate_frequency('dataset4/mav0/imu0/data.csv')

print(f"Frequency of the camera: {cam_freq:.2f} Hz")
print(f"Frequency of the imu: {imu_freq:.2f} Hz")