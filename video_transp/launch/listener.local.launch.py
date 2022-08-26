# from launch_ros.actions import Node
# import fogros2
from launch_ros.actions import Node
from launch import LaunchDescription


def generate_launch_description():
    ld = LaunchDescription()

    talker_node = Node(
        package="video_transp", 
        executable="video_pub", 
        output="screen"
    )

    listener_node = Node(
        package="video_transp",
        executable="video_sub",
        output="screen"
    )
    
    ld.add_action(talker_node)
    ld.add_action(listener_node)
    return ld



