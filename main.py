from PIL import Image, ImageFilter, ImageChops, ImageEnhance
import numpy as np
import sys
import os

def apply_vignette(input_path, output_path):
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

    # Save the result
    img_with_blurred_borders.save(output_path)


def process_image(input_path, output_path):
    # Open an image file
    with Image.open(input_path) as img:
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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_image_path>")
    else:
        input_path = sys.argv[1]
        apply_vignette(input_path, 'test.jpg')
        process_image('test.jpg', input_path)
        os.remove('test.jpg')