from launch import LaunchDescription
from launch_ros.actions import Node


def term(title: str) -> str:
    return f'gnome-terminal --tab --title={title} -- bash -c \'exec "$@"\' __node__'

def generate_launch_description():
    return LaunchDescription([
        Node(package='demo', 
             executable='talker',
             emulate_tty=True,
             prefix=term('talker')),

        Node(package='demo', 
             executable='listener',
             emulate_tty=True,
             prefix=term('listener')),
    ])