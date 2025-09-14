# 사용도구
- postman 
- github
- docker
- gpt

# 간단 페이지 만들기 
벡엔드
- fastapi
프론트엔드
- html, css, js
데이터베이스
- mysql or mariadb 

python3 -m venv <가상환경이름>\
python3 -m venv venv # 파이썬 가상환경 만들기\
source ./venv/bin/activate # 가상환경 활성화\
pip install fastapi==0.74.1 # fastapi 설치\
pip install "uvicorn[standard]" # uvicorn 설치\
하지만 우리는 이렇게 일일이 설치하는게 귀찮으니까 \
requirements.txt 를 만들어서 한번에 설치하게 설정\

fastapi 실행 
uvicorn main:app --reload
