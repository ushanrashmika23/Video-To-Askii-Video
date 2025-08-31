
"""
ASCII Video Player - Program Flow & Architecture

1. User launches the program.
2. Terminal UI (curses) displays a styled video selector:
    - Instructions, credits, and a list of video files from the 'video' folder.
    - User navigates with arrow keys, selects with Enter, or exits with 'q'.
3. Upon selection, the chosen video is played as ASCII art in the terminal:
    - Frames are converted to ASCII and displayed.
    - Audio is extracted and played in sync using simpleaudio.
    - User can quit playback at any time by pressing 'q'.

Key Components:
- select_video_file: Handles the curses-based UI for video selection.
- video_to_ascii: Converts video frames to ASCII and manages audio playback.
- frame_to_ascii: Converts a single video frame to ASCII art.
- Uses OpenCV for video, Pillow for image processing, simpleaudio for audio.
"""
import threading
import simpleaudio as sa
import simpleaudio as sa
from PIL import Image
import cv2
import os
import time
import curses

ASCII_CHARS = ["@","%", "#", "*", "+", "=", "-", ":", ".", " "]

def select_video_file(folder):
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.wmv'))]
    def curses_menu(stdscr):
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        selected = 0
        instructions = [
            " ASCII Video Player                       ",
            "────────────────────────────────────────────────────────────",
            "Instructions:",
            "  ↑/↓ : Move selection",
            "  Enter: Play selected video",
            "  q    : Quit selector (or exit during playback)",
            # "─────────────────────────────────────────────",
            "────────────────────────────────────────────────────────────",
            "Place your videos in the 'video' folder near the main.py.",
            ""
        ]
        credits_box = [
            " " * 60,
            # "+----------------------------------------------------------+",
            "| Credits: ushanrashmika23                              ",
            "| GitHub: github.com/ushanrashmika23                        ",
            # "+----------------------------------------------------------+",
            " " * 60
        ]
        while True:
            stdscr.clear()
            height, width = stdscr.getmaxyx()
            box_width = min(70, width-4)
            box_height = min(len(files)+len(instructions)+len(credits_box)+8, height-4)
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
            # Credits box
            for idx, line in enumerate(credits_box):
                stdscr.addstr(box_y+1+len(instructions)+idx, box_x+2, line, curses.A_DIM)
            # Video list title
            video_list_y = box_y+1+len(instructions)+len(credits_box)
            stdscr.addstr(video_list_y, box_x+2, "Video list:", curses.color_pair(2) | curses.A_BOLD)
            # File list or no files message
            if files:
                for idx, fname in enumerate(files):
                    line_y = video_list_y+1+idx
                    if line_y >= box_y+box_height-2:
                        break
                    name, ext = os.path.splitext(fname)
                    display_name = (name[:35] + '...' if len(name) > 35 else name) + ext
                    if idx == selected:
                        stdscr.addstr(line_y, box_x+4, "> " + display_name, curses.color_pair(1) | curses.A_REVERSE | curses.A_BOLD)
                    else:
                        stdscr.addstr(line_y, box_x+6, display_name)
            else:
                stdscr.addstr(video_list_y+2, box_x+4, "No video files found in folder.", curses.color_pair(3) | curses.A_BOLD)
            # Footer
            stdscr.addstr(box_y+box_height-2, box_x+2, "Press 'q' to exit.", curses.color_pair(3) | curses.A_BOLD)
            key = stdscr.getch()
            if files:
                if key == curses.KEY_UP and selected > 0:
                    selected -= 1
                elif key == curses.KEY_DOWN and selected < len(files)-1:
                    selected += 1
                elif key in [curses.KEY_ENTER, 10, 13]:
                    return files[selected]
            if key in [ord('q'), ord('Q')]:
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
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    alpha = 2.0
    beta = 0
    high_contrast = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
    inverted = cv2.bitwise_not(high_contrast)
    image = Image.fromarray(inverted)
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
            # Only show ASCII art and a charming exit instruction
            ascii_lines = ascii_art.split('\n')
            exit_line = "\n\nPress 'q' to quit playback"
            print("\n".join(ascii_lines) + exit_line)
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

# Usage
if __name__ == "__main__":
    video_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video")
    video_path = select_video_file(video_folder)
    if video_path:
        video_to_ascii(os.path.join(video_folder, video_path), new_width=90, fps_limit=30)
