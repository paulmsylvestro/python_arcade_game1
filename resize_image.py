import sys
from PIL import Image

def resize_image(input_path, output_path, short_side):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            original_width, original_height = img.size
            if original_width < original_height:
                new_width = short_side
                new_height = int((short_side / original_width) * original_height)
            else:
                new_height = short_side
                new_width = int((short_side / original_height) * original_width)

            # Resize it (Using LANCZOS for high quality downsampling)
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Save it back out
            resized_img.save(output_path)
            print(f"Successfully resized '{input_path}' to {new_width}x{new_height} and saved as '{output_path}'.")
    except Exception as e:
        print(f"Error resizing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 resize_image.py <input.png> <output.png> <short_side_length>")
        print("Example: python3 resize_image.py assets/plane_raw.png assets/plane.png 64")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        target_short_side = int(sys.argv[3])
    except ValueError:
        print("Error: Short side length must be an integer value.")
        sys.exit(1)
        
    resize_image(input_file, output_file, target_short_side)
