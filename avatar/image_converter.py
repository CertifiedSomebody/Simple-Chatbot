from PIL import Image
import os

input_folder = "avatar/"
output_folder = "avatar_converted/"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".jpeg", ".webp")):  # Check for JPG or WEBP files
        img = Image.open(os.path.join(input_folder, filename))
        new_filename = os.path.splitext(filename)[0] + ".png"  # Change extension to .png
        img.save(os.path.join(output_folder, new_filename), "PNG")  # Convert to PNG

print("Conversion complete! Check the 'avatar_converted' folder.")
