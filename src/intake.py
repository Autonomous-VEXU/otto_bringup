#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from otto_bringup.srv import Intake
from ros_colorsens_apds9960.msg import ColorProximity
from std_msgs.msg import Float64MultiArray, Empty
from sensor_msgs.msg import JointState

'''
intake motor commands (sign)
------------------------
      | L | M | T |
------|---|---|---|
hopper| - | - | - |
bottom| + | - | - |
middle| - | + | - |
high  | - | + | + |

columns == motor group
rows == desired location
'''

class Intake(Node):
    '''a node that is responsible for intake motor control, will later become an action'''
    def __init__(self):
        super().__init__('intake')

        # parameters
        self.detected_ball = 0 # ball color (0 = none, 1 = red, 2 = blue)
        self.motor_speed = 10.0 # intake motor base speed

        # E stop toggle
        self.e_stop = False

        # motor Float arrays
        self.motor_pos = Float64MultiArray()
        self.motor_pos.data = [-1.0 * self.motor_speed]

        self.motor_neg = Float64MultiArray()
        self.motor_neg.data = [self.motor_speed]

        # create publishers for intake motors
        self.low_motor = self.create_publisher(Float64MultiArray, '/intake_low', 10)
        self.mid_motor = self.create_publisher(Float64MultiArray, '/intake_mid', 10)
        self.top_motor = self.create_publisher(Float64MultiArray, '/intake_high', 10)

        # fix qos
        color_qos = QoSProfile(
            depth=10,
            reliability=QoSReliabilityPolicy.BEST_EFFORT
        )

        # subscribe to color sensor topic
        self.create_subscription(ColorProximity, "/color_sensor", self.color_sensor_callback, qos_profile=color_qos)

        # subscribe to e stop topic
        self.create_subscription(Empty, "/e_stop", self.stop_motors, 10)

    def color_sensor_callback(self, msg:ColorProximity):
        '''color sensor topic callback'''
        if self.e_stop == True:
            return
        
        self.mid_motor.publish(self.motor_neg)
        self.low_motor.publish(self.motor_pos)

        if msg.proximity > 0.025:
            if msg.color.r >= msg.color.b:
                self.get_logger().info("detected red ball")
                self.detected_ball = 1
                self.top_motor.publish(self.motor_pos)
            elif msg.color.b > msg.color.r:
                self.detected_ball = 2
                self.get_logger().info("detected blue ball")
                self.top_motor.publish(self.motor_neg)
        else:
            self.detected_ball = 0
            self.mid_motor.publish(self.motor_neg)
            self.low_motor.publish(self.motor_pos)

    def block_jam_detection(self, msg:JointState): 
        '''detects if a block gets stuck in a intake motor'''

        pass
        
    def stop_motors(self, msg:Empty):
        '''stops all three intake motors through an toggling boolean e-stop'''
        zero_msg = Float64MultiArray()
        zero_msg.data = [0.0]

        self.low_motor.publish(zero_msg)
        self.mid_motor.publish(zero_msg)
        self.top_motor.publish(zero_msg)

        self.e_stop = not self.e_stop # toggle e_stop

        if self.e_stop == True:
            self.get_logger().warn("E-Stop Activated")
        else:
            self.get_logger().warn("E-Stop Disabled")

def main(args=None):
    rclpy.init(args=args)
    node = Intake()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()