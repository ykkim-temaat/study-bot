import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node

def generate_launch_description():

    # 패키지 이름 설정
    package_name = 'study-bot'
    lidar_package_name = 'oradar_lidar'

    # Launch Arguments 정의
    port_name_arg = DeclareLaunchArgument(
        'port_name',
        default_value='/dev/ttyUSB0',
        description='MS200 LiDAR serial port'
    )

    # robot_state_publisher 실행 (우리 패키지의 rsp.launch.py 활용)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py')]),
            launch_arguments={'use_sim_time': 'true'}.items()
    )

    # MS200 LiDAR 드라이버 노드 실행 (oradar_lidar 패키지)
    # TF 브로드캐스터 노드는 포함하지 않음 (URDF에서 정의됨)
    ms200_driver_node = Node(
        package=lidar_package_name,
        executable='oradar_scan',
        name='MS200',
        output='screen',
        parameters=[
            {'device_model': 'MS200'},
            {'frame_id': 'laser_frame'},
            {'scan_topic': '/scan'},
            {'port_name': LaunchConfiguration('port_name')},
            {'baudrate': 230400},
            {'angle_min': 0.0},
            {'angle_max': 360.0},
            {'range_min': 0.05},
            {'range_max': 20.0},
            {'clockwise': False},
            {'motor_speed': 10}
        ]
    )

    # 런치 설명(LaunchDescription) 반환
    return LaunchDescription([
        port_name_arg,
        rsp,
        ms200_driver_node
    ])
