import os
import json
from PIL import Image
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

# Check if the chart content extends beyond the canvas boundaries.
def checkOverflow(image_path):
    # Load the saved image
    img = Image.open(image_path)
    # Convert to grayscale image (L mode)
    img_array = np.array(img.convert("L"))
    # Get image dimensions
    height, width = img_array.shape

    # Set the threshold for background color (assuming white background with a value of 255)
    background_color = 255
    threshold = 250  # Define a threshold; pixels below this value are considered chart content

    # Check the four boundaries (top, bottom, left, right)
    if np.any(img_array[0, :] < threshold):  # Check top boundary
        return True
    if np.any(img_array[-1, :] < threshold):  # Check bottom boundary
        return True
    if np.any(img_array[:, 0] < threshold):  # Check left boundary
        return True
    if np.any(img_array[:, -1] < threshold):  # Check right boundary
        return True
    return False

def checkOverlap(image_path, east_model_path, min_confidence, min_overlap_ratio):
    image = cv2.imread(image_path)
    width, height = 320, 320
    # Copy the original image and get image dimensions
    orig = image.copy()
    (H, W) = image.shape[:2]

    # Set new width and height and calculate scaling ratio
    (newW, newH) = (width, height)
    rW = W / float(newW)
    rH = H / float(newH)

    # Resize the image and get new dimensions
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]

    # Output layer names for the EAST model
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"
    ]

    # Load the pre-trained EAST model
    # print("[INFO] loading EAST text detector...")
    net = cv2.dnn.readNet(east_model_path)

    # Construct a blob and perform a forward pass to get scores and geometry data
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    # Initialize bounding boxes and confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # Loop over each row
    for y in range(0, numRows):
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        for x in range(0, numCols):
            if scoresData[x] < min_confidence:
                continue

            (offsetX, offsetY) = (x * 4.0, y * 4.0)
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    # Apply non-maxima suppression to suppress overlapping bounding boxes
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # Check for overlap among text regions
    overlap_detected = False
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            # Get coordinates of two rectangles
            (x1, y1, x2, y2) = boxes[i]
            (x1_, y1_, x2_, y2_) = boxes[j]

            # Calculate intersection area
            inter_startX = max(x1, x1_)
            inter_startY = max(y1, y1_)
            inter_endX = min(x2, x2_)
            inter_endY = min(y2, y2_)

            inter_area = max(0, inter_endX - inter_startX) * max(0, inter_endY - inter_startY)

            # Calculate area of each rectangle
            area1 = (x2 - x1) * (y2 - y1)
            area2 = (x2_ - x1_) * (y2_ - y1_)

            # Calculate overlap ratio
            overlap_ratio = inter_area / min(area1, area2)
            # Check if overlap ratio exceeds threshold
            if overlap_ratio > min_overlap_ratio:
                overlap_detected = True
                break
        if overlap_detected:
            break

    # Display output image
    return overlap_detected

# Define the image folder path
base_dir = '/Users/subring/capstone/findRule/saved_data'
# json_file_path = "/Users/subring/capstone/tryout/Zihuan/GPTOutput.json"
json_file_path = "/Users/subring/capstone/findRule/gptOutputAdded.json"
east_model_path = "/Users/subring/capstone/tryout/Zihuan/frozen_east_text_detection.pb"

# Read the existing JSON file
with open(json_file_path, "r") as f:
    data = json.load(f)

# Traverse all subfolders and files
for root, dirs, files in os.walk(base_dir):
    for file in files:
        # Check if the file name ends with "_gpt.png"
        if file.lower().endswith('_gpt.png'):
            # Get the full file path
            image_path = os.path.join(root, file)
            # Get the folder name
            folder_name = os.path.basename(root)
            check_overflow = True
            check_overlap = True
            # if checkOverflow(image_path):
            #     check_overflow = "true"
            #     print(f"{folder_name} is overflowed")
            # if checkOverlap(image_path, east_model_path, 0.5, 0.3):
            #     check_overlap = "true"
            #     print(f"{folder_name} is overlapped")
            # Add image path to "0" under "189"
            if folder_name in data and "0" in data[folder_name]:
                data[folder_name]["0"]["check_overflow"] = True
                data[folder_name]["0"]["check_overlap"] = True
            else:
                print(f"Unable to find the key {folder_name} or '0'. Please check the JSON format!")

# Write the modified data back to the JSON file
with open(json_file_path, "w") as f:
    json.dump(data, f, indent=4)

print("Successfully updated the JSON file")
