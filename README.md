# Bachelor
## About the project
## Getting started
### Download Instructions
In order to launch the games, navigate to the Launcher using
**cd Bachelor/Launcher** in Visual Studio Code.
Use the following command to install the needed packages:

**Windows/Linux**: pip install pygame mediapipe joblib tensorflow opencv-python python-chess scikit-learn

**Mac (Apple Silicion):** pip install pygame mediapipe joblib tensorflow-macos tensorflow-metal opencv-python python-chess scikit-learn

## Launcher
The launcher can be navigated using the arrow keys and pressing enter to start the games.

### Gesture Hero: 
When letters pop up on screen during gameplay, line your hand up with the camera and do the corresponding hand sign in American Sign Language.
Note that the terminal will give you a response on your current gesture.

The player or nurse/physiotherapist can add songs to the game by adding the mp3 file of the song to the music folder in the game structure. Then, for integrating the song into the game, they can update the songs.json file for linking the file path and giving the song a title in the title screen, while also linking the song to a certain beat map.  

To get the timing right, there should be around a three second gap until the desired melody starts. For the beat map, one should convert the BPM (beats per minute) of the song into milliseconds per beat. The formula for this will be:

60000⁄BPM

So, if the BPM is 130, as it is in our Level 2 song, it will be around 462 milliseconds per beat. This means that we should have an input every 462 milliseconds. If we skip beats in our song or if we want to add input for drums, synths or other sounds in the song, we can adjust manually. 



W.I.P: High score system, option to switch out letters on screen with actual hand symbols

### Apple Catcher:
Press space twice in order to start the game.
In game.py, there is a variable called "use_handtracking". Change this to 0 to enable object (handball) tracking. Having it on 1 makes it so the camera tracks your finger instead.

### Chess:
Navigate options menu with arrow keys
Stockfish has to be downloaded externally and path has to be specified in main.py (this is W.I.P and will be fixed)

Drawing game:

W.I.P but fundamentals work

## Documentation
[PyGame Documentation](https://www.pygame.org/docs/)  
[MediaPipe Documentation](https://developers.google.com/mediapipe/)  
[JobLib Documentation](https://joblib.readthedocs.io/en/stable/)  
[TensorFlow Documentation](https://www.tensorflow.org/api_docs)  
[OpenCV Documentation](https://docs.opencv.org/4.x/index.html)  
[Python Chess Documentation](https://python-chess.readthedocs.io/en/latest/)  
[scikit-learn Documentation](https://scikit-learn.org/stable/)  
