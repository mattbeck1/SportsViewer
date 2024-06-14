import cv2
import pytesseract
import re
import numpy as np
from PIL import Image

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise and improve thresholding
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Use adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)
    # Apply morphological operations to enhance text regions
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresh, kernel, iterations=1)
    return dilated

def find_text_regions(thresh):
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def extract_text_from_regions(image, contours):
    time_texts = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Filter contours based on size (to avoid very small regions)
        if 50 < w < 300 and 20 < h < 100:  # Adjust size filtering as needed
            roi = image[y:y+h, x:x+w]
            # Use Tesseract with specific PSM mode for single line of text
            custom_config = r'--oem 3 --psm 1 -c tessedit_char_whitelist=0123456789:'
            text = pytesseract.image_to_string(roi, config=custom_config)
            print(f"Detected text: {text.strip()}")  # Debug output
            time_texts.append(text.strip())
    return time_texts

def find_time_pattern(texts):
    time_pattern = re.compile(r'\b\d{1,2}:\d{2}\b')
    for text in texts:
        match = time_pattern.search(text)
        if match:
            return match.group()
    return None

# Load the image
image_path = 'test_screen2.png'  # Replace with the path to your image
image = cv2.imread(image_path)

# Preprocess the image
preprocessed = preprocess_image(image)

# Save the preprocessed image for inspection
cv2.imwrite('preprocessed_image.png', preprocessed)

# Find text regions
contours = find_text_regions(preprocessed)

# Extract text from regions
texts = extract_text_from_regions(image, contours)

# Find time pattern
time_text = find_time_pattern(texts)

print(f'Extracted Time: {time_text}')