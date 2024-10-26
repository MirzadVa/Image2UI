import cv2
import numpy as np
import pytesseract
import webbrowser
import os

# Read the image
image = cv2.imread('table_image.png')

# # Check if the image is loaded
if image is None:
    print("Error: Image not found.")
    exit()

# # Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Use Hough Line Transform to detect straight lines (using HoughLinesP for line segments)
lines = cv2.HoughLinesP(edges, 1, np.pi / 180,
                        threshold=100, minLineLength=30, maxLineGap=5)

# Draw the detected lines on the original image
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]  # Extract the endpoints of the line
        # Draw lines in green
        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


# # Find contours in the edge-detected image
contours, _ = cv2.findContours(
    edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# print("countours")
# print(contours)

# N = 3

textList = []

# Loop through each contour to check for text
for contour in contours:
    # Get the bounding box for each contour
    x, y, w, h = cv2.boundingRect(contour)

    # Extract the region of interest (ROI) from the original image
    roi = gray[y:y + h, x:x + w]

    # Use pytesseract to perform OCR on the ROI
    text = pytesseract.image_to_string(roi)

    # If text is found, draw the contour and print the text
    if text.strip():  # Check if the text is not just whitespace
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 120, 120),
                      2)  # Draw rectangle around contour
        splited = text.split()
        textList.insert(0, splited)


data = textList[0]
headers = data[:3]
rows = [data[i:i + 3] for i in range(3, len(data), 3)]

# Create HTML table
html_table = '<table border="1">\n'
# Add headers
html_table += '  <tr>\n'
for header in headers:
    html_table += f'    <th>{header}</th>\n'
html_table += '  </tr>\n'

# Add data rows
for row in rows:
    html_table += '  <tr>\n'
    for item in row:
        html_table += f'    <td>{item}</td>\n'
    html_table += '  </tr>\n'

html_table += '</table>'

# Print or save the HTML table

# Save HTML table to a file
file_path = 'table.html'
with open(file_path, 'w') as file:
    file.write(html_table)

# Open the HTML file in the default web browser
# Get the absolute file path
abs_path = os.path.abspath(file_path)
webbrowser.open(f'file://{abs_path}')
