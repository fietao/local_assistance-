import pyautogui
import pytesseract
import cv2
import numpy as np
from PIL import Image
import os

class ScreenReader:
    def __init__(self):
        # On Windows, you might need to specify the path to tesseract.exe.
        # usually it is located at: C:\Program Files\Tesseract-OCR\tesseract.exe
        # Uncomment and adjust the line below if pytesseract fails.
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        
        # Ensure a directory exists for saving temporary vision data
        self.vision_dir = os.path.join(os.path.dirname(__file__), 'temp')
        os.makedirs(self.vision_dir, exist_ok=True)
        self.last_capture_path = os.path.join(self.vision_dir, 'latest_screen.png')

    def capture_screen(self):
        """Takes a full screenshot and saves it temporarily."""
        screenshot = pyautogui.screenshot()
        screenshot.save(self.last_capture_path)
        return self.last_capture_path

    def read_text_from_screen(self):
        """Takes a screenshot and runs OCR (Optical Character Recognition) to extract any visible text."""
        try:
            # Take screenshot directly into PIL format
            screenshot = pyautogui.screenshot()
            
            # Convert PIL image to OpenCV format for easier processing (optional, but good practice)
            # opencv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # Extract text using PyTesseract
            extracted_text = pytesseract.image_to_string(screenshot)
            
            # Save a copy just in case we need to reference what the AI "saw" later
            screenshot.save(self.last_capture_path)
            
            # Clean up empty strings or excessive line breaks
            cleaned_text = " ".join(extracted_text.split())
            
            return cleaned_text if cleaned_text else "No recognizable text found on screen."
            
        except pytesseract.TesseractNotFoundError:
            return "ERROR: Tesseract ODE is not installed or configured correctly. Please install Tesseract."
        except Exception as e:
            return f"Vision Error: {e}"

vision = ScreenReader()