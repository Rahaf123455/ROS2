#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class modeDetermination(Node):
    def __init__(self):
        super().__init__("modeDetermination")
        self.subscription=self.create_subscription(String,'/position',self.modeDetermination,10) 
        self.publisher=self.create_publisher(String,'/modeDetermined',10)    #get position and publish the new mode
        self.currentMode=""
    def modeDetermination(self,msg): 
        position = msg.data
        if position == "top-left" or position=="top-right":
            mode = "RTL"
        elif position == "bottom-left" or position=="bottom-right":
            mode = "AUTO"
        else:
            return
        if self.currentMode==mode:
            return
        msg = String()
        msg.data = mode #publish mode in modeDetermination topic
        self.publisher.publish(msg)
        self.currentMode=mode
def main(args=None):
    rclpy.init(args=args)
    node = modeDetermination()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
