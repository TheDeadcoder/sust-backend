import os
import cv2
import requests
import numpy as np
from io import BytesIO

# Load the foreground image (output.png)
foreground_image_path = 'output.png'
foreground_image = cv2.imread(foreground_image_path, -1)  # Load with alpha channel

bg_1 = 'https://images.unsplash.com/photo-1580508244245-c446ca981a6b?q=80&w=3174&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
bg_2 = 'https://img.freepik.com/free-photo/two-tones-gray-background_53876-104897.jpg?w=2000&t=st=1708169239~exp=1708169839~hmac=587784c160761fa043176f806b74a63826cfb1d17f23ef11f27561e7183004c5'

# Load the background image
background_image_path = bg_2
response = requests.get(background_image_path)
if response.status_code == 200:
    background_image_bytes = BytesIO(response.content)
    background_image_array = np.frombuffer(background_image_bytes.getvalue(), dtype=np.uint8)
    background_image_from_url = cv2.imdecode(background_image_array, cv2.IMREAD_COLOR)

    # Resize the background image to match the dimensions of the foreground image
    foreground_height, foreground_width, _ = foreground_image.shape
    if foreground_height > 0 and foreground_width > 0:
        background_image_resized = cv2.resize(background_image_from_url, (foreground_width, foreground_height))

        # Split the foreground image into color channels and alpha channel
        foreground_bgr = foreground_image[:, :, :3]
        alpha_mask = foreground_image[:, :, 3]

        # Convert alpha mask to 3 channels
        alpha_mask = cv2.cvtColor(alpha_mask, cv2.COLOR_GRAY2BGR)

        # Perform alpha blending
        foreground_float = foreground_bgr.astype(float)
        background_float = background_image_resized.astype(float)
        alpha_mask_float = alpha_mask.astype(float) / 255

        foreground_blended = cv2.multiply(alpha_mask_float, foreground_float)
        background_blended = cv2.multiply(1 - alpha_mask_float, background_float)
        output_image = cv2.add(foreground_blended, background_blended)

        output_image = output_image.astype(np.uint8)

        # Save the composite image
        cv2.imwrite('composite_image.png', output_image)
    else:
        print("Error: Invalid dimensions for foreground image.")
else:
    print("Error: Failed to fetch background image from URL.")

if os.path.exists(foreground_image_path):
    # Remove the image file
    os.remove(foreground_image_path)
    print(f"{foreground_image_path} removed successfully.")
else:
    print(f"{foreground_image_path} does not exist.")