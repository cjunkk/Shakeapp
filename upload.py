import requests
import base64
import qrcode

# Set API endpoint and headers
url = "https://api.imgur.com/3/image"
headers = {"Authorization": "Client-ID bd1de98fb9a0d89"}

# Read image file and encode as base64
with open("mosaic.png", "rb") as file:
  data = file.read()
  base64_data = base64.b64encode(data)

# Upload image to Imgur and get URL
response = requests.post(url, headers=headers, data={"image": base64_data})
url = response.json()["data"]["link"]
print(url)
qr = qrcode.QRCode(version=3, box_size=20, border=10, error_correction=qrcode.constants.ERROR_CORRECT_H)

# Define the data to be encoded in the QR code
data = url

# Add the data to the QR code object
qr.add_data(data)

# Make the QR code
qr.make(fit=True)

# Create an image from the QR code with a black fill color and white background
img = qr.make_image(fill_color="black", back_color="white")

# Save the QR code image
img.save("qr_code.png")