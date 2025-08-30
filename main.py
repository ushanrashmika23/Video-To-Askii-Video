

from PIL import Image
import cv2
import os
import time

ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def grayify(image):
    return image.convert("L")  # convert to grayscale

def pixels_to_ascii(image):
    pixels = image.getdata()
    ascii_chars = [ASCII_CHARS[pixel // 25] for pixel in pixels]
    return ascii_chars

def image_to_ascii(path, new_width=100):
    try:
        image = Image.open(path)
    except Exception as e:
        print("Unable to open image:", e)
        return
    
    image = resize_image(image, new_width)
    image = grayify(image)

    ascii_chars = pixels_to_ascii(image)
    rows = [" ".join(ascii_chars[i:(i+new_width)]) for i in range(0, len(ascii_chars), new_width)]
    ascii_img = "\n".join(rows)
    return ascii_img

def frame_to_ascii(frame, new_width=100):
    # Convert OpenCV frame (BGR) to PIL Image (keep original colors)
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    # Convert to grayscale for ASCII mapping
    image = grayify(image)
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    image = image.resize((new_width, new_height))
    ascii_chars = pixels_to_ascii(image)
    rows = [" ".join(ascii_chars[i:(i+new_width)]) for i in range(0, len(ascii_chars), new_width)]
    ascii_img = "\n".join(rows)
    return ascii_img

def video_to_ascii(video_path, new_width=100, fps_limit=30):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Unable to open video: {video_path}")
        return
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow('Video Preview (Original)', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ascii_art = frame_to_ascii(frame, new_width)
            os.system('cls' if os.name == 'nt' else 'clear')
            print(ascii_art)
            time.sleep(1.0 / fps_limit)
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Example usage
if __name__ == "__main__":
    video_path = "sobana.mp4"  # replace with your video file
    video_to_ascii(video_path, new_width=100, fps_limit=30)
