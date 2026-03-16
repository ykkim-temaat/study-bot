import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    package_name = 'study-bot'

    # 기본 드라이버 런치 파일 포함
    ms200_scan = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'ms200_scan.launch.py')])
    )

    # Rviz2 설정 파일 경로 (study-bot 패키지 내부에 별도 설정이 없다면 기본값 사용 권장)
    # 여기서는 oradar_lidar의 설정을 참조하거나 study-bot의 설정을 새로 만들 수 있습니다.
    # 일단 study-bot 전용 설정을 사용할 수 있도록 경로를 잡습니다.
    rviz_config_path = os.path.join(get_package_share_directory(package_name), 'config', 'ms200_view.rviz')
    
    # Rviz2 노드 실행
    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        output='screen'
    )

    return LaunchDescription([
        ms200_scan,
        rviz2_node
    ])
