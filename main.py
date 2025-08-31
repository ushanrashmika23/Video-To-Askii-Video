import threading
from playsound import playsound
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
    ascii_chars = [ASCII_CHARS[int(pixel / 255 * (len(ASCII_CHARS) - 1))] for pixel in pixels]
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
    # Convert OpenCV frame (BGR) to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Increase contrast to maximum
    alpha = 2.0  # Contrast control (1.0-3.0+)
    beta = 0     # Brightness control (0-100)
    high_contrast = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    # Convert to PIL Image
    image = Image.fromarray(high_contrast)
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    image = image.resize((new_width, new_height))
    ascii_chars = pixels_to_ascii(image)
    rows = [" ".join(ascii_chars[i:(i+new_width)]) for i in range(0, len(ascii_chars), new_width)]
    ascii_img = "\n".join(rows)
    return ascii_img

def video_to_ascii(video_path, new_width=100, fps_limit=30):
    # Extract audio from video using ffmpeg
    audio_path = "_temp_audio.wav"
    # Always extract audio to ensure it's up to date
    os.system(f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_path}"')

    # Play sound in a separate thread
    def play_audio():
        playsound(audio_path)

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.start()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Unable to open video: {video_path}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return
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
        audio_thread.join()
        if os.path.exists(audio_path):
            os.remove(audio_path)

# Example usage
if __name__ == "__main__":
    video_path = "sobana.mp4"  # replace with your video file
    video_to_ascii(video_path, new_width=100, fps_limit=30)
