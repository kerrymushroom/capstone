from imutils.object_detection import non_max_suppression
import numpy as np
import cv2

def checkOverlap(image, east_model_path, min_confidence, min_overlap_ratio):
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
    print("[INFO] loading EAST text detector...")
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

    if overlap_detected:
        print("There is an overlap in text regions in the image")
    else:
        print("There is no overlap in text regions in the image")

    # Draw bounding boxes on the original image
    for (startX, startY, endX, endY) in boxes:
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)

    # Display output image
    cv2.imshow("Text Detection", orig)
    cv2.waitKey(0)
    return overlap_detected

# Set image path and EAST model path
# image_path = "/Users/subring/capstone/tryout/Zihuan/image_3236_overlap.png"
image_path = "/Users/subring/capstone/tryout/Zihuan/image_1556_overlap.png"
east_model_path = "/Users/subring/capstone/tryout/Zihuan/frozen_east_text_detection.pb"

# Load the image
image = cv2.imread(image_path)

# Call the function
overlap = checkOverlap(image, east_model_path, 0.5, 0.2)
print("Overlap detected:", overlap)
