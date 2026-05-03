import sys
from PIL import Image

def resize_image(input_path, output_path, width, height):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            # Resize it (Using LANCZOS for high quality downsampling)
            resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
            # Save it back out
            resized_img.save(output_path)
            print(f"Successfully resized '{input_path}' to {width}x{height} and saved as '{output_path}'.")
    except Exception as e:
        print(f"Error resizing image: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 resize_image.py <input.png> <output.png> <width> <height>")
        print("Example: python3 resize_image.py assets/plane_raw.png assets/plane.png 64 64")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    try:
        target_width = int(sys.argv[3])
        target_height = int(sys.argv[4])
    except ValueError:
        print("Error: Width and height must be integer values.")
        sys.exit(1)
        
    resize_image(input_file, output_file, target_width, target_height)
