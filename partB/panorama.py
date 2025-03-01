# %%
import cv2
import numpy as np
import matplotlib.pyplot as plt

image1 = cv2.imread("images/left.jpeg")
image2 = cv2.imread("images/middle.jpeg")
image3 = cv2.imread("images/right.jpeg")

def detect_and_save_keypoints(image, filename):
    """Detects keypoints using ORB and saves the image with keypoints drawn."""
    orb_detector = cv2.ORB_create()
    keypoints, _ = orb_detector.detectAndCompute(image, None)
    keypoint_image = cv2.drawKeypoints(image, keypoints, None, color=(0, 255, 0))
    cv2.imwrite(f"output/{filename}", keypoint_image)

def stitch_images(image_a, image_b):
    """Stitches two images together using feature matching and homography."""
    
    # Converting images to grayscale for feature detection
    gray_a, gray_b = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY), cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY) 

    # Initializing ORB detector
    orb_detector = cv2.ORB_create()

    # Detecting keypoints and computing descriptors
    keypoints_a, descriptors_a = orb_detector.detectAndCompute(gray_a, None)
    keypoints_b, descriptors_b = orb_detector.detectAndCompute(gray_b, None)

    # Using BFMatcher for feature matching
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)
    matches = sorted(matcher.match(descriptors_a, descriptors_b), key=lambda m: m.distance)


    if len(matches) < 4:
        print("Error: Not enough feature matches found for stitching.")
        return None

    # Extracting matched keypoints
    points_a = np.float32([keypoints_a[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    points_b = np.float32([keypoints_b[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Computing homography matrix using RANSAC
    homography_matrix, mask = cv2.findHomography(points_b, points_a, cv2.RANSAC)
    if homography_matrix is None:
        print("Error: Homography computation failed.")
        return None

    # Wrapping the image and returning the output
    img_height, img_width = image_a.shape[:2]  
    panorama_width = img_width + image_b.shape[1]

    warped_result = cv2.warpPerspective(image_b, homography_matrix, (panorama_width, img_height))

    warped_result[0:img_height, 0:img_width] = image_a

    return warped_result



if any(img is None for img in [image1, image2, image3]):
    print("Error: One or more images could not be loaded. Check the file paths.")
else:
    detect_and_save_keypoints(image1, "keypoints_left.jpg")
    detect_and_save_keypoints(image2, "keypoints_middle.jpg")
    detect_and_save_keypoints(image3, "keypoints_right.jpg")
    
    # Stitching the middle and right image first
    panorama_right = stitch_images(image2, image3)
    if panorama_right is not None:
        # Stitching the leftmost image with the previously stitched panorama
        panorama_final = stitch_images(image1, panorama_right)
        
        if panorama_final is not None:
            cv2.imwrite("output/panorama.jpg", panorama_final)
            
            panorama_rgb = cv2.cvtColor(panorama_final, cv2.COLOR_BGR2RGB)
            
            plt.figure(figsize=(12, 6))
            plt.imshow(panorama_rgb)
            plt.axis("off") 
            plt.title("Stitched Panorama")
            plt.show()
        else:
            print("Error: Failed to stitch the leftmost image with the panorama.")
    else:
        print("Error: Failed to stitch the rightmost two images.")



