#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from mavros_msgs.srv import SetMode
class decisionEngine(Node):
    def __init__(self): # publishes the decided mode to topic mode and subscribes to the file that sends the symbol 
        super().__init__("decisionEngine")
        self.mode_client = self.create_client(SetMode,'/mavros/set_mode')
        self.subscription=self.create_subscription(String,'/symbol',self.flightModeChoice,10)
        self.publisher=self.create_publisher(String,'/decision',10)
        self.currentSymbol = ""
    def flightModeChoice(self,msg): # this decides the mode depending on the incoming data from symbol topic
        opencvSymbol=msg.data.strip()
        self.get_logger().info(f"Received:{opencvSymbol}")
        if opencvSymbol != self.currentSymbol:
            if opencvSymbol=='R':
                mode = "RTL"
            elif opencvSymbol=='A':
                mode="Auto"
            elif opencvSymbol=='M':
                mode="MANUAL"
            elif opencvSymbol=='F':
                mode="FBWA"
            else:
                self.get_logger().warning(f"Invalid symbol received: {opencvSymbol}")
                return
        else:
            return
        self.currentSymbol = opencvSymbol
        msg = String()
        msg.data = mode
        self.publisher.publish(msg)
        self.get_logger().info(f"mode: {mode}")
        self.changeMode(mode)

    def changeMode(self, mode): # sends the request to mavros to send it to sitl and the function is called above
        request=SetMode.Request()
        request.base_mode=0
        request.custom_mode=mode
        self.mode_client.call_async(request)

def main(args=None):
    rclpy.init(args=args)
    node = decisionEngine()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
