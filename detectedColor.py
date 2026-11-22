#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class detectedColor(Node):
    def __init__(self): # publishes detected color
        super().__init__("detectedColor")
        self.last_color = None
        self.publisher=self.create_publisher(String,'/Color',10)
        self.subscription=self.create_subscription(String,'/opencv',self.detectedColor,10)
    def detectedColor(self,msg):
        color = msg.data.strip().lower()
        validColors=["red","green","blue","yellow"]
        if not color or color not in validColors :
            self.get_logger().warning("no color accepted")
            self.last_color = None
            return
        msg = String()
        msg.data = color
        self.publisher.publish(msg)
def main(args=None):
    rclpy.init(args=args)
    node = detectedColor()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()