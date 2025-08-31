# ASCII Video Player

A terminal-based Python application that converts videos to ASCII art and plays synchronized audio. Features a modern, interactive UI for video selection and playback.

## Features
- Converts video frames to ASCII art in real time
- Synchronized audio playback using `simpleaudio`
- Modern terminal UI for video selection (curses-based)
- Easy navigation: arrow keys, Enter to select, 'q' to quit
- Credits and GitHub link displayed in UI

## How It Works
1. Place your video files (`.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`) in the `video` folder next to `main.py`.
2. Run the program:
   ```
   python main.py
   ```
3. Use the arrow keys to select a video and press Enter to play.
4. Watch the video as ASCII art in your terminal, with audio.
5. Press 'q' at any time to quit playback or exit the selector.

## Architecture Overview
- **select_video_file**: Curses-based UI for interactive video selection.
- **video_to_ascii**: Converts video frames to ASCII and manages audio playback.
- **frame_to_ascii**: Converts a single video frame to ASCII art.
- Uses OpenCV for video, Pillow for image processing, and simpleaudio for audio.


## Requirements
- Python 3.10+
- All Python dependencies are listed in `requirements.txt`:
   - opencv-python
   - Pillow
   - simpleaudio
   - windows-curses (Windows only)
   - ffmpeg-python
- [ffmpeg](https://ffmpeg.org/) (must be installed and in PATH)

## Configuration Tutorial

1. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Install ffmpeg:**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html) and follow platform instructions.
   - Add ffmpeg to your system PATH so it can be called from the terminal.

3. **Prepare your videos:**
   - Place your video files (`.mp4`, `.avi`, `.mov`, `.mkv`, `.wmv`) in the `video` folder next to `main.py`.

4. **Run the program:**
   ```
   python main.py
   ```

5. **Usage:**
   - Use arrow keys to select a video, Enter to play, 'q' to quit.
   - ASCII art and audio will play in your terminal.

## Credits
- Author: ushanrashmika =23
- GitHub: [github.com/ushanrashmika](https://github.com/ushanrashmika)

## License
MIT
