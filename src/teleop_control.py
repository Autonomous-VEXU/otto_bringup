import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Empty

class OttoTeleop(Node):
    def __init__(self):
        super().__init__('otto_teleop')

        # sub to controller input
        self.create_subscription(Joy, '/joy', self.controller_input_callback, 10)

        # pub to estop
        self.e_stop = self.create_publisher(Empty, )

        # controller debounce
        self.prev_button_0 = 0
        self.prev_button_1 = 0
        self.prev_button_2 = 0 
        self.prev_button_3 = 0

    def controller_input_callback(self, msg:Joy):
        '''handle controller input'''

        if msg.buttons[1] == 1 and self.prev_button_1 == 0: 
            self.scoring_callback(2)
        elif msg.buttons[0] == 1 and self.prev_button_0 == 0: 
            self.check_collision()
        elif msg.buttons[2] ==1 and self.prev_button_2 == 0:
            self.scoring_callback(3)
        elif msg.buttons[3] == 1 and self.prev_button_3 == 0: 
            self.scoring_callback(1)

        self.prev_button_0 = msg.buttons[0]
        self.prev_button_1 = msg.buttons[1]
        self.prev_button_2 = msg.buttons[2]
        self.prev_button_3 = msg.buttons[3]

def main(args=None):
    rclpy.init(args=args)
    node = OttoTeleop()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()