#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from mavros_msgs.msg import State
from mavros_msgs.srv import SetMode
class changeMode(Node):
    def __init__(self):
        super().__init__("changeMode")
        self.subscription = self.create_subscription(String,'/modeDetermined',self.changeMode,10)
        self.stateSubscription = self.create_subscription(State,'/mavros/state',self.stateCallback,10)
        self.modeClient = self.create_client(SetMode,'/mavros/set_mode')
        self.currentMode = ""
        self.lastRequestedMode = ""
        self.requestInProgress = False
        self.get_logger().info("Flight node started")
    def stateCallback(self, msg):
        self.currentMode = msg.mode
    def changeMode(self, msg):
        mode = msg.data
        if mode == self.lastRequestedMode:
            return
        if self.requestInProgress:
            return
        if not self.modeClient.service_is_ready():
            self.get_logger().warning("/mavros/set_mode service is not available")
            return
        self.lastRequestedMode = mode
        self.requestInProgress = True
        request = SetMode.Request()
        request.custom_mode = mode
        self.get_logger().info(f"Sending mode request: {mode}")
        future = self.modeClient.call_async(request)
        future.add_done_callback(self.modeChangeResponse)
    def modeChangeResponse(self, future):
        self.requestInProgress = False
        try:
            response = future.result()
            if response.mode_sent:
                self.get_logger().info(
                    f"Mode request sent successfully: " f"{self.lastRequestedMode}")
            else:
                self.get_logger().warning(f"Mode request was rejected: "f"{self.lastRequestedMode}")
                self.lastRequestedMode = ""
        except Exception as e:
            self.get_logger().error(f"Mode service error: {e}")
            self.lastRequestedMode = ""
def main(args=None):
    rclpy.init(args=args)
    node = changeMode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
if __name__ == "__main__":
    main()
