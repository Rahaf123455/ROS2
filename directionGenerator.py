#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64
from rclpy.qos import QoSProfile, ReliabilityPolicy

class directionGenerator(Node):
    def __init__(self):
        super().__init__("directionGenerator")
        qos = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT
)

        self.create_subscription(
    Float64,
    '/mavros/global_position/compass_hdg',
        self.heading_callback,
    qos
)
        self.move_subscription = self.create_subscription(String,'/move',self.directionGenerator,10)
        self.heading = None

    def heading_callback(self, msg):
        self.heading = msg.data
    def directionGenerator(self, msg):
        target_heading = target_heading%360
        hazardPosition = msg.data
        if not self.heading:
            self.get_logger().warning("no heading recieved yet")
            return
        if hazardPosition == "LEFT":
            target_heading = self.heading - 30
        elif hazardPosition == "RIGHT":
            target_heading = self.heading + 30
        else:
            self.get_logger().warning("invalid direction")
            return

def main(args=None):
    rclpy.init(args=args)
    node = directionGenerator()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == "__main__":
    main()