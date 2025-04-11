import matplotlib.pyplot as plt
import numpy as np
import argparse
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import cv2

def main():
    parser = argparse.ArgumentParser()

    # Add parameters (arguments)
    parser.add_argument('-f', '--file', type=str, help="Log file", required=True)
    parser.add_argument('-p', '--path', type=str, help="Saved path to dataset", required=False)
    args = parser.parse_args()

    # Load the dataset
    try:
        data = np.loadtxt(args.file, delimiter=',', skiprows=1)
    except Exception as e:
        print(f"Error loading file: {e}")
        return

    # Extract time, x, y, z columns
    try:
        time = data[:, 0]
        x = data[:, 1]
        y = data[:, 2]
        z = data[:, 3]
    except IndexError as e:
        print(f"Error extracting columns: {e}")
        return

    # Plot x, y, z versus time using scatter plot
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(x, y, z, c=time, cmap='viridis', s=10)

    # ax.set_title('3D Pose')
    # ax.set_xlabel('X Position')
    # ax.set_ylabel('Y Position')
    # ax.set_zlabel('Z Position')
    # print((time[-1] - time[0])/1000000000)

    # plt.show()
    # Animate the pose in 3D using scatter plot
    def update(frame):
        ax.cla()
        ax.scatter(x[:frame], y[:frame], z[:frame], c=time[:frame], cmap='viridis', s=10)
        ax.set_title('3D Pose Animation')
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Z Position')

    ani = FuncAnimation(fig, update, frames=len(time), interval=50, repeat=False)
    plt.show()
    if args.path:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()