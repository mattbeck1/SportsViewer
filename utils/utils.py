from picamera2 import Picamera2, Preview
import pytesseract

def getSelectedROI(roi):
    picam2 = Picamera2()
    capture_config = picam2.create_still_configuration()

    image = picam2.switch_mode_and_capture_image(capture_config)

    selected_roi = image[roi[y1]:roi[y2], roi[x1]:roi[x2]]

    custom_config = r'--oem 3 --psm 6'
    value = pytesseract.image_to_string(scoreboard, config=custom_config)

    return roi