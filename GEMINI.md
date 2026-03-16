# Package: study-bot

## 🤖 Robot Description
- **Link Hierarchy**: `base_link` -> `chassis` -> `laser_frame` / `wheels` / `caster`.
- **URDF Base**: `description/robot.urdf.xacro`.
- **Lidar URDF**: `description/lidar.xacro`.

## 🔋 Hardware Integration Status
- **LiDAR**: MS200 LiDAR (Driver in `oradar_lidar` package).
- **Physical Link**: `laser_frame` (URDF 내 0.175m 높이 설정됨 vs 드라이버 런치 파일 0.18m 비교 필요).
- **Control**: `gazebo_control.xacro` 기반 차동 구동 (Differential Drive).

## 🛠 Next Step: Execute Merge Prompt 002
- [x] 통합용 프롬프트 `002_ms200_lidar_studybot_integration.md` 작성 완료.
- [ ] `prompts/002_*.md` 지침에 따라 `ms200.launch.py` 구현.
- [ ] `ms200_scan.launch.py`의 TF 브로드캐스터와 `robot_state_publisher` 간의 충돌 방지 (Xacro 기반 TF 사용).

## ⚠️ Known Issues / Notes
- `laser_frame` 좌표계가 실제 센서 마운팅과 일치하는지 물리적 측정 필요.
- 가상환경(VMware) 상에서 USB 장치 연결 시 `/dev/ttyUSB0` 인식 여부 확인 필수.
