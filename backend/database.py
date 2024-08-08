# Import các thư viện cần thiết từ SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL kết nối đến cơ sở dữ liệu PostgreSQL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456aA@localhost/MSE-DEV-1"

# Tạo engine để quản lý kết nối đến DB
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Tạo sessionmaker để tạo các phiên làm việc (session) với DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tạo lớp cơ sở để các model kế thừa
Base = declarative_base()