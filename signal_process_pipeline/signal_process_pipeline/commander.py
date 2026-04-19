#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int32


class CommanderNode(Node):
    def __init__(self):
        super().__init__('commander_node')
        self.publisher = self.create_publisher(String, '/cmd', 10)
        self.get_logger().info("Commander Node has started. Type 'forward', 'backward', 'left', or 'right'.")



    def run_interface(self):
        while rclpy.ok():
            user_cmd = input("Enter command: ").strip().lower()

            if user_cmd in ['forward', 'backward', 'left', 'right']:
                msg = String()
                msg.data = user_cmd
                self.publisher.publish(msg)
                self.get_logger().info(f"Sent command: {user_cmd}")

            else:
                self.get_logger().warn("Invalid command use")

def main(args=None):
    rclpy.init(args=args)
    node=CommanderNode()
    node.run_interface()
    rclpy.shutdown()