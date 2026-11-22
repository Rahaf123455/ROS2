#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class stateInterpretation(Node):
    def __init__(self): # publishes the symbol based on the vision and subscribes to the color topic
        super().__init__("stateinterpretation")
        self.subscription=self.create_subscription(String,'/Color',self.mapColor,10) 
        self.publisher=self.create_publisher(String,'/symbol',10)
    def mapColor(self,msg): # this decides or maps the symbol depending on the incoming data from opencv
        color=msg.data
        if not color:
            self.get_logger().warning("no color received")
            return
        if color=='green':
            symbol='A'
        elif color=='red':
            symbol='M'
        elif color=='blue':
            symbol='F'
        elif color=='yellow':
            symbol='R'
        else:
            self.get_logger().warning("Invalid color received")
            return
        msg = String()
        msg.data = symbol
        self.publisher.publish(msg)
        self.get_logger().info(f"symbol: {symbol}")

def main(args=None):
    rclpy.init(args=args)
    node = stateInterpretation()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()