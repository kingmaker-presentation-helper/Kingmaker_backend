import sqlite3
from passlib.context import CryptContext

# SQLite 연결 및 테이블 생성
conn = sqlite3.connect('local_database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        hashed_password TEXT NOT NULL
    )
''')

conn.commit()

# password 암호화 모듈
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# password 비교
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# password 암호화
def hash_password(password):
    return pwd_context.hash(password)


# DB 에서 User 정보 가져오기
def get_user_info(user_email: str):
    cursor.execute("SELECT * FROM users WHERE email=?", (user_email,))
    user_info = cursor.fetchone()
    if user_info:
        return {"email": user_info[1], "hashed_password": user_info[2]}
    else:
        return None
