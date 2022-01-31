# 비접촉 터치 시스템(Virtual Mouse)

창의공학 종합설계 무정차 방지 시스템 사이드 프로젝트
> 기존의 화면에 터치하여 조작하는 키오스크 방식을 대체하기 위해 손의 랜드마크를 감지하고 제스처 패턴을 추적하는 실시간 카메라와 함께 Python, openCV, Mediapipe를 활용한 비접촉 터치 시스템을 개발했습니다. 비접촉 시스템은 화면에 손으로 조작할 수 있는 가상의 마우스 구현을 통해 화면 조작을 진행합니다.

## Demo
> 무정차 방지 키오스크 조작 영상


## Dependencies
- openCv
- mediapipe
- mouse (linux 환경에서 사용하기 위한)
- pynput (linux 환경에서 사용하기 위한)
- numpy

## Installation
1. 해당 레포지토리를 clone 합니다.
```bash
git clone https://github.com/ckdrkt2/virtual_mouse.git
```
2. ```AIVirtualMouse.py```를 실행합니다.
3. 버튼이 클릭되는 것을 확인하고 싶다면 ```testui.py```를 함께 실행해서 테스트해볼 수 있습니다.

## Project WIKI
- https://capstone.uos.ac.kr/mie/index.php/3%EC%A1%B0-%EB%B2%84%EC%A0%80%EB%B9%84%ED%84%B0

## Reference
- https://github.com/ravigithub19/ai-virtual-mouse