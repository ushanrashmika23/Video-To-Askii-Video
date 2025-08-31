
import threading
import simpleaudio as sa
import simpleaudio as sa
from PIL import Image
import cv2
import os
import time
import curses

ASCII_CHARS = ["@", "%", "#", "*", "+", "=", "-", ":", ".", " "]

def select_video_file(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wmv'))]
    if not files:
        print("No video files found in folder.")
        return None
    def curses_menu(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        selected = 0
        instructions = [
            "[ ASCII Video Player - Metasploit Style UI ]",
            "─────────────────────────────────────────────",
            "Instructions:",
            "  ↑/↓ : Move selection",
            "  Enter: Play selected video",
            "  q    : Quit selector (or exit during playback)",
            "─────────────────────────────────────────────",
            "Place your videos in the 'video' folder near the main.py.",
            ""
        ]
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            box_width = min(70, width-4)
            box_height = min(len(files)+len(instructions)+6, height-4)
            box_y = (height - box_height) // 2
            box_x = (width - box_width) // 2
            # Draw ASCII box border
            stdscr.addstr(box_y, box_x, "┌" + "─"*(box_width-2) + "┐", curses.color_pair(2) | curses.A_BOLD)
            for i in range(1, box_height-1):
                stdscr.addstr(box_y+i, box_x, "│" + " "*(box_width-2) + "│", curses.color_pair(2))
            stdscr.addstr(box_y+box_height-1, box_x, "└" + "─"*(box_width-2) + "┘", curses.color_pair(2) | curses.A_BOLD)
            # Title and instructions
            for idx, line in enumerate(instructions):
                stdscr.addstr(box_y+1+idx, box_x+2, line, curses.color_pair(2) | curses.A_BOLD if idx==0 else curses.A_DIM)
            # File list
            for idx, fname in enumerate(files):
                line_y = box_y+len(instructions)+2+idx
                if line_y >= box_y+box_height-2:
                    break
                if idx == selected:
                    stdscr.addstr(line_y, box_x+4, "> " + fname, curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD)
                else:
                    stdscr.addstr(line_y, box_x+6, fname)
            # Footer
            stdscr.addstr(box_y+box_height-2, box_x+2, "Press 'q' to exit.", curses.color_pair(3) | curses.A_BOLD)
            key = stdscr.getch()
            if key == curses.KEY_UP and selected > 0:
                selected -= 1
            elif key == curses.KEY_DOWN and selected < len(files)-1:
                selected += 1
            elif key in [curses.KEY_ENTER, 10, 13]:
                return files[selected]
            elif key in [ord('q'), ord('Q')]:
                return None
    return curses.wrapper(curses_menu)

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
    # --- AUDIO EXTRACTION AND PLAYBACK ---
    # Extract audio from video using ffmpeg (WAV format for compatibility)
    audio_path = "_temp_audio.wav"
    extract_cmd = f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ar 44100 -ac 2 "{audio_path}"'
    os.system(extract_cmd)

    # Play audio in a separate thread using simpleaudio
    stop_audio_event = threading.Event()
    def play_audio():
        try:
            wave_obj = sa.WaveObject.from_wave_file(audio_path)
            play_obj = wave_obj.play()
            while play_obj.is_playing():
                if stop_audio_event.is_set():
                    play_obj.stop()
                    break
                time.sleep(0.05)
        except Exception as e:
            print(f"Audio playback error: {e}")

    audio_thread = threading.Thread(target=play_audio)
    audio_thread.daemon = True  # Ensure thread exits with main program
    audio_thread.start()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Unable to open video: {video_path}")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        return
        return
    import msvcrt
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            ascii_art = frame_to_ascii(frame, new_width)
            os.system('cls' if os.name == 'nt' else 'clear')
            # Add a 3-line exit banner at the bottom
            ascii_lines = ascii_art.split('\n')
            banner_width = new_width * 2
            exit_banner = [
                "=" * banner_width,
                "||   PRESS 'q' TO EXIT PLAYBACK   ||".center(banner_width),
                "=" * banner_width
            ]
            print("\n".join(ascii_lines + exit_banner))
            # Check for 'q' key press to exit
            if msvcrt.kbhit():
                key = msvcrt.getch()
                if key in [b'q', b'Q']:
                    print("Exiting...")
                    stop_audio_event.set()
                    break
            time.sleep(1.0 / fps_limit)
    finally:
        cap.release()
        audio_thread.join()
        if os.path.exists(audio_path):
            os.remove(audio_path)

# Example usage
if __name__ == "__main__":
    video_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video")
    video_path = select_video_file(video_folder)
    if video_path:
        video_to_ascii(os.path.join(video_folder, video_path), new_width=100, fps_limit=30)
