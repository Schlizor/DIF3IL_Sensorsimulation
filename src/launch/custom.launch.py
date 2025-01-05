from launch import LaunchDescription
import os

from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    rviz_config_file = os.path.join(
        get_package_share_directory("ros_tcp_endpoint"), "config", "basic.rviz"
    )

    return LaunchDescription(
        [
            Node(
                package="ros_tcp_endpoint",
                executable="default_server_endpoint",
                name="ros_tcp_server",
                output="screen",
            ),
            # OctoMap Server Node
            Node(
                package="octomap_server2",
                executable="octomap_server_node",
                name="octomap_server",
                output="screen",
                parameters=[
                    {"resolution": 0.05},  # Auflösung in Metern
                    {"frame_id": "map"},  # Fixed Frame
                ],
                remappings=[
                    ("cloud_in", "/lidar/pointcloud2"),  # Remapping für die Pointcloud
                ],
            ),
            # Optional: RViz starten
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", rviz_config_file],
            ),
        ]
    )
