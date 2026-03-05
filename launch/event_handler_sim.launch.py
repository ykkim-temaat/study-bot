import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, TimerAction, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.event_handlers import OnProcessExit # <-- [추가됨] 이벤트 핸들러 모듈

from launch_ros.actions import Node

def generate_launch_description():

    package_name='study-bot'

    # 1. 로봇 뼈대 (변함 없음)
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name), 'launch', 'rsp.launch.py')]), 
            launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 2. 월드 변수 선언 (변함 없음)
    world = LaunchConfiguration('world')
    world_arg = DeclareLaunchArgument(
        'world',
        default_value="empty.sdf",
        description='World to load'
    )

    # 3. Gazebo 실행 (변함 없음)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
            launch_arguments={'gz_args': ['-r -v4 ', world, ' --render-engine ogre'], 'on_exit_shutdown': 'true'}.items()
    )

    # 4. 로봇 소환 노드 (변함 없음, 단 리스트에 바로 넣지 않음)
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'study-bot',
                                   '-z', '0.1'],
                        output='screen')

    # 5. 브리지 노드 (변함 없음, 단 리스트에 바로 넣지 않음)
    bridge_params = os.path.join(get_package_share_directory(package_name),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=['--ros-args', '-p', f'config_file:={bridge_params}']
    )

    # ========================================================================
    # 💡 [핵심 추가] 이벤트 핸들러 및 타이머 설정 구역
    # ========================================================================

    # 이벤트 A: Gazebo가 켜질 시간을 주기 위해, 런치 파일 실행 3초 뒤에 로봇 소환(spawn_entity) 실행
    delay_spawn = TimerAction(
        period=3.0,
        actions=[spawn_entity]
    )

    # 이벤트 B: 로봇 소환(spawn_entity) 프로세스가 '완료(Exit)'되면, 그제서야 통신 브리지(ros_gz_bridge) 실행
    bridge_after_spawn = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=spawn_entity,
            on_exit=[ros_gz_bridge]
        )
    )

    # Launch them all!
    # 기존 spawn_entity와 ros_gz_bridge가 빠지고, 그 자리를 이벤트 액션들이 대체합니다.
    return LaunchDescription([
        world_arg,          # 선언부 
        rsp,                # 실행부 1: 로봇 뼈대 계산
        gazebo,             # 실행부 2: 가제보 켜기
        delay_spawn,        # 실행부 3: (3초 대기 후) 로봇 소환
        bridge_after_spawn  # 실행부 4: (로봇 소환 끝나면) 브리지 연결
    ])