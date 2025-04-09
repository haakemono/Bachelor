import cv2
import os

# Create directory to store images
save_dir = "guitar_dataset/images"
os.makedirs(save_dir, exist_ok=True)

# Start webcam
cap = cv2.VideoCapture(0)
count = 0

print("🎸 Press 's' to save an image. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Flip for mirror view
    cv2.imshow("Capture Guitar Images", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        img_path = os.path.join(save_dir, f"guitar_{count:03d}.jpg")
        cv2.imwrite(img_path, frame)
        print(f"✅ Saved: {img_path}")
        count += 1

    elif key == ord('q'):
        print("📁 Done capturing images.")
        break

cap.release()
cv2.destroyAllWindows()
