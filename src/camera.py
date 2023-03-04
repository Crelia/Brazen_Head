import cv2

class Camera:
    def __init__(self):
        # Set up the camera
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # Create a window to display the camera image
        cv2.namedWindow("Camera")
    
    def capture_image(self):
        # Capture an image from the camera
        ret, frame = self.cap.read()
        # Convert the image to grayscale for face detection (optional)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Display the image in the window
        cv2.imshow("Camera", frame)
        # Return the grayscale image
        return gray
    
    def release(self):
        # Release the camera and destroy the window when finished
        self.cap.release()
        cv2.destroyAllWindows()
