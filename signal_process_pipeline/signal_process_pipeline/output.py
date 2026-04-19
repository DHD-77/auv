#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class OutNode(Node):
    def __init__(self):
        super().__init__('output_node')
        self.subscription = self.create_subscription(Int32, '/processed_signal', self.out_callback, 10)


    def out_callback(self, msg):
        input_value = msg.data
        final_value = input_value+10
        self.get_logger().info(f"{final_value}")


def main(args=None):
    rclpy.init(args=args)
    node = OutNode()
    rclpy.spin(node)
    rclpy.shutdown()