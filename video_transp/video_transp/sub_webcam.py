
import rclpy
import numpy as np
from rclpy.node import Node
from sensor_msgs.msg  import Image
from cv_bridge import CvBridge
import cv2

lower_red = np.array([0, 90, 128])
upper_red = np.array([180, 255, 255])


class ImageSubscriber(Node):
    def __init__(self, name):
        super().__init__(name)
        self.sub = self.create_subscription(
            Image, "image_raw", self.listener_callback, 10
        )
        self.cv_bridge = CvBridge()

    def detect_red_object(self, image):
        hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask_red = cv2.inRange(hsv_img, lower_red, upper_red)
        contours, hierarchy = cv2.findContours(
            mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE
        )


        cts = []
        for cnt in contours:
            if cnt.shape[0] < 150:
                continue
            (x,y,w,h) = cv2.boundingRect(cnt)
            cts.append((x+w/2,y+h/2))

            # xc = x+w/2
            # yc = y+h/2
            # self.get_logger().info(f"find_center:({xc}, {yc})")

            # cv2.drawContours(image, [cnt], -1, (0,255,0), 2)
            # cv2.circle(image, (int(x+w/2)),int(y+h/2), 5)
            # cv2.circle(image, (int(x+w/2),int(y+h/2)), 5, (255,0,0), -1)
        self.get_logger().info(f"receiving && caculate centers:{cts}")
        # cv2.imshow("object",image)
        # cv2.waitKey(10)

    def listener_callback(self, data):
        # self.get_logger().info("receiving video frame")
        image = self.cv_bridge.imgmsg_to_cv2(data, "bgr8")
        self.detect_red_object(image)


def main(args=None):
    rclpy.init(args=args)
    node = ImageSubscriber("image_sub")
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


# main()



