import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def preprocess_image(path: str, max_dim: int = 700):
    """Loads, resizes, and preprocesses an image for analysis."""
    image = cv2.imread(path)
    
    if image is None:
        raise ValueError(f"Error: Unable to load image from path '{path}'")
    
    scale_factor = max_dim / max(image.shape[:2])
    resized_image = cv2.resize(image, (0, 0), fx=scale_factor, fy=scale_factor)

    # Converting the image to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Thresholding the image 
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)
    
    return resized_image, thresh, scale_factor

def filter_circular_contours(contours, scale, min_area=500):
    """Filters contours based on circularity and minimum area."""
    circular_contours = []
    
    for cnt in contours:
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue  

        area = cv2.contourArea(cnt)
        circularity = 4 * np.pi * (area / (perimeter ** 2))

        if 0.7 < circularity < 1.2 and area > min_area * (scale ** 2):
            circular_contours.append(cnt)
    
    return circular_contours

def detect_edges(image, threshold, scale):
    """Detects and draws circular contours in a thresholded image."""
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtering the circular coins
    circular_contours = filter_circular_contours(contours, scale)

    cv2.drawContours(image, circular_contours, -1, (0, 255, 0), 2)

    return circular_contours

def segment_coins(image, contours, save_folder):
    """Crops and saves detected coins."""
    segmented_coins = []
    
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Extracting mask for circular region
        mask = np.zeros_like(image, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), -1)

        # Applying mask to extract the coins
        segmented_coin = cv2.bitwise_and(image, mask)

        cropped_coin = segmented_coin[y:y+h, x:x+w]

        segmented_coins.append(cropped_coin)
        cv2.imwrite(os.path.join(save_folder, f"segmented_coin_{i+1}.jpg"), cropped_coin)

    return segmented_coins

def count_coins(image_path, save_folder="output"):
    """Detects, segments, and counts coins in the given image."""
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Preprocessing the image
    image, threshold, scale = preprocess_image(image_path)

    # Detecting the contours of the coins
    contours = detect_edges(image, threshold, scale)

    # Segmenting and saving the coins
    segmented_coins = segment_coins(image, contours, save_folder)
    num_coins = len(segmented_coins)

    # Saving the output images
    cv2.imwrite(os.path.join(save_folder, "detected_coins.jpg"), image)
    cv2.imwrite(os.path.join(save_folder, "threshold.jpg"), threshold)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(8, 6))
    plt.imshow(image_rgb)
    plt.axis("off")
    plt.title(f"Detected Coins: {num_coins}")
    plt.show()

    print(f"Total coins detected: {num_coins}")
    return num_coins


image_path = "images/coins.jpeg"
num_coins = count_coins(image_path, save_folder="output")
print(f"Total coins detected: {num_coins}") 
