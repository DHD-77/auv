import rclpy
from rclpy.node import Node
import cv2 # This is OpenCV
from cv_bridge import CvBridge # This is the translator
import numpy as np

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')
        self.bridge = CvBridge()
        
        # Open the webcam (0 is usually the built-in camera)
        self.cap = cv2.VideoCapture(0)
        
        # Create a timer that runs 30 times per second (30 FPS)
        self.timer = self.create_timer(1.0/30.0, self.timer_callback)

    def timer_callback(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # 1. Convert to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 2. Define the range for RED color
        
        low_green = np.array([40, 100, 100])
        high_green = np.array([90, 255, 255])
        
        # 3. Create the Mask
        mask = cv2.inRange(hsv_frame, low_green, high_green)

        # 4. Find the center (Moments)
        M = cv2.moments(mask)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            
            # Draw a circle on the object so you know it's working
            cv2.circle(frame, (cX, cY), 20, (0, 255, 0), -1)
            self.get_logger().info(f"Object found at X: {cX}")
        else:
            self.get_logger().info("Object LOST")

        width = frame.shape[1]
        if M["m00"] > 1000:
            cX = int(M["m10"] / M["m00"])
            if cX < width // 3:
                processed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                msg = "LEFT: Grayscale"
            elif cX < 2 * (width//3):
                processed = frame
                msg = "CENTER: Normal"
            else:
                processed = cv2.Canny(frame, 100, 200)
                msg = "RIGHT: Canny"
        else:
            processed = cv2.bitwise_not(frame)
            msg = "LOST: Negative"

        cv2.putText(processed, msg, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow("Final Result", processed)
        cv2.waitKey(1)
        


       
        

def main(args=None):
    rclpy.init(args=args)
    node = VisionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.cap.release()
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()