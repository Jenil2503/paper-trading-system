import os
from datetime import datetime,timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Header, HTTPException

load_dotenv()

JWT_SECRET = os.environ["JWT_SECRET"]
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60*24

pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def hash_password(plain_password : str):
    return pwd_context.hash(plain_password)

def verify_password(plain_password : str, hashed_password : str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(user_id:int):
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub" : str(user_id), "exp":expire}
    return jwt.encode(payload,JWT_SECRET,algorithm=ALGORITHM)


def decode_access_token(token : str):
    payload = jwt.decode(token,JWT_SECRET,algorithms=[ALGORITHM])
    return int(payload["sub"]) 

def get_current_user_id(authorization : str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authriation header")
    
    token = authorization.replace("Bearer ", "")
    try:
        return decode_access_token(token)
    except Exception:
        raise HTTPException(status_code= 401, detail="Invalid or expired token")