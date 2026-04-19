#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class ProcessNode(Node):
    def __init__(self):
        super().__init__('processor_node')
        self.subscription = self.create_subscription(Int32, '/raw_signal', self.listener_callback, 10)
        self.publisher = self.create_publisher(Int32, '/processed_signal', 10)
    
    def listener_callback(self, msg):
        input_value = msg.data
        multiplied_value = input_value * 5
        out_msg = Int32()
        out_msg.data = multiplied_value
        self.publisher.publish(out_msg)
        self.get_logger().info(f"Relaying {input_value} -> {multiplied_value} ")






def main(args=None):
    rclpy.init(args=args)
    node=ProcessNode()
    rclpy.spin(node)
    rclpy.shutdown()