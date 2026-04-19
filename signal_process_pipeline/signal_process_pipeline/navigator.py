#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from custom_interfaces.msg import BotPose


class NavigatorNode(Node):
    def __init__(self):
        super().__init__('navigator_node')
        self.subscription = self.create_subscription(String, '/cmd', self.navigator_callback, 10)
        self.publish = self.create_publisher(BotPose, '/bot_pose', 10)
        self.get_logger().info("Navigator node has started")
        self.x = 0.0
        self.y = 0.0
        self.current_direction = "North"

    def navigator_callback(self, msg):
        cmd = msg.data.lower()

        if cmd == "forward":
            if self.current_direction == "North":
                self.y +=1.0
            
            elif self.current_direction == "South":
                self.y -= 1.0

            elif self.current_direction == "East":
                self.x += 1.0

            elif self.current_direction == "West":
                self.x -= 1.0


        elif cmd == "backward":
            if self.current_direction == "North":
                self.y -=1.0
            
            elif self.current_direction == "South":
                self.y += 1.0

            elif self.current_direction == "East":
                self.x -= 1.0

            elif self.current_direction == "West":
                self.x += 1.0
            
        elif cmd == "left":
            if self.current_direction == "North":
                self.current_direction = "West"

            elif self.current_direction == "South":
                self.current_direction = "East"

            elif self.current_direction == "East":
                self.current_direction = "North"

            elif self.current_direction == "West":
                self.current_direction = "South"


        elif cmd == "right":
            if self.current_direction == "North":
                self.current_direction = "East"

            elif self.current_direction == "East":   
                self.current_direction = "South"

            elif self.current_direction == "South":
                self.current_direction = "West"

            elif self.current_direction == "West":
                self.current_direction = "North"

        else:
            self.get_logger().warn(f"Unknown command: {cmd}")
            return
        

        pose_msg = BotPose()
        pose_msg.x = self.x
        pose_msg.y = self.y
        pose_msg.facing_direction = self.current_direction

        self.publish.publish(pose_msg)
        self.get_logger().info(f"Moved to ({self.x}, {self.y}) facing {self.current_direction}")







def main(args=None):
    rclpy.init(args=args)
    node = NavigatorNode()
    rclpy.spin(node)
    rclpy.shutdown()