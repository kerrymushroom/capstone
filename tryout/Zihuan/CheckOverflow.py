import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from PIL import Image
import numpy as np

# Check if the chart content extends beyond the canvas boundaries.
def checkOverflow(img):
    img_array = np.array(img.convert("L"))  # Convert to grayscale image (L mode)
    height, width = img_array.shape  # Get image dimensions

    # Set the threshold for background color (assuming white background with a value of 255)
    background_color = 255
    threshold = 250  # Define a threshold; pixels below this value are considered chart content

    # Check the four boundaries (top, bottom, left, right)
    if np.any(img_array[0, :] < threshold):  # Check top boundary
        print("Chart exceeds top boundary")
    if np.any(img_array[-1, :] < threshold):  # Check bottom boundary
        print("Chart exceeds bottom boundary")
    if np.any(img_array[:, 0] < threshold):  # Check left boundary
        print("Chart exceeds left boundary")
    if np.any(img_array[:, -1] < threshold):  # Check right boundary
        print("Chart exceeds right boundary")

# Set the path for the image file
file_path = 'tryout/Zihuan/image_test.png'

# Load and check the saved image for boundary overflow
img = Image.open(file_path)
checkOverflow(img)
