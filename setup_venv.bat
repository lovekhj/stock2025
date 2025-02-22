@echo off

:: 가상환경 생성
python -m venv venv

:: 가상환경 활성화
call venv\Scripts\activate

:: pip 업그레이드
python -m pip install --upgrade pip

:: requirements.txt의 패키지 설치
pip install -r requirements.txt

echo 가상환경이 설정되었습니다.
echo 가상환경을 활성화하려면 'venv\Scripts\activate' 명령어를 실행하세요.
pause 