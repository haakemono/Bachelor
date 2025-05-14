# Gesture Games (Bachelor Project)

##  About the Project  
This project explores gesture recognition and hand tracking to create accessible and engaging games. The system includes a launcher and multiple interactive games that respond to hand gestures and movement using computer vision and machine learning.

Built with:
- Python  
- OpenCV  
- MediaPipe  
- TensorFlow  
- PyGame  


### Prerequisites
- Python 3.9 or greater
- pip
- Visual Studio Code

---
## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Bachelor.git
cd Bachelor
```

### 2. Install Dependencies

**Windows/Linux:**

```bash
pip install pygame mediapipe joblib tensorflow opencv-python python-chess scikit-learn
```

**macOS (Apple Silicon):**

```bash
pip install pygame mediapipe joblib tensorflow-macos tensorflow-metal opencv-python python-chess scikit-learn
```

### 3. Launch the Game Suite

```bash
cd Launcher
python main.py
```

---

## Launcher Instructions

Use the **arrow keys** to navigate the launcher menu.  
Press **Enter** to start the selected game.

---

## Games

### Gesture Hero

When letters pop up on screen during gameplay, line your hand up with the camera and make the corresponding hand sign in American Sign Language (ASL).

The terminal will show feedback on your current gesture.

#### Adding Custom Songs

You can add your own songs by doing the following:

1. Place your `.mp3` file in the `music/` folder.
2. Open the `songs.json` file and add a new entry:
   - Set the file path
   - Set the song title (as shown on the title screen)
   - Link the song to a beat map

#### Beat Map Timing

To sync the song to gameplay:
- Wait around **3 seconds** before the melody starts.
- Use this formula to calculate beat interval:

```
Milliseconds per beat = 60000 / BPM
```

**Example:**  
If your song has a BPM of 130:  
`60000 / 130 = ~462 milliseconds per beat`

You can customize the timing or skip beats to match different instruments (e.g. drums, synths).

#### Work in Progress:
- High score system  
- Option to show hand symbols instead of letters  

---

### Apple Catcher

- Press **spacebar twice** to start the game.
- In `game.py`, locate the `use_handtracking` variable:
  - Set to `1` for finger tracking.
  - Set to `0` for object tracking (e.g., a small ball in your hand).

---

### Chess

- Use arrow keys to navigate the options menu.
- Requires the **Stockfish chess engine**:
  - Download it from [https://stockfishchess.org/download/](https://stockfishchess.org/download/)
  - Set the correct file path in `main.py` under the `engine_path` variable.

This process will be automated in a future update.

---

### Drawing Game

This is still a work in progress, but basic hand-tracked drawing functionality works.

---

## Project Structure

```
Bachelor/
│
├── Launcher/
│   ├── apple_catcher/
│   │   ├── __pycache__/
│   │   ├── img/
│   │   ├── templates/
│   │   ├── constants.py
│   │   ├── difficulty_manager.py
│   │   ├── game.py
│   │   ├── main.py
│   │   └── render_logic.py
│   │
│   ├── assets/
│   │   ├── apple_catcher.png
│   │   ├── chess.png
│   │   ├── draw_game.png
│   │   └── gesture_hero.png
│   │
│   ├── chess/
│   │   ├── __pycache__/
│   │   ├── assets/
│   │   ├── stockfish/
│   │   ├── chessboard.py
│   │   ├── engine.py
│   │   ├── gesture_recognition.py
│   │   └── main.py
│   │
│   ├── draw_game/
│   │   ├── __pycache__/
│   │   └── draw_game.py
│   │
│   ├── gesture_hero/
│   │   ├── __pycache__/
│   │   ├── assets/
│   │   ├── beatmaps/
│   │   ├── music/
│   │   ├── constants.py
│   │   ├── game_logic.py
│   │   ├── gesture_input.py
│   │   ├── main.py
│   │   ├── render.py
│   │   └── songs.json
│   │
│   ├── shared_input/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── gesture_hand_tracking.py
│   │   ├── gesture_recognition_model.pkl
│   │   ├── gesture.py
│   │   ├── label_encoder.pkl
│   │   ├── scaler.pkl
│   │   └── tracking.py
│   │
│   └── launcher.py
│
├── Neural_network setup/
│   ├── sign_language_data.csv
│   └── train_model.py
│
├── .gitmodules
├── README.md
└── Untitled.ipynb
```
## Gameplay tutorials

### signlaguage used

### Video tutorials of the gameplay


---

## Documentation and Resources

- [PyGame Documentation](https://www.pygame.org/docs/)  
- [MediaPipe Documentation](https://developers.google.com/mediapipe/)  
- [JobLib Documentation](https://joblib.readthedocs.io/en/stable/)  
- [TensorFlow Documentation](https://www.tensorflow.org/api_docs)  
- [OpenCV Documentation](https://docs.opencv.org/4.x/index.html)  
- [Python Chess Documentation](https://python-chess.readthedocs.io/en/latest/)  
- [scikit-learn Documentation](https://scikit-learn.org/stable/)  
