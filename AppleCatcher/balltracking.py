import cv2
import numpy as np

class HoughBallTracker:
    def __init__(self):
        self.tracker = None
        self.tracking = False
        self.bbox = None

        # Your optimal values:
        self.min_radius = 20
        self.max_radius = 90
        self.param1 = 50
        self.param2 = 65
        self.min_dist = 39

    def detect_ball(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)

        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=self.min_dist,
            param1=self.param1,
            param2=self.param2,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )

        if circles is not None:
            circles = np.uint16(np.around(circles[0, :]))
            x, y, r = circles[0]
            x, y, r = int(x), int(y), int(r)
            bbox = (x - r, y - r, r * 2, r * 2)
            return bbox
        return None

    def initialize_tracker(self, frame, bbox):
        self.tracker = cv2.TrackerKCF_create()
        self.tracker.init(frame, bbox)
        self.tracking = True
        self.bbox = bbox

    def update_tracker(self, frame):
        success, bbox = self.tracker.update(frame)
        if success:
            self.bbox = bbox
            return True
        else:
            self.tracking = False
            self.tracker = None
            return False

    def draw_bbox(self, frame):
        if self.bbox:
            x, y, w, h = [int(v) for v in self.bbox]
            center_x = x + w // 2
            center_y = y + h // 2
            radius = int((w + h) / 4)
            cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 3)
            cv2.putText(frame, f"Ball at ({center_x},{center_y})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

def main():
    cap = cv2.VideoCapture(0)
    tracker = HoughBallTracker()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        if tracker.tracking:
            success = tracker.update_tracker(frame)
            if not success:
                bbox = tracker.detect_ball(frame)
                if bbox:
                    tracker.initialize_tracker(frame, bbox)
        else:
            bbox = tracker.detect_ball(frame)
            if bbox:
                tracker.initialize_tracker(frame, bbox)

        if tracker.tracking:
            tracker.draw_bbox(frame)

        cv2.imshow("Ball Tracker - Final Version", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
