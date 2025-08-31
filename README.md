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
- [OpenCV](https://pypi.org/project/opencv-python/)
- [Pillow](https://pypi.org/project/Pillow/)
- [simpleaudio](https://pypi.org/project/simpleaudio/)
- [windows-curses](https://pypi.org/project/windows-curses/) (Windows only)
- [ffmpeg](https://ffmpeg.org/) (must be installed and in PATH)

## Credits
- Author: ushanrashmika23
- GitHub: [github.com/ushanrashmika](https://github.com/ushanrashmika23)

## License
MIT
