#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from otto_bringup.srv import Intake # type: ignore
from ros_colorsens_apds9960.msg import ColorProximity
from std_msgs.msg import Float64MultiArray


'''
intake moveset:
    - intake ball (to_hopper:bool, duration) [will need color sensor integration]
    - score high (duration)
    - score mid (duration)
    - score low (duration)
    - reject ball (level:int) [will need color sensor integration]
'''

class Intake(Node):
    '''a node that is responsible for intake motor control, will later become an action'''
    def __init__(self):
        super().__init__('intake')

        #sensor debug flag
        sensor_test = True

        if sensor_test == False:
            # intake service server
            self.intake = self.create_service()

            # parameters
            self.detected_ball = 0 # ball color (0 = none, 1 = red, 2 = blue)
            self.motor_speed = 4.0 # motor base speed

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
        self.apds9960 = self.create_subscription(ColorProximity, "/color_sensor", self.color_sensor_callback, qos_profile=color_qos)
    
    def color_sensor_callback(self, msg:ColorProximity):
        '''color sensor topic callback'''
        # is there a ball present?
        if msg.proximity > 0.025:
            if msg.color.r >= msg.color.b:
                self.get_logger().info("detected red ball")
            elif msg.color.b > msg.color.r:
                self.detected_ball = 2
                self.get_logger().info("detected blue ball")
        else:
            self.detected_ball = 0

    def intake_srv_callback(self, request, reponse):
        '''intake service callback''' 
        match request.type:
            case 0: 
                self.intake_ball()
            case 1: 
                self.score_low(request.toggle)
            case 2: 
                self.score_mid(request.toggle)
            case 3: 
                self.score_top(request.toggle)
            case 4:
                self.stop_motors()

    def intake_ball(self): 
        '''intake a ball to the hopper'''
        msg = Float64MultiArray()
        msg.data = self.motor_speed
        self.low_motor.publish()
        self.mid_motor.publish()

        # if color is not what is expected, reject ball with score top
        
    def score_top(self):
        '''score a ball in the top goal'''
        self.low_motor.publish()
        self.mid_motor.publish()
        self.top_motor.publish()

    def score_mid(self): 
        '''score a ball in the mid goal'''
        self.low_motor.publish()
        self.mid_motor.publish()
        self.top_motor.publish()

    def score_low(self): 
        '''score a ball in the low goal'''
        self.low_motor.publish()
        self.mid_motor.publish()
        self.top_motor.publish()
    
    def stop_motors(self):
        zero_msg = Float64MultiArray()
        zero_msg.data = 0.0
        self.low_motor.publish(zero_msg)
        self.mid_motor.publish(zero_msg)
        self.high_motor.publish(zero_msg)
        self.get_logger().info("Stopped intake motors")

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