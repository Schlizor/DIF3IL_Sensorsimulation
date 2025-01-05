from launch import LaunchDescription

from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    package_name = "ros_tcp_endpoint"
    config_directory = os.path.join(get_package_share_directory(package_name), "config")
    rviz_config_file = os.path.join(config_directory, "basic.rviz")

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
                package="octomap_server",
                executable="octomap_server_node",
                name="octomap_server",
                output="screen",
                parameters=[
                    {"resolution": 0.05},  # Auflösung in Metern
                    {"frame_id": "map"},  # Fixed Frame
                    {"publish_full_map": True},  # Vollständige Karte veröffentlichen
                    {"publish_binary_map": True},  # Binäre Karte veröffentlichen
                    {
                        "publish_free_space": True
                    },  # Freie Bereiche veröffentlichen (optional)
                ],
                remappings=[
                    (
                        "cloud_in",
                        "/simulated/lidar/pointcloud2",
                    ),  # Remapping für die Pointcloud
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
