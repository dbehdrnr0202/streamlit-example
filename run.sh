#!/bin/bash
# 필요한 패키지가 설치되어 있는지 확인하고 없으면 설치
if ! command -v streamlit &> /dev/null
then
    echo "Streamlit이 설치되어 있지 않습니다. 설치 중..."
    pip install streamlit
fi
python -m streamlit run main.py