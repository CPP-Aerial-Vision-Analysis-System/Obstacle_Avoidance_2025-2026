from launch import LaunchDescription
from launch_ros.actions import Node

def term(title:str) ->str:#allows for our nodes to be outputted in sperate terminals
    return f'gnome-terminal --tab --title= {title} -- bash -c \'exec "$@"\' node'

def generate_launch_description():
    ld = LaunchDescription()    #creates launch description object

    publisher_node = Node(
        package= "my_weather_check",
        executable= "weather_talker",
        name = 'talker',
        output = 'screen',  #how ros2 handles outputs
        emulate_tty = True,
        prefix = term('talker')
    )
    subscriber_node = Node(
        package= "my_weather_check",
        executable= "weather_listener",
        name = 'listener',
        output = 'screen',  #how ros2 handles outputs
        emulate_tty = True,
        prefix = term('listener'),
    )    
    ld.add_action(publisher_node)
    ld.add_action(subscriber_node)
    return ld