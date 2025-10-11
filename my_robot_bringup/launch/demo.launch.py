from launch import LaunchDescription
from launch_ros.actions import Node

def term (title:str) -> str:
    return f'gnome-terminal --tab --title={title} -- bash -c \'exec "$@"\' __node__'

def generate_launch_description():
        ld = LaunchDescription()

        talker_node = Node(
        
            package = "demo_chat",
            executable = "talker",
            emulate_tty = 'True',
            prefix = term("talker")
        )

        listener_node = Node(
            package = "demo_chat",
            executable = "listener",
            emulate_tty ='True',
            prefix = term("listener")

        )


        ld.add_action(talker_node)
        ld.add_action(listener_node)

        return ld