import os  # 운영체제와 상호작용(환경변수 사용 등)을 위한 모듈

from dotenv import load_dotenv  # .env 파일에서 환경변수 불러오기
from sqlalchemy import create_engine  # 데이터베이스 연결을 위한 엔진 생성
from sqlalchemy.ext.declarative import declarative_base  # 데이터베이스 모델의 기본 클래스
from sqlalchemy.orm import sessionmaker  # 데이터베이스와 대화할 세션 생성

# .env 파일에서 환경변수 불러오기 (.env 파일에는 DB 정보가 저장되어 있음)
load_dotenv()

# 데이터베이스 타입 확인 (기본값: sqlite)
DB_TYPE = os.getenv("DB_TYPE", "sqlite")

if DB_TYPE == "mysql":
    # MySQL 설정
    DB_USERNAME = os.getenv("DB_USERNAME")  # 사용자 이름
    DB_PASSWORD = os.getenv("DB_PASSWORD")  # 비밀번호
    DB_HOST = os.getenv("DB_HOST")          # 데이터베이스 주소
    DB_PORT = os.getenv("DB_PORT")          # 포트 번호
    DB_DATABASE = os.getenv("DB_DATABASE")  # 데이터베이스 이름
    
    # 데이터베이스 접속 주소 만들기
    DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
    
    # 데이터베이스와 연결하는 엔진 생성
    engine = create_engine(
        DATABASE_URL,
        pool_recycle=3600,      # 1시간마다 연결을 새로 만듦 (오래된 연결 방지)
        pool_pre_ping=True,     # 연결이 살아있는지 확인
        echo=True               # 실행되는 SQL 쿼리 로그 출력
    )
else:
    # SQLite 설정 (기본값) - 로컬 개발용
    DATABASE_URL = "sqlite:///./csu_page.db"
    
    # 데이터베이스와 연결하는 엔진 생성
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},  # SQLite 전용 설정
        echo=True  # 실행되는 SQL 쿼리 로그 출력
    )

# 데이터베이스와 대화할 세션 생성 함수
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델을 만들 때 사용하는 기본 클래스
Base = declarative_base()

# 데이터베이스 세션을 생성하고, 사용이 끝나면 닫아주는 함수
def get_db():
    db = SessionLocal()  # 세션 생성
    try:
        yield db         # 세션을 반환 (필요한 곳에서 사용)
    finally:
        db.close()       # 사용이 끝나면 세션 닫기