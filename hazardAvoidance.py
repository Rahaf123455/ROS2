#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class hazardAvoidance(Node):
    def __init__(self): # publishes the symbol based on the vision and subscribes to the color topic
        super().__init__("hazardAvoidance")
        self.subscription=self.create_subscription(String,'/opencv',self.hazardAvoidance,10) 
        self.publisher=self.create_publisher(String,'/move',10)
    def hazardAvoidance(self,msg): 
        obstacleState, center, position, distance = msg.data.split(' ')
        dataVerfication=msg.data.split(' ')
        validPositions = ["LEFT", "RIGHT", "CENTER"]
        if len(dataVerfication)!=4:
            self.get_logger().warning(f"invalid obstacle position")
            return
        if position not in validPositions:
            self.get_logger().warning(f"invalid obstacle position")
            return
        if position == "LEFT":
            move = "RIGHT"
        elif position == "RIGHT":
            move = "LEFT"
        elif position == "CENTER":
            move = "RIGHT"
        msg = String()
        msg.data = move
        self.publisher.publish(msg)
def main(args=None):
    rclpy.init(args=args)
    node = hazardAvoidance()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()