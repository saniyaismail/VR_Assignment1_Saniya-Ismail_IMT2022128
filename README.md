# VR_Assignment1_Saniya-Ismail_IMT2022128

# Part A - Coin Detection

- cd partA 

## Input Image
![Alt Text](partA/images/coins.jpeg)
**Path:** `images/coins.jpeg`

The code can be found at `coin_detection.py`. On running the Python script, it reads the input image from `images/coins.jpeg` and writes the following files as an output to the `output` directory:

- `output/detected_coins.jpg` - Image with detected coins outlined
- `output/threshold.jpg` - Thresholded binary image
- `output/segmented_coin_1.jpg` to `output/segmented_coin_17.jpg` - Individual segmented coins

---

## 1. Image Preprocessing

- **Resizing:** The image is resized while maintaining aspect ratio to ensure efficient processing.
- **Grayscale Conversion:** `cv2.cvtColor` is used to convert the image to grayscale.
- **Gaussian Blurring:** `cv2.GaussianBlur` is applied to remove noise and smoothen the image.
- **Adaptive Thresholding:** `cv2.adaptiveThreshold` is used to binarize the image, making object detection easier.

---

## 2. Edge Detection and Contour Filtering

- `cv2.findContours` is used to identify object boundaries in the binary image.
- **Circular Contour Filtering:** Contours are filtered based on circularity and area constraints to detect coins accurately.

### Formula Used:
**Circularity**  
\[
\text{Circularity} = \frac{4\pi \times \text{Area}}{\text{Perimeter}^2}
\]  
Only contours with circularity between **0.7 and 1.2** are considered valid coins.

---

## 3. Coin Segmentation

- **Bounding Boxes:** `cv2.boundingRect` is used to extract rectangular regions containing coins.
- **Masking:** A mask is created for each segmented coin to extract only the relevant portion.
- **Saving Individual Coins:** Each segmented coin is saved separately.

### Output Files:
- `output/segmented_coin_1.jpg` to `output/segmented_coin_17.jpg`

---

## 4. Coin Counting

- The total number of coins detected is 17

---

## Observations:

- In cases where there is **uneven lighting**, some coins may not be detected properly due to inconsistent contour detection.
