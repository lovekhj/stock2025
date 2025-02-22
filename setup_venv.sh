#!/bin/bash

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
source venv/bin/activate

# pip 업그레이드
pip install --upgrade pip

# requirements.txt의 패키지 설치
pip install -r requirements.txt

echo "가상환경이 설정되었습니다."
echo "가상환경을 활성화하려면 'source venv/bin/activate' 명령어를 실행하세요." 