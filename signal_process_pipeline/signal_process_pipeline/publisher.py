#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class PubNode(Node):
    def __init__(self):
        super().__init__('publisher_node')
        self.pub = self.create_publisher(Int32, '/raw_signal', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.current_number = 2

    def timer_callback(self):
        msg = Int32()
        msg.data = self.current_number
        self.pub.publish(msg)
        self.get_logger().info(f'Publishing:{msg.data}')
        self.current_number +=2




def main(args = None):
    rclpy.init(args=args)
    node=PubNode()
    rclpy.spin(node)
    rclpy.shutdown()