import os
from PIL import Image

def process_image(input_path, img_output, bin_output):
    with Image.open(input_path) as img:
        new_width = 40
        new_height = int(new_width * 3 / 4)
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)

        left = 0
        top = max(0, (new_height - 20) // 2)
        right = new_width
        bottom = top + 20
        cropped_img = resized_img.crop((left, top, right, bottom))

        # Step 3: Apply a black and white filter with thresholding
        # Convert the image to grayscale first
        grayscale_img = cropped_img.convert("L")
        
        # Apply a threshold to get a binary image
        threshold = 128  # You can adjust the threshold as needed
        bw_img = grayscale_img.point(lambda p: p > threshold and 255)

        pixels = list(bw_img.getdata())
        byte_array = bytearray(0xFF if pixel else 0x00 for pixel in pixels)

        bw_img.save(img_output)

        with open(bin_output, 'wb') as f:
            f.write(byte_array)

def process_images_in_folder(input_folder, img_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                img_dir = os.path.join(img_folder, relative_path)

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                if not os.path.exists(img_dir):
                    os.makedirs(img_dir)

                output_file_name = os.path.splitext(file)[0]
                output_path = os.path.join(output_dir, output_file_name)
                img_output_file_name = os.path.splitext(file)[0]
                img_output_path = os.path.join(img_dir, f"{img_output_file_name}.png")
                process_image(input_path, img_output_path, output_path)

if __name__ == "__main__":
    input_folder = './origin_frames'
    img_output = './frames'
    bin_output = './frame_data'

    process_images_in_folder(input_folder, img_output, bin_output)
