import os
from PIL import Image, ImageTk

def load_piece_images(directory):
    """
    Load piece images from the assets directory.
    """
    pieces = {
        'r': 'br', 'n': 'bn', 'b': 'bb', 'q': 'bq', 'k': 'bk', 'p': 'bp',  # Black pieces
        'R': 'wr', 'N': 'wn', 'B': 'wb', 'Q': 'wq', 'K': 'wk', 'P': 'wp'   # White pieces
    }
    images = {}
    for piece, filename in pieces.items():
        file_path = os.path.join(directory, f"{filename}.png")
        if os.path.exists(file_path):
            images[piece] = ImageTk.PhotoImage(Image.open(file_path).resize((50, 50)))
        else:
            print(f"Missing image for piece: {filename}")
    return images
