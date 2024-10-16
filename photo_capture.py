import os
import time
from picamera2 import Picamera2

# Function to capture real-time photos
def capture_real_time_photos():
    print("Initializing camera...")
    picam2 = Picamera2()  # Initialize the camera
    try:
        picam2.start()
        print("Camera started.")

        real_time_dir = "/home/pi/Pictures/RaspPhotos"

        # Ensure the directory exists
        if not os.path.exists(real_time_dir):
            os.makedirs(real_time_dir)
            print(f"Directory {real_time_dir} created.")
        else:
            print(f"Directory {real_time_dir} already exists.")

        # Capture images in real-time
        for i in range(1, 6):
            filename = os.path.join(real_time_dir, f"image_{i}.jpg")
            picam2.capture_file(filename)
            print(f"Real-time photo {i} taken and saved to {filename}")
            time.sleep(1)  # Optional: Wait for 1 second between each photo

    finally:
        picam2.stop()
        picam2.close()
        print("Camera stopped.")





      # picam2.stop()
      # picam2.close()
      # print("Camera stopped.")

# if __name__ == "__main__":
    # capture_real_time_photos()
