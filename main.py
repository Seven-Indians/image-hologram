from PIL import Image, ImageFilter, ImageChops, ImageEnhance
import numpy as np
import customtkinter as ctk
from customtkinter import filedialog

def apply_vignette(input_path):
    # Open the input image
    img = Image.open(input_path).convert("RGB")
    width, height = img.size

    # Create a vignette mask
    vignette = Image.new("L", (width, height), 0)
    for x in range(width):
        for y in range(height):
            # Calculate distance to the center
            dx = x - width / 2
            dy = y - height / 2
            distance = np.sqrt(dx**2 + dy**2)
            # Normalize distance and apply a quadratic falloff
            max_distance = np.sqrt((width / 2)**2 + (height / 2)**2)
            vignette.putpixel((x, y), int(255 * (1 - (distance / max_distance)**2)))

    # Apply Gaussian blur to the vignette mask for smoother effect
    vignette = vignette.filter(ImageFilter.GaussianBlur(100))

    # Convert the vignette mask to RGB mode
    vignette_rgb = Image.merge("RGB", (vignette, vignette, vignette))

    # Use the multiply method to apply the vignette effect
    img_with_vignette = ImageChops.multiply(img, vignette_rgb)

    # Create a blurred version of the image
    blurred_img = img.filter(ImageFilter.GaussianBlur(0))

    # Combine the original image and the blurred image using the vignette mask
    img_with_blurred_borders = Image.composite(blurred_img, img_with_vignette, vignette)

    # Enhance the brightness and contrast of the image
    enhancer = ImageEnhance.Brightness(img_with_blurred_borders)
    img_with_blurred_borders = enhancer.enhance(1.5)

    # return the image with the vignette effect
    return img_with_blurred_borders

def process_image(img, output_path):
    # Create a new image with a 16:9 aspect ratio and black background
    width, height = 1920, 1080
    new_img = Image.new("RGBA", (width, height), "black")

    # Resize the image
    img = img.resize((360, 360), Image.LANCZOS)

    # Rotate the image and paste it into the new image
    for angle in [0, 90, 180, 270]:
        rotated_img = img.rotate(angle)
        if rotated_img.mode != 'RGBA':
            rotated_img = rotated_img.convert('RGBA')
        if angle == 90:
            x_offset = 985-540
            y_offset = 540-180
        elif angle == 180:
            x_offset = 985-180
            y_offset = 540+180
        elif angle == 270:
            x_offset = 985+180
            y_offset = 540-180
        else:
            x_offset = 985-180
            y_offset = 0
        new_img.paste(rotated_img, (x_offset, y_offset), rotated_img)

    # Convert the new image to RGB mode before saving
    new_img = new_img.convert('RGB')
    new_img.save(output_path)

def select_image():
    root = ctk.CTk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    return file_path

def save_image():
    root = ctk.CTk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(
        title="Save Image As",
        defaultextension=".jpg",
        filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("BMP files", "*.bmp"), ("TIFF files", "*.tiff")]
    )
    return file_path

if __name__ == "__main__":
    input_path = select_image()
    temp = apply_vignette(input_path)
    output_path = save_image()
    process_image(temp, output_path)