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
- Python 3.9 is recommended
- pip
- Visual Studio Code (not nescessary but highly recommended)

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
pip install pygame mediapipe joblib tensorflow opencv-python python-chess scikit-learn numpy
```

**macOS (Apple Silicon):**

```bash
pip install pygame mediapipe joblib tensorflow-macos tensorflow-metal opencv-python python-chess scikit-learn numpy
```

### 3. Launch the Game Suite

```bash
cd Launcher
python main.py
```

---
### 4. Install Stockfish
In order to get the Chess game to work one has to install [Stockfish](https://stockfishchess.org/download/) seperately.
* After downloading, unzip the folder
* Locate the "stockfish" folder wherever it was unzipped
* Copy the contents of this folder and paste in Bachelor/Launcher/chess/stockfish in the source code.
* One may still get a malware error on MacOS when launching Chess. This is solved by going into Settings>Privacy and Security>Security and pressing allow on Stockfish.
___  
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

To sync the added song to gameplay:
- Make sure there is a 3 second gap from when the mp3 file starts playing to the first beat
- Use this formula to calculate beat interval:

```
Milliseconds per beat = 60000 / BPM
```

**Example:**  
If your song has a BPM of 130:  
`60000 / 130 = ~462 milliseconds between beats`

You can customize the timing or skip beats to match different instruments (e.g. drums, synths).

---

### Apple Catcher

- Press **spacebar twice** to start the game.
- If you want to change trackinng mode, in `game.py`, locate the `use_handtracking` variable:
  - Set to `1` for finger tracking (default).
  - Set to `0` for object tracking (e.g., a small ball in your hand).

---

### Chess

- Use arrow keys to navigate the options menu.
- In the Chess game, the pieces are controlled on the board through gesture recognition. The squares on the board are selected by performing two separate gestures. The first gesture will select a column and the second selects a row. After the square with the desired piece has been selected, the player repeats the process to choose destination square.
- Current gesture information can be found in the terminal
---

### Drawing Game

Make the ASL sign for:

* F to start drawing
* L to stop drawing
* A to switch color to red
* B to switch color to blue
* C to switch color to green
* E to equip the eraser
* D to clear the canvas

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
│   │   ├── stockfish/ (Place content of zip file in here)
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

### Gestures used
![Gestures](https://github.com/user-attachments/assets/1b6520c1-637b-4f80-9fb9-228c4ce3cc54)


### Video tutorials of the gameplay  

- [Video Demonstration of Chess](https://youtu.be/c6FOaJa5Ivw)  
- [Video Demonstration of Gesture Hero](https://youtu.be/CdLEewWx-nU)  
- [Video Demonstration of Draw Game](https://youtu.be/D5UQdGqIIBw)  
- [Video Demonstration of Apple Catcher](https://youtu.be/iReqirHHHMs)
- [Video Demonstration of Apple Catcher (Ball Tracking)](https://youtu.be/XaR_7jP8GpA)
---

## Licenses

- [PyGame License](https://www.pygame.org/docs/LGPL.txt)  
- [MediaPipe License](https://github.com/joblib/joblib/blob/main/LICENSE.txt)  
- [JobLib License](https://joblib.readthedocs.io/en/stable/)  
- [TensorFlow License](https://github.com/tensorflow/examples/blob/master/LICENSE)  
- [OpenCV License](https://github.com/opencv/opencv/blob/4.x/LICENSE)  
- [Python Chess License](https://github.com/niklasf/python-chess/blob/master/LICENSE.txt)  
- [scikit-learn License](https://github.com/SciSharp/scikit-learn.net/blob/master/LICENSE)  
- [Stockfish License](https://github.com/official-stockfish/Stockfish/blob/master/Copying.txt)
- [NumPy License](https://numpy.org/doc/stable/license.html)
- [Keras License](https://github.com/keras-team/keras/blob/master/LICENSE)
- [Python License](https://docs.python.org/3/license.html#)
- [JSON License](https://www.json.org/license.html)
