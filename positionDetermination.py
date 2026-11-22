#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class positionDetermination(Node):
    def __init__(self):
        super().__init__("positionDetermination")
        self.subscription=self.create_subscription(String,'ballon',self.positionDetermination,10) # gets data from open cv and publishes position
        self.publisher=self.create_publisher(String,'/position',10) 
    def gridName(self, centerX, centerY, cameraWidth, cameraHeight): # get coordinates x and y and camera width and height 
        if centerX < cameraWidth / 3: # divide camera frame to 9 positions and check where the coordinates center are to determine position
            if centerY < cameraHeight / 3:
                position = "top-left"
            elif centerY >= 2 * cameraHeight / 3:
                position = "bottom-left"
            else:
                position = "middle-left"
        elif centerX >= 2 * cameraWidth / 3:
            if centerY < cameraHeight / 3:
                position = "top-right"
            elif centerY >= 2 * cameraHeight / 3:
                position = "bottom-right"
            else:
                position = "middle-right"
        else:
            if centerY < cameraHeight / 3:
                position = "top-mid"
            elif centerY >= 2 * cameraHeight / 3:
                position = "bottom-mid"
            else:
                position = "middle-center"
        return position
    def positionDetermination(self,msg): 
        centerX,centerY,cameraWidth,cameraHeight = msg.data.split(',') #recieve data from opencv in (..,..,..,..) format
        dataVerfication=msg.data.split(',')
        if len(dataVerfication)!=4: #check if the sent data is valid or if its missing a parameter
            self.get_logger().warning(f"invalid data sent")
            return
        centerX=int(dataVerfication[0])
        centerY=int(dataVerfication[1])
        cameraWidth=int(dataVerfication[2])
        cameraHeight=int(dataVerfication[3])
        position=self.gridName(centerX,centerY,cameraWidth,cameraHeight) #send collected data to the function above and return position
        msg = String()
        msg.data = position
        self.publisher.publish(msg) #oublish position
def main(args=None):
    rclpy.init(args=args)
    node = positionDetermination()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == "__main__":
    main()