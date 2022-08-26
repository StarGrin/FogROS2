
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
# import time
# import numpy as np
# from learning_interface.msg import ObjectPosition

class ImagePublisher(Node):
    def __init__(self, name):
        super().__init__(name)
        self.publisher_ = self.create_publisher(Image, "image_raw", 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.cap = cv2.VideoCapture(4)
        self.cv_bridge = CvBridge()

    def timer_callback(self):
        ret, frame = self.cap.read()

        if ret == True:
            self.publisher_.publish(
                self.cv_bridge.cv2_to_imgmsg(frame, "bgr8")
            )
        
        self.get_logger().info("publish video frame")

def main(args=None):
    rclpy.init(args=args)
    node = ImagePublisher("image_pub")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

# main()

# import sub_webcam
# import threading
# tp = threading.Thread(target=main())
# ts = threading.Thread(target=sub_webcam.main())
# tp.start()
# ts.start()
